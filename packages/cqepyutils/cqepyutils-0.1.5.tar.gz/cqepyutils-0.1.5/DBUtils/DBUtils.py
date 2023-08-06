import cx_Oracle
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def fetch_query(file_path):
    """
    Reads an SQL query from a file.

    Parameters:
    file_path (str): The path to the SQL file to read.

    Returns:
    str: The SQL query as a string.
    """
    # Set up logging
    logger.info("Reading SQL query from file...")

    # Read the SQL query from the file
    with open(file_path, 'r') as f:
        query = f.read()

    # Return the SQL query as a string
    logger.info("SQL query read successfully!")
    return query


def execute_query(query, connection_details):
    """
    Connects to an Oracle database and executes an SQL query.
    Returns the query results as a pandas DataFrame.

    Parameters:
    query (str): The SQL query to execute.
    connection_details (str): The connection details to use to connect to the Oracle database.
                              This should be in the format '<username>/<password>@<hostname>:<port>/<service_name>'.

    Returns:
    pandas.DataFrame: The query results as a pandas DataFrame.
    """
    # Set up logging
    logger.info("Connecting to Oracle database...")

    # Connect to the Oracle database
    try:
        connection = cx_Oracle.connect(connection_details)
    except cx_Oracle.DatabaseError as e:
        logger.error("Error connecting to database: %s", e)
        raise

    # Execute the SQL query and fetch the results into a DataFrame
    logger.info("Executing SQL query...")
    try:
        df = pd.read_sql(query, connection)
    except cx_Oracle.DatabaseError as e:
        logger.error("Error executing SQL query: %s", e)
        raise

    # Close the database connection
    logger.info("Closing database connection...")
    connection.close()

    # Return the query results as a DataFrame
    logger.info("Query executed successfully!")
    return df
