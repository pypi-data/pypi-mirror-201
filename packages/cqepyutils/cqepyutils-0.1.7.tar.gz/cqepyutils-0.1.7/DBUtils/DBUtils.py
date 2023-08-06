import logging
import pandas as pd
import cx_Oracle
import base64
import yaml
import matplotlib.pyplot as plt
from IPython.display import display


def get_query_from_file(file_path):
    logging.info('Step 1: Reading SQL query from file...')
    with open(file_path, 'r') as file:
        query = file.read()
    return query


def execute_query(query, database_config_name, query_params=None):
    # Step 1: Load database configuration from config file
    logging.info('Step 1: Loading database configuration from config file...')
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    db_config = config['database_configurations'][database_config_name]

    # Step 2: Connect to Oracle database
    logging.info('Step 2: Connecting to Oracle database...')
    password = base64.b64decode(db_config['password'].encode()).decode()  # decode base64-encoded password
    dsn = cx_Oracle.makedsn(db_config['host'], db_config['port'], service_name=db_config['service_name'])
    connection = cx_Oracle.connect(db_config['username'], password, dsn)

    # Step 3: Execute SQL query
    logging.info('Step 3: Executing SQL query...')
    if query_params:
        result = pd.read_sql_query(query, connection, params=query_params)
    else:
        result = pd.read_sql_query(query, connection)

    # Step 4: Close database connection
    logging.info('Step 4: Closing database connection...')
    connection.close()

    return result


def plot_data(dataframe):
    # Step 1: Plot data as graph
    logging.info('Step 1: Plotting data as graph...')
    plt.figure(figsize=(15, 5))
    plt.plot(dataframe.iloc[:, 0], dataframe.iloc[:, 1], label='Data')
    plt.xlabel(dataframe.columns[0])
    plt.ylabel(dataframe.columns[1])
    plt.title('Query Results')
    plt.legend()
    plt.show()

    # Step 2: Display data as DataFrame
    logging.info('Step 2: Displaying data as DataFrame...')
    display(dataframe)

# if __name__ == '__main__':
#     # Configure logger
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
#
#     # Step 1: Read SQL query from file
#     query_file_path = 'query.sql'
#     query = get_query_from_file(query_file_path)
#
#     # Step 2: Execute SQL query
#     logging.info('Step 2: SQL query read successfully!')
#     database_config_name = 'dev'
#     result = execute_query(query, database_config_name)
#
#     # Step 3: Plot query results
#     logging.info('Step 3: Plotting query results...')
#     plot_data(result)
#
#
# database_configurations:
#   dev:
#     host: your_host_name
#     port: your_port_number
#     service_name: your_service_name
#     username: your_username
#     password: your_base64_encoded_password
# test
