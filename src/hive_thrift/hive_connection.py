from hmsclient import hmsclient
from pyhive import hive

# Using Hive Metastore Thrift client
# def list_hive_tables(metastore_host: str, metastore_port: int, database_name: str) -> list:
 
#     client = hmsclient.HMSClient(host=metastore_host, port=metastore_port)
#     client.open()

#     try:
#         tables = client.get_all_tables(db_name=database_name)
#         return tables
#     finally:
#         client.close()

def list_hive_tables(hive_host: str, hive_port: int, database_name: str, username: str = "hive") -> list[str]:
    """
    Connects to HiveServer2 using Thrift and returns a list of tables in the specified database.

    :param hive_host: Hostname or IP of HiveServer2
    :param hive_port: Port number (default 10000)
    :param database_name: Hive database name
    :param username: Hive username (default 'hive')
    :return: List of table names
    """
    conn = hive.Connection(host=hive_host, port=hive_port, username=username, database=database_name, auth="NONE")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def get_exact_hive_ddl(hive_host: str, hive_port: int, database_name: str, table_name: str) -> str:
    """
    Connects to HiveServer2 via Thrift and fetches the exact DDL as Hive stores it.
    """
    # Example connection using Kerberos authentication
    # conn = hive.Connection (
    # host='hive-server.example.com',
    # port=10000,
    # auth='KERBEROS',
    # kerberos_service_name='hive'
    # )
   
    conn = hive.Connection(host=hive_host, port=hive_port, username="hive", database=database_name, auth="NONE")
    cursor = conn.cursor()
    cursor.execute(f"SHOW CREATE TABLE {database_name}.{table_name}")
    ddl = "\n".join([row[0] for row in cursor.fetchall()])
    cursor.close()
    conn.close()
    return ddl


if __name__ == "__main__":
    print("Listing tables in Hive Metastore:")
    #table_list =  list_hive_tables("localhost",9083,"sales_db")
    table_list =  list_hive_tables("localhost",10000,"sales_db","hive")
    table_ddl =  get_exact_hive_ddl("localhost",10000,"sales_db","sales_summary")
    print(table_list)
    print(table_ddl)