import pandas as pd
from robot.api.deco import keyword
from sqlalchemy import create_engine
import base64
import yaml
import matplotlib.pyplot as plt
from IPython.display import display
from robot.api import logger


@keyword('Get Query from File')
def get_query_from_file(file_path):
    """
    Reads SQL query from file

    :param file_path: path to file containing SQL query
    :return: SQL query as a string
    """
    logger.info('Step 1: Reading SQL query from file...')
    with open(file_path, 'r') as file:
        return file.read()


@keyword('Execute Query')
def execute_query(query, database_config_name, query_params=None):
    """
    Executes SQL query on specified database configuration using SQLAlchemy

    :param query: SQL query to execute
    :param database_config_name: name of database configuration in config file
    :param query_params: optional dictionary of query parameters
    :return: pandas dataframe containing query results
    """
    # Step 1: Load database configuration from config file
    logger.info('Step 1: Loading database configuration from config file...')
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    db_config = config['database_configurations'][database_config_name]

    # Step 2: Connect to database using SQLAlchemy
    logger.info('Step 2: Connecting to database using SQLAlchemy...')
    password = base64.b64decode(db_config['password'].encode()).decode()  # decode base64-encoded password
    engine = create_engine(
        f'oracle://{db_config["username"]}:{password}@{db_config["host"]}:{db_config["port"]}/'
        f'?service_name={db_config["service_name"]}')

    # Step 3: Execute SQL query
    logger.info('Step 3: Executing SQL query...')
    if query_params:
        result = pd.read_sql_query(query, engine, params=query_params)
    else:
        result = pd.read_sql_query(query, engine)

    return result


@keyword('Plot Data')
def plot_data(dataframe):
    """
    Plots query results as a graph and displays them as a dataframe

    :param dataframe: pandas dataframe containing query results
    """
    # Step 1: Plot data as graph
    logger.info('Step 1: Plotting data as graph...')
    plt.figure(figsize=(15, 5))
    plt.plot(dataframe.iloc[:, 0], dataframe.iloc[:, 1], label='Data')
    plt.xlabel(dataframe.columns[0])
    plt.ylabel(dataframe.columns[1])
    plt.title('Query Results')
    plt.legend()
    plt.show()

    # Step 2: Display data as DataFrame
    logger.info('Step 2: Displaying data as DataFrame...')
    display(dataframe)


@keyword('Execute SQL Query and Plot Results')
def execute_sql_query_and_plot_results(query_file_path, database_config_name):
    """
    Executes SQL query and plots the results as a graph

    :param query_file_path: path to file containing SQL query
    :param database_config_name: name of database configuration in config file
    """
    # Step 1: Get SQL query from file
    logger.info('Step 1: Get SQL query from file...')
    query = get_query_from_file(query_file_path)

    # Step 2: Execute SQL query
    logger.info('Step 2: Execute SQL query...')
    result = execute_query(query, database_config_name)

    # Step 3: Plot data
    logger.info('Step 3: Plot data...')
    plot_data(result)


@keyword("Get DataFrame Columns")
def get_dataframe_columns(dataframe):
    """
    Returns the column names of a pandas dataframe

    :param dataframe: pandas dataframe to get column names from
    :return: list of column names
    """
    logger.info('Step 1: Getting dataframe columns...')
    return dataframe.columns.tolist()

# *** Settings ***
# Library    RFDBUtils.py
#
# *** Variables ***
# ${query_file_path}    path/to/query_file.sql
# ${database_config_name}    config_name_here
#
# *** Test Cases ***
# Execute SQL Query and Plot Results Test
#     ${query}    Get Query From File    ${query_file_path}
#     ${dataframe}    Execute Query    ${query}    ${database_config_name}
#     Plot Data    ${dataframe}
#     ${columns}    Get DataFrame Columns    ${dataframe}
#     Should Contain    ${columns}    column_name_here


# import pandas as pd
# from sqlalchemy import create_engine
# import base64
# import yaml
# import matplotlib.pyplot as plt
# from IPython.display import display
# from robot.api import logger
# from robot.api.deco import keyword
#
#
# @keyword
# def get_query_from_file(file_path):
#     """
#     Reads SQL query from file
#
#     :param file_path: path to file containing SQL query
#     :return: SQL query as a string
#     """
#     logger.info('Step 1: Reading SQL query from file...')
#     with open(file_path, 'r') as file:
#         return file.read()
#
#
# @keyword
# def execute_query(query, database_config_name, query_params=None):
#     """
#     Executes SQL query on specified database configuration using SQLAlchemy
#
#     :param query: SQL query to execute
#     :param database_config_name: name of database configuration in config file
#     :param query_params: optional dictionary of query parameters
#     :return: pandas dataframe containing query results
#     """
#     # Step 1: Load database configuration from config file
#     logger.info('Step 1: Loading database configuration from config file...')
#     with open('config.yaml', 'r') as file:
#         config = yaml.safe_load(file)
#     db_config = config['database_configurations'][database_config_name]
#
#     # Step 2: Connect to database using SQLAlchemy
#     logger.info('Step 2: Connecting to database using SQLAlchemy...')
#     password = base64.b64decode(db_config['password'].encode()).decode()  # decode base64-encoded password
#     engine = create_engine(
#         f"oracle://{db_config['username']}:{password}@{db_config['host']}:{db_config['port']}/{db_config['service_name']}")
#
#     # Step 3: Execute SQL query
#     logger.info('Step 3: Executing SQL query...')
#     if query_params:
#         result = pd.read_sql_query(query, engine, params=query_params)
#     else:
#         result = pd.read_sql_query(query, engine)
#
#     return result
#
#
# @keyword
# def plot_data(dataframe):
#     """
#     Plots query results as a graph and displays them as a dataframe
#
#     :param dataframe: pandas dataframe containing query results
#     """
#     # Step 1: Plot data as graph
#     logger.info('Step 1: Plotting data as graph...')
#     plt.figure(figsize=(15, 5))
#     plt.plot(dataframe.iloc[:, 0], dataframe.iloc[:, 1], label='Data')
#     plt.xlabel(dataframe.columns[0])
#     plt.ylabel(dataframe.columns[1])
#     plt.title('Query Results')
#     plt.legend()
#     plt.show()
#
#     # Step 2: Display data as DataFrame
#     logger.info('Step 2: Displaying data as DataFrame...')
#     display(dataframe)
#
#
# @keyword
# def get_dataframe_columns(dataframe):
#     """
#     Returns the column names of a pandas dataframe
#
#     :param dataframe: pandas dataframe to get column names from
#     :return: list of column names
#     """
#     logger.info('Step 1: Getting dataframe columns...')
#     return dataframe.columns.tolist()
#
#
# @keyword
# def get_file(file_path):
#     """
#     Reads file contents
#
#     :param file_path: path to file
#     :return: file contents as a string
#     """
#     logger.info('Step 1: Reading file contents...')
#     with open(file_path, 'r') as file:
#         return file.read()
