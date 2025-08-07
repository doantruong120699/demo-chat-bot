import os
import psycopg2
import pandas as pd
from psycopg2 import OperationalError

def connect_to_db():
    """
    Connects to the PostgreSQL database using environment variables.
    Sets the search_path to 'public' so you can query tables without prefixing with 'public.'.
    Returns a connection object.
    Raises OperationalError if connection fails.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

        with conn.cursor() as cur:
            cur.execute("SET search_path TO public;")
        return conn

    except OperationalError as e:
        print("❌ Failed to connect to the PostgreSQL database.")
        print(f"Error: {e}")
        raise

def execute_sql_query(conn, query):
    """Execute SQL query and return results as DataFrame."""
    try:
        with conn.cursor() as cur:
            cur.execute("SET search_path TO public;")
        results = pd.read_sql(query, conn)
        return results
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None


def get_database_schema(conn):
    """Get schema information for the PostgreSQL database tables."""
    schema_info = {}

    try:
        # Get list of tables in the public schema
        tables_query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """
        tables = pd.read_sql(tables_query, conn)
        table_names = tables['table_name'].tolist()

        # Get schema for each table
        for table in table_names:
            columns_query = f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table}'
                AND table_schema = 'public';
            """
            columns = pd.read_sql(columns_query, conn)
            schema_info[table] = columns.to_dict('records')

            # Get a few sample rows to understand the data
            sample_query = f'SELECT * FROM "{table}" LIMIT 3'
            samples = pd.read_sql(sample_query, conn)
            schema_info[f"{table}_samples"] = samples.to_dict('records')

        return schema_info
    except Exception as e:
        print(f"Error getting schema information: {e}")
        return {"error": str(e)}

def get_table_schema(conn, table_name):
    """
    Retrieves the schema of a specific table from the connection.
    Returns a list of column names.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
    return [row[0] for row in cursor.fetchall()]
