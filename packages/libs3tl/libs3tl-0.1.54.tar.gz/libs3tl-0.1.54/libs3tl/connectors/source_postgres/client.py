
import os
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.dialects.postgresql import insert
from urllib.parse import quote_plus as urlquote
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql as pgsql


class PostgresSource:
    """
    Source connector for PostgreSQL database using SQLAlchemy.
    This function is used to initialize a PostgresSource object and is called when creating an instance of this class.
    It takes in a configuration dictionary containing the relevant database information necessary to connect to the Postgres database.
    It instantiates an engine object which is used to interact with the Postgres database and is used throughout the class.

        Configuration parameters in json format:
        - host (string): Hostname or IP address of the database.
        - port (int): Port used by the database.
        - user (string): User to authenticate with.
        - password (string): Password to authenticate with.
        - database (string): Name of the database to use.
        - schema (string): Name of the schema to use.

        creates SQLAlchemy engine using config json object in self.engine
    """

    def __init__(self, config: dict, clientSelf):
        self.metadata = None
        self.dbname = config["dbname"]
        self.table = config["table"]
        self.schema = config["schema"]
        self.clientSelf = clientSelf
        config['encodedPassword'] = self.url_encoded_password(config['password'])
        try:
            self.engine = create_engine(
                "postgresql://{user}:{encodedPassword}@{host}:{port}/{dbname}".format_map(config)
            )
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to instantiates an engine object: {str(e)}")


    def url_encoded_password(self, password):
        return urlquote(password)

    def check(self):
        """
        This check() function is used to check if the database connection is successful.
        It attempts to connect to the database and prints a success message if successful.
        """
        try:
            connection = self.engine.connect()
            connection.close()
            self.clientSelf.logInfo(self.clientSelf.step, 'check connection successful')
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to check connection to the database: {str(e)}")

    def discover(self):
        """
        This discover() function is used to discover the tables in the database.
        It gets a list of all the tables in the database and returns it.
        Returns:
            tables: list of all the tables in the database.
        """
        try:
            # get a list of all the tables in the database
            tables = self.engine.table_names()
            return tables
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to discover the tables in the database: {str(e)}")

    def read(self, query: str = None):
        """
        Read from the connected database.
        The read() method takes an optional query parameter, and executes the query on the connected database.
        If no query is provided, it runs a SELECT * query on the specified table.
        Returns:
            records: list of dictionaries.
        """
        try:
            if not query:
                query = "SELECT * FROM {}.{}".format(self.schema, self.table)
            records = []
            with self.engine.connect() as conn:
                with conn.begin():
                    query_data = conn.execute(query)
                    col_names = [elem[0] for elem in query_data.cursor.description]
                    result = query_data.fetchall()
                    for row in result:
                        records.append(dict(zip(col_names, row)))
                    return records
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to fetch the data: {str(e)}")

    def setup_metadata(self):
        """
        configuring metadata with sqlalchemy engine
        The setup_metadata() method sets up the database engine and creates a MetaData object to store the database information.
        """
        try:
            self.metadata = MetaData(schema=self.schema)
            self.metadata.bind = self.engine
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to setup metadata: {str(e)}")

    def get_table(self):
        """
        This get_table() function is used to get the table object from the database. It sets up the Metadata object and then
        connects to the database. It then creates and returns a Table object using the table name, metadata and
        schema provided in the configuration.
        """
        try:
            self.setup_metadata()
            with self.engine.connect() as conn:
                with conn.begin():
                    return Table(self.table, self.metadata, schema=self.schema, autoload_with=conn)
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to get table details from database: {str(e)}")








