# hive_client.py
from pyhive import hive

class HiveClient:
    def __init__(self, host: str, port: int, username: str = "hive", database: str = "default"):
        self.host = host
        self.port = port
        self.username = username
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a single HiveServer2 connection."""
        self.conn = hive.Connection(
            host=self.host,
            port=self.port,
            username=self.username,
            database=self.database,
            auth="NONE"
        )
        self.cursor = self.conn.cursor()

    def list_tables(self) -> list[str]:
        """List all tables in the current database."""
        self.cursor.execute("SHOW TABLES")
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_ddl(self, table_name: str) -> str:
        """Fetch the exact DDL for a given table."""
        self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
        ddl = "\n".join([row[0] for row in self.cursor.fetchall()])
        return ddl

    def close(self):
        """Close the Hive connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
