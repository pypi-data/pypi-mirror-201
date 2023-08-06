"""Module to conditionally execute transform logic for silver and gold pipelines based on project metadata
   including creating Databricks views and/or tables.
"""

import os
import sys  # don't remove required for error handling


from importlib import util  # library management
import traceback  # don't remove required for error handling
import json
from html.parser import HTMLParser  # web scraping html
from string import Formatter
import base64
import requests
import re

# spark
# https://superuser.com/questions/1436855/port-binding-error-in-pyspark
from pyspark.sql import SparkSession


pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    # import pyspark.pandas  as pd
    # bug - pyspark version will not read local files in the repo
    import pyspark.pandas as pd
else:
    import pandas as pd


class PipelineMetaData:
    """Class to conditionally execute transform logic for silver and gold pipelines based on project metadata
    including creating Databricks views and/or tables.
    """

    @staticmethod
    def get_configuration_for_pipeline(config, pipeline_metadata):
        """Takes in config dictionary and pipeline_metadata, returns populated config_pipeline dictionary

        Args:
            config (_type_): _description_
            pipeline_metadata (_type_): _description_

        Returns:
            _type_: _description_
        """

        arg_list = {}

        yyyy_param = config["yyyy"]
        mm_param = config["mm"]
        dd_param = config["dd"]
        if len(dd_param.strip()) == 0 or dd_param.strip() == 'N/A' or dd_param.strip() == 'NA':
            transmission_period = mm_param + "_" + yyyy_param
            dd_param = "NA"
        else:
            transmission_period = yyyy_param + "_" + mm_param + "_" + dd_param

        environment = config["environment"]
        override_save_flag = config["override_save_flag"]

        row = pipeline_metadata

        execute_flag = row["execute_flag"]
        pipeline_parameters = row["pipeline_parameters"]
        export_schema_metrics = row["export_schema_metrics"]
        view_name = row["view_name"]
        pipeline_name = row["pipeline_name"]
        query_name = row["pipeline_name"]
        if view_name is not None:
            view_name = str(view_name).strip()
            if len(view_name) > 0:
                # some queries have multiple params, save for each
                pipeline_name = view_name

        if pipeline_name is view_name:
            print("saving pipeline with view name")
        else:
            if pipeline_name is None or pipeline_name == "":
                print("pipeline_name is blank")
            else:
                print(f"saving pipeline with pipeline_name:{pipeline_name}")

        row_id_keys = row["row_id_keys"]

        # execute
        arg_dictionary = dict()

        if pipeline_parameters is None:
            print("pipeline_parameters are empty")
            pipeline_parameters = ""
        else:
            pipeline_parameters = pipeline_parameters.strip()

        config_pipeline = {"pipeline_parameters": pipeline_parameters}

        if pipeline_parameters != "":
            print("pipeline_parameters are " + pipeline_parameters)
            arg_list = [x.strip() for x in pipeline_parameters.split("|")]
            for line in arg_list:
                pair = [x.strip() for x in line.split(":")]
                if len(pair) > 1:
                    arg_dictionary[pair[0]] = pair[1]
                else:
                    arg_dictionary[pair[0]] = ""
        else:
            print("pipeline_parameters are blank")

        arg_dictionary["environment"] = environment
        arg_dictionary["yyyy"] = yyyy_param
        arg_dictionary["mm"] = mm_param
        arg_dictionary["dd"] = dd_param
        arg_dictionary["transmission_period"] = transmission_period

        # save the pipeline name as view name
        # this allows for the same pipeline to be saved multiple times with different paramters

        if override_save_flag == "override_with_save":
            save_flag = "save"
        elif override_save_flag == "override_with_skip_save":
            save_flag = "skip_save"
        else:
            save_flag = "default"

        if save_flag == "default":
            if row["save_flag"] is not None:
                if len(row["save_flag"]) > 0:
                    save_flag = row["save_flag"]
            else:
                save_flag = "save"

        execute_results_flag = row["execute_results_flag"]
        if execute_results_flag is None:
            execute_results_flag = "skip_execute"
        if execute_results_flag.strip() == "":
            execute_results_flag = "skip_execute"

        config_pipeline["transmission_period"] = transmission_period
        config_pipeline["environment_for_live"] = "environment_for_live_dev"
        config_pipeline["live_prefix"] = "live_"
        config_pipeline["pipeline_name"] = pipeline_name
        config_pipeline["query_name"] = query_name
        config_pipeline["view_name"] = view_name
        config_pipeline["save_flag"] = save_flag
        config_pipeline["execute_flag"] = execute_flag
        config_pipeline["arg_dictionary"] = arg_dictionary
        config_pipeline["export_schema_metrics"] = export_schema_metrics
        config_pipeline["row_id_keys"] = row_id_keys
        config_pipeline["execute_results_flag"] = execute_results_flag

        return config_pipeline

    @staticmethod
    def get_execute_pipeline_parameters(
        config,
        config_pipeline
    ):
        """Takes in config dictionary, config_pipeline, and repository path, returns result of executed pipelines

        Args:
            config (_type_): _description_
            config_pipeline (_type_): _description_
            config_pipeline (_type_): _description_
            repository_path (_type_): _description_

        Returns:
            _type_: _description_
        """

        repository_path = config["repository_path"]
        environment = config["environment"]
        project_id = config["project_id"]
        project_id_root = config["project_id_root"]
        pipeline_name = config_pipeline["pipeline_name"]
        arg_dictionary = config_pipeline["arg_dictionary"]
        live_prefix = config_pipeline["live_prefix"]
        environment_for_live = config_pipeline["environment_for_live"]

        base_path = "".join([repository_path.rstrip('/'), "/", project_id_root, "/", project_id])
        base_path = base_path.replace("/Workspace", "")
        dir_name_python = "".join([base_path, "/autogenerated/python/"])
        # clean up double slashes
        dir_name_python = dir_name_python.replace('//','/')
        pipeline_name = pipeline_name.replace(project_id, "")
        pipeline_name = pipeline_name.replace(".", "")
        pipeline_name = project_id + "_" + pipeline_name
        path_to_execute = "".join([dir_name_python, pipeline_name])
        database_prefix = "davt_" + project_id + "_" + environment
        arg_dictionary["live_prefix"] = live_prefix
        arg_dictionary["environment_for_live"] = environment_for_live
        arg_dictionary["database_prefix"] = database_prefix

        config_pipeline["arg_dictionary"] = arg_dictionary
        config_pipeline["path_to_execute"] = path_to_execute
        print(f"config_pipeline:{str(config_pipeline)}")
        return config_pipeline

    @staticmethod
    def get_view_dataframe(config, spark, config_pipeline):
        """Takes in config dictionary, spark and config pipeline
        and returns dataframe with columns sorted

        Args:
            config (_type_): _description_
            spark (_type_): _description_
            config_pipeline (_type_): _description_

        Returns:
            sorted_df: _description_
        """

        davt_database_name = config["davt_database_name"]
        view_name = config_pipeline["view_name"]

        full_view_name = f"{davt_database_name}.{view_name}"
        sql_statement = f"SELECT * FROM {full_view_name}"
        print(f"sql_statement:{sql_statement}")
        unsorted_df = spark.sql(sql_statement)
        sorted_df = unsorted_df.select(sorted(unsorted_df.columns))
        sorted_df.createOrReplaceTempView("table_sorted_df")

        config_pipeline["full_view_name"] = full_view_name

        return sorted_df

    @staticmethod
    def save_pipeline_sql(config, config_pipeline):
        """Takes in config dictionary, config_pipeline dictionary, token, repository_path
        and saves sql

        Args:
            config (_type_): _description_
            config_pipeline (_type_): _description_

        Returns:
            _type_: _description_
        """

        token = config["access_token"]
        repository_path = config["repository_path"]

        # environment vars
        yyyy_param = config["yyyy"]
        mm_param = config["mm"]
        dd_param = config["dd"]
        environment = config["environment"]
        databricks_instance_id = config["databricks_instance_id"]
        project_id = config["project_id"]
        project_id_root = config["project_id_root"]

        # pipeline vars
        query_name = config_pipeline["query_name"]
        pipeline_name = config_pipeline["pipeline_name"]
        execute_results_flag = config_pipeline["execute_results_flag"]
        live_prefix = config_pipeline["live_prefix"]
        environment_for_live = config_pipeline["environment_for_live"]
        arg_dictionary = config_pipeline["arg_dictionary"]
        transmission_period = config_pipeline["transmission_period"]

        base_path = "".join(
            [repository_path, "/", project_id_root, "/", project_id, "/"]
        )
        base_path = base_path.replace("/Workspace", "")
        dir_name_python = "".join([base_path.rstrip("/"), "/autogenerated/python/"])
        dir_name_sql = "".join([base_path.rstrip("/"), "/autogenerated/sql/"])
        dir_name_sql = dir_name_sql.replace('//','/')
        message = f"dir_name_sql:{dir_name_sql}"
        print(message)
        message = f"dir_name_python:{dir_name_python}"
        print(message)
        bearer = "Bearer " + token
        headers = {"Authorization": bearer, "Content-Type": "application/json"}
        headers_redacted = str(headers).replace(bearer, "[bearer REDACTED]")
        api_version = "/api/2.0/preview/sql"
        text = ["/queries?page_size=50&page=1&order=-executed_at&q=", query_name]
        api_command = "".join(text)
        url = f"https://{databricks_instance_id}{api_version}{api_command}"
        print(f"- Attempting FETCH-SQL for query_name:{query_name} url:{str(url)} ----")
        print(f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers)

        data = None
        data_sql = None

        try:
            data = json.loads(response.text)
            response_text = response.text
            response_text_fetch = (
                f"Received FETCH-SQL with length : {len(str(response_text))}"
            )
            response_text_fetch = response_text_fetch + f" when posting to : {url} to fetch sql query: {query_name}"
            print("- response : success  -")
            print(f"{response_text_fetch}")
        except Exception as exception_check:
            html_filter = HTMLFilter()
            html_filter.feed(response.text)
            response_text = html_filter.text
            print(f"- response : error - {str(exception_check)}")
            print(f"Error converting response text:{response_text} to json")

        if data is None:
            print("Error loading sql query")
        else:
            query_text = (
                "# Check configuration of view in list - no query content was found"
            )
            response = "not set"

            for i in data["results"]:
                # print(i)
                query_text_original = i["query"]
                query_text = query_text_original.replace("{{", "TEMPORARY_OPEN_BRACKET").replace("}}", "TEMPORARY_CLOSE_BRACKET")
                query_text = query_text.replace("{", "{{").replace("}", "}}")
                query_text = query_text.replace("TEMPORARY_OPEN_BRACKET", "{").replace("TEMPORARY_CLOSE_BRACKET", "}")
                query_text = query_text.lstrip()
                query_text = query_text.rstrip()
                query_text = query_text.replace('"','\\"')

                # remove -- comments
                query_text = re.sub(r'^--.*\n?', '', query_text, flags=re.MULTILINE)

                if query_text == "":
                    print(f"query name{query_name}:")
                    print(f"{query_text} not found in DataBricks SQL")
                else:
                    if not query_text.endswith(";"):
                        query_text += ";"
                ph = "TEMPORARY_OPEN_BRACKET"
                variable_text = f'execute_results_flag = "{execute_results_flag}"'
                query_parse = query_text_original.replace("{{", "{").replace("}}", "}")
                # print(f"query_parse:{query_parse}")
                param_list = [
                    fname for _, fname, _, _ in Formatter().parse(query_parse) if fname
                ]
                print(f"param_list:{str(param_list)}")
                dict_param_unique = dict()
                for line in list(dict.fromkeys(param_list)):
                    line = line.replace('"', "").replace("'", "")
                    if line.strip() == "environment":
                        dict_param_unique["'" + line.strip() + "'"] = environment
                    elif line.strip() == "live_prefix":
                        dict_param_unique["'" + line.strip() + "'"] = live_prefix
                    elif line.strip() == "environment_for_live":
                        dict_param_unique[
                            "'" + line.strip() + "'"
                        ] = environment_for_live
                    else:
                        dict_param_unique["'" + line.strip() + "'"] = (
                            "'enter " + line.strip() + " value'"
                        )

                dict_param_unique["yyyy"] = yyyy_param
                dict_param_unique["mm"] = mm_param
                dict_param_unique["dd"] = dd_param
                dict_param_unique["transmission_period"] = transmission_period

                sql_command_text = 'sql_command_text = """' + query_text + '""".format(**dict_parameters)'
                print_query_text = f"print(sql_command_text)"
                print_df_results_text = """
from pyspark.sql.functions import col
dfResults = spark.sql(sql_command_text)
#display(dfResults)
listColumns=dfResults.columns
#if ("sql_statement"  in listColumns):
#    print(dfResults.first().sql_statement)
if (dfResults.count() > 0):
    if ("sql_statement"  in listColumns):
        dfMerge = spark.sql(dfResults.first().sql_statement)
        display(dfMerge)
"""

                new_param_code = ""
                for line in dict_param_unique:
                    line = line.replace('"', "").replace("'", "")
                    # new_param_code = new_param_code + f"-- MAGIC {line} =  ''\n"
                    if line in arg_dictionary:
                        new_param_code = new_param_code + f"dbutils.widgets.text('{line}', '{arg_dictionary[line]}')\n"
                    else:
                        print(f"{line} not in arg_dictionary")
                        new_param_code = new_param_code + f"dbutils.widgets.text('{line}', 'default')\n"
                    new_param_code = new_param_code + f"{line} = dbutils.widgets.get('{line}')\n"

                dict_code = ""
                for line in dict_param_unique:
                    line = line.replace('"', "").replace("'", "")
                    # new_param_code = new_param_code + f"-- MAGIC {line} =  ''\n"
                    if line in arg_dictionary:
                        line_strip = line.strip().replace("\"","")
                        dict_code = dict_code + f"'{line_strip}':'{arg_dictionary[line]}',"
                    else:
                        print(f"{line} not in arg_dictionary")
                        line_strip = line.strip().replace("\"","")
                        dict_code = dict_code +  f"'{line_strip}':'default',"

                dict_code = dict_code + f"'environment':'{environment}',"
                dict_parameters = "dict_parameters = {" + dict_code.rstrip(",") + "}\n"

                new_param_code = new_param_code + dict_parameters


                print(f"Set query parameters for {query_name}")
                # print('query parameters from new' + new_param_code)
                # print ('query parameters from ' + pipeline_name + '--------->' + new_param_code )
                ###
                # BE CAREFUL ABOUT SPACING - DON'T TRY GET FANCY WITH FORMAT BECAUSE
                # MAY BREAK INDENTS WHICH ARE IMPORTANT TO PYTHON EXECUTION
                ###

                contexttext1 = f"""
{new_param_code}
                """
                contexttext2 = " # COMMAND ----------\n"

                contexttext3 = f"""{sql_command_text}\n"""

                contexttext4 = " # COMMAND ----------\n"

                contexttext5 = f"""{print_query_text}\n"""

                contexttext6 = """ # COMMAND ----------\n"""

                contexttext7 = f"""{variable_text}\n"""

                # contexttext7b = f"""{query_text}\n"""

                contexttext8 = f"""{print_df_results_text}\n"""

                content_text = contexttext1 + contexttext2 + contexttext3 + contexttext4 + contexttext5
                content_text = content_text + contexttext6 + contexttext7 + contexttext8
                content_text = content_text.lstrip()

                api_version = "/api/2.0"
                api_command = "/workspace/import"
                url = f"https://{databricks_instance_id}{api_version}{api_command}"

                pipeline_name = pipeline_name.replace(project_id, "")
                pipeline_name = pipeline_name.replace(".", "")
                pipeline_name = project_id + "_" + pipeline_name

                content_python = base64.b64encode(content_text.encode("UTF-8")).decode(
                    "UTF-8"
                )
                new_path_python = str(os.path.join(dir_name_python, pipeline_name))
                sys.path.append(dir_name_python)
                isdir = os.path.isdir(dir_name_python)
                print(f"dir_name_python: isdir:{isdir}")

                ## Try to delete the file ##
                try:
                    os.remove(new_path_python)
                except OSError as e:  ## if failed, report it back to the user ##
                    print ("Error: %s - %s." % (e.filename, e.strerror))

                # Python
                # post
                data_python = {
                    "content": content_python,
                    "path": new_path_python,
                    "language": "PYTHON",
                    "overwrite": True,
                    "format": "SOURCE",
                }
                print(f"------- Save Python {pipeline_name}  -------")
                print(f"url:{str(url)}")

                headers_import = {"Authorization": bearer, "Accept": "application/json"}
                headers_redacted = str(headers_import).replace(
                    bearer, "[bearer REDACTED]"
                )
                print(f"headers:{headers_redacted}")
                print(f"json:{str(data_python)}")

                # response
                response_python = requests.post(
                    url=url, json=data_python, headers=headers_import
                )

                try:
                    data = json.loads(response_python.text)
                    response_python_text = json.dumps(response_python.json())
                    print("- response : success  -")
                    response_python_text_message = "Received SAVE-PYTHON-RESPONSE : "
                    response_python_text_message += f"{response_python.text} when posting to : {url}  "
                    response_python_text_message += f"to save python pipeline with sql query: {pipeline_name}"
                    response_python_text_message += f"to {new_path_python}"
                except Exception as exception_check:
                    html_filter = HTMLFilter()
                    html_filter.feed(response_python.text)
                    response_python_text = html_filter.text
                    print(f"- response : error - {str(exception_check)}")
                    print(
                        f"Error SAVE-PYTHON-RESPONSE converting response text:{response_python_text} to json"
                    )

                print(response_python_text)
                sys.path.append(dir_name_sql)

                content_sql = base64.b64encode(
                    query_text_original.encode("UTF-8")
                ).decode("UTF-8")
                # replace period in file name
                query_name = query_name.replace(".", "_")
                new_path_sql = str(os.path.join(dir_name_sql, query_name))
                ## Try to delete the file ##
                try:
                    os.remove(new_path_sql)
                except OSError as e:  ## if failed, report it back to the user ##
                    print ("Error: %s - %s." % (e.filename, e.strerror))

                data_sql = {
                    "content": content_sql,
                    "path": new_path_sql,
                    "language": "SQL",
                    "overwrite": True,
                    "format": "SOURCE",
                }
                print("------- Save SQL ----------------")
                print(f"url:{str(url)}")
                headers_redacted = str(headers).replace(bearer, "[bearer REDACTED]")
                print(f"headers:{headers_redacted}")
                print(f"json:{str(data_sql)}")

            # post
        response_sql = requests.post(url=url, json=data_sql, headers=headers)
        config_sql = {"response_sql": response_sql}
        return config_sql


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data
