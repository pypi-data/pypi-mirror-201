import os
from sqlalchemy import create_engine, MetaData, Table, inspect
from urllib.parse import quote_plus as urlquote
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql
import pymysql
from sqlalchemy.dialects.mysql import base as mysqltypes

class MySQLDestination:
    """
    Destination connector for MySQL database using SQLAlchemy.
    This function is used to initialize a MySQLDestination object and is called when creating an instance of this class.
    It takes in a configuration dictionary containing the relevant database information necessary to connect to the MySQL database.
    It instantiates an engine object which is used to interact with the MySQL database and is used throughout the class.
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
                "mysql+pymysql://{user}:{encodedPassword}@{host}:{port}/{dbname}".format_map(config)
            )
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to instantiates an engine object: {str(e)}")


    def url_encoded_password(self, password) -> str:
        return urlquote(password)

    def check(self) -> bool:
        """
        This check() function is used to check if the database connection is successful.
        It attempts to connect to the database and prints a success message if successful.
        """
        try:
            connection = self.engine.connect()
            self.clientSelf.logInfo(self.clientSelf.step, 'check connection successful')
            connection.close()
            return True
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to check connection to the database: {str(e)}")
            return False

    def setup_metadata(self) -> bool:
        """
        configuring metadata with sqlalchemy engine
        The setup_metadata() method sets up the database engine and creates a MetaData object to store the database information.
        """
        try:
            self.metadata = MetaData(schema=self.schema)
            self.metadata.bind = self.engine
            return True
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to setup metadata: {str(e)}")
            return True

    def get_table(self) -> Table:
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

    def create_table(self, table) -> bool:
        """
        This function is used to create a new table in the database. It compiles the Table object provided into a SQL
         statement and then executes it in the database.
        """
        try:
            with self.engine.begin() as conn:
                tbl = CreateTable(table, if_not_exists=True)
                sql_stmt = str(
                    tbl.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})) + ';'
                self.clientSelf.logInfo(self.clientSelf.step, sql_stmt)
                conn.execute(sql_stmt)
                return True
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, 'Error in execute DDL query: ' + str(e))
            return False


    def check_table(self) -> bool :
        """
        This function is used to check if the table provided in the configuration exists in the database.
        It uses the inspect method to check if the table exists and returns a boolean value based on the result.
        """
        try:
            result = inspect(self.engine).has_table(self.table, schema=self.schema)
            return result
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Failed to check the tables in the database: {str(e)}")
            return False

    def alter_table(self, table, col_name: list) -> bool:
        """
        This function is used to alter a table in the database. It iterates through the list of columns provided and
        then alters the table to add these columns.
        """
        try:
            with self.engine.begin() as conn:
                DDLCompiler = conn.dialect.ddl_compiler(conn.dialect, None)
                for c in col_name:
                    column = getattr(table.c, c)
                    self.convertToMySQLDataType(column, alter=True)
                    columnSpec = DDLCompiler.get_column_specification(column)
                    sql_stmt = 'ALTER TABLE %s.%s ADD %s;' % (table.schema, table.name, columnSpec)
                    self.clientSelf.logInfo(self.clientSelf.step, str(sql_stmt))
                    conn.execute(sql_stmt)
                    return True
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Error in execute Alter query: {str(e)}")
            return False

    def write(self, table, data) -> bool:
        """
        This function is used to write data to the database. It takes in the table object and a list of dictionaries
         containing the data to be written. It then compiles an insert statement with the table object and data and
         executes it in the database.
        """
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    insert_update_stmt = mysql.insert(table).values(data).on_duplicate_key_update(data)
                    conn.execute(insert_update_stmt)
                    return True
        except Exception as e:
            self.clientSelf.logError(self.clientSelf.step, f"Error while inserting data: {str(e)}")
            return False

    def handleTableDataType(self, table):
        for column in table.c:
            self.convertToMySQLDataType(column)

    def convertToMySQLDataType(self, column, alter=False):
        if alter:
            column.nullable = True

        dataTypeMapping = {'DOUBLE_PRECISION': mysqltypes.DOUBLE(), 'BYTEA': mysqltypes.BLOB(), 'INTERVAL': mysqltypes.VARCHAR(255),
                           'UUID': mysqltypes.VARCHAR(255), 'VARCHAR': mysqltypes.VARCHAR(4000),
                           'JSONB': mysqltypes.VARCHAR(4000), 'BIGINT': mysqltypes.BIGINT()}
        
        if str(column.type) == 'UUID':
            column.server_default = ""
            
        if str(column.type) in dataTypeMapping:
            column.type = dataTypeMapping[str(column.type)]
        
        return column