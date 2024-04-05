import psycopg2
import urllib.parse as up
import pandas as pd


class ManageDatabase:

    def __init__(self, df_to_use):
        self.df_to_use = df_to_use

    @staticmethod
    def connection_elephant_db():
        # creating connection to db elephant
        up.uses_netloc.append("postgres")
        DATABASE_URL = 'postgres://fdywwoqg:b8K0s-drWFCB7LaTOondKYSyPjo-WGBM@batyr.db.elephantsql.com/fdywwoqg'
        url = up.urlparse(DATABASE_URL)
        conn = psycopg2.connect(database=url.path[1:],
                                user=url.username,
                                password=url.password,
                                host=url.hostname,
                                port=url.port
                                )
        return conn

    def upload_to_db(self, table_name):
        # Establish a connection to the ElephantSQL database
        conn = self.connection_elephant_db()

        try:
            # Create a cursor object
            cur = conn.cursor()

            # Get the column names and data types from the DataFrame
            column_names = self.df_to_use.columns.tolist()
            data_types = self.df_to_use.dtypes

            # Map Pandas data types to SQL data types
            pandas_sql_types = {
                'object': 'TEXT',  # Assuming object data type as TEXT in PostgreSQL
                'int64': 'INTEGER',
                'float64': 'REAL',
                'datetime64[ns]': 'TIMESTAMP'  # Mapping datetime64[ns] to TIMESTAMP
            }

            # Create a SQL CREATE TABLE statement dynamically
            create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ('
            for col_name, data_type in zip(column_names, data_types):
                sql_data_type = pandas_sql_types.get(str(data_type), 'TEXT')  # Default to TEXT if data type not found
                create_table_query += f'\n    "{col_name}" {sql_data_type},'
            create_table_query = create_table_query.rstrip(',') + '\n);'

            # Execute the CREATE TABLE statement
            cur.execute(create_table_query)

            # Insert data from the DataFrame into the table
            for index, row in self.df_to_use.iterrows():
                placeholders = ', '.join(['%s' for _ in range(len(column_names))])  # Create placeholders for values
                query = f'INSERT INTO {table_name} ({", ".join(column_names)}) VALUES ({placeholders})'
                cur.execute(query, tuple(row))  # Pass the query and row values as parameters

            # Commit the transaction
            conn.commit()

            print(f"Table {table_name} created and data inserted successfully.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the cursor and connection
            cur.close()
            conn.close()

    def query_table(self, table_name):
        conn = self.connection_elephant_db()
        cur = conn.cursor()
        final_df_name = None
        try:
            query = f'SELECT * FROM {table_name}'
            cur.execute(query)
            # Fetch all rows from the result set
            rows = cur.fetchall()
            # Get column names from the cursor description
            columns = [desc[0] for desc in cur.description]
            # Convert rows and columns into DataFrame
            final_df_name = pd.DataFrame(rows, columns=columns)
            return final_df_name
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the cursor and connection
            cur.close()
            conn.close()
