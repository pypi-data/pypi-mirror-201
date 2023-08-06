## Description

This package contains several functions for interacting with a PostgreSQL database using Python and the Pandas library. Specifically, it includes functions for:

- Loading data from a CSV file to a Pandas dataframe
- Mapping Pandas datatypes to suitable PostgreSQL datatypes
- Creating new tables on a PostgreSQL database
- Inserting data from a Pandas DataFrame into a table in a PostgreSQL database

## Functions

### `csv_to_dataframe(filepath: str) -> pd.DataFrame`

This function reads a CSV file and returns a Pandas DataFrame.

### `get_dtatframe_column_dtypes_dict(dataframe: pd.DataFrame) -> dict`

This function takes a Pandas DataFrame as input and returns a dictionary with the data types of each column.

### `map_pandas_to_postgresql_datatypes(column_datatype_dict: dict) -> dict`

This function maps Pandas datatypes to suitable PostgreSQL datatypes.

### `connect_to_postgresql(**connection_params)`

This function takes keyword arguments containing connection parameters for a PostgreSQL database and returns a database connection object.

### `create_postgresql_table(connection, table_name, field_dict) -> bool`

This function creates a new table with the specified name and fields using the provided database connection.

### `insert_dataframe_into_postgresql(connection, table_name, dataframe) -> None`

This function inserts all values in a Pandas DataFrame into a table in a PostgreSQL database.

## Dependencies

This package requires the following Python libraries:

- `pandas`
- `psycopg2`

It also assumes that a PostgreSQL database is available and that the necessary connection parameters are provided to the `connect_to_postgresql` function.