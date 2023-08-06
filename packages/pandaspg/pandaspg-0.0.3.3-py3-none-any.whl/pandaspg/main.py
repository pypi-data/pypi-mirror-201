import pandas as pd

import psycopg2
from psycopg2.extras import execute_values


def csv_to_dataframe(filepath: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a Pandas DataFrame.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The DataFrame containing the CSV data.
    """
    df = pd.read_csv(filepath)
    return df


def get_dataframe_column_dtypes_dict(dataframe: pd.DataFrame) -> dict:
    """
    This function takes a pandas DataFrame as input and returns a dictionary with the data types of each column.

    Parameters:
    ----------
    dataframe : pandas DataFrame
        The DataFrame to analyze

    Returns:
    -------
    dict
        A dictionary where the keys are the column names and the values are the data types of the corresponding columns.
    """
    dtypes = dataframe.dtypes
    return dict(dtypes)


def map_pandas_to_postgresql_datatypes(column_datatypes_dict: dict) -> dict:
    """
    Maps Pandas datatype to suitable PostgreSQL datatype.

    Args:
        column_datatype_dict (dict): A dictionary containing pandas dataframe column names as its keys
            and their datatype as its values.

    Returns:
        dict: A dictionary mapping the intial keys of the data_types dictionary to their suitable
            PostgresSQL datatype.

    Example:
        >>> data_types = {'id': 'int64', 'name': 'object', 'dob': 'datetime64'}
        >>> map_pandas_to_postgres(data_types)
        {'id': 'INTEGER', 'name': 'TEXT', 'dob': 'TIMESTAMP'}
    """
    mapping = {
        'object': 'TEXT',
        'category': 'TEXT',
        'bool': 'BOOLEAN',
        'uint8': 'SMALLINT',
        'uint16': 'SMALLINT',
        'uint32': 'INTEGER',
        'uint64': 'BIGINT',
        'int8': 'SMALLINT',
        'int16': 'SMALLINT',
        'int32': 'INTEGER',
        'int64': 'BIGINT',
        'float64': 'DOUBLE PRECISION',
        'datetime64[ns]': 'TIMESTAMP',
        'timedelta[ns]': 'INTERVAL',
    }
    return {data_type: mapping[str(dtype)] for data_type, dtype in column_datatypes_dict.items()}


def connect_to_postgresql(**connection_params):
    """
    Connects to a PostgreSQL database using the provided keyword arguments and returns a database connection object.

    Args:
    - **connection_params: keyword arguments containing the connection parameters, such as host, port, database, user, and password

    Returns:
    A psycopg2.extensions.connection object representing the database connection
    """
    conn = psycopg2.connect(**connection_params)
    return conn


def create_postgresql_table(connection, table_name, field_dict) -> bool:
    """
    Creates a new table with the specified name and fields using the provided database connection.

    Args:
    - connection (psycopg2.extensions.connection): a database connection object
    - table_name (str): the name of the table to be created
    - field_dict (dict): a dictionary containing the names of the fields and their corresponding data types

    Returns:
    True if a table was created successfully, False otherwise
    """

    cursor = connection.cursor()

    # Generate the SQL command to create the table
    command = f"CREATE TABLE {table_name} ("

    # Define the primary key field if needed
    if field_dict.get('id') is None:
        command += "id SERIAL PRIMARY KEY, "

    for field, datatype in field_dict.items():
        command += f"{field} {datatype} NULL, "

    # Remove the last comma and space from the command
    command = command[:-2]

    # Close the parentheses and execute the command
    command += ")"

    try:
        cursor.execute(command)
    except Exception as e:
        print(f"Error creating table: {e}")
        return False

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()

    return True


def insert_dataframe_into_postgresql(connection, table_name, dataframe) -> None:
    """
    Inserts all values in a Pandas DataFrame to a table in a PostgreSQL database.

    Args:
    - connection (psycopg2.extensions.connection): The connection to the database.
    - table_name (str): The name of the table to insert the values into.
    - dataframe (pandas.DataFrame): The DataFrame to be inserted.

    Returns:
    None

    Raises:
    Exception: If there is an error during insertion.
    """
    try:
        # Prepare the query
        query = f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES %s"
        values = [tuple(x) for x in dataframe.to_numpy()]

        # Execute the query
        cursor = connection.cursor()
        execute_values(cursor, query, values)
        connection.commit()

        # Close the cursor
        cursor.close()
    except Exception as e:
        raise Exception(f"Error inserting data into PostgreSQL: {str(e)}")
