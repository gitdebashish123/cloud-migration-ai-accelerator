from langchain_core.prompts import load_prompt
from dotenv import load_dotenv
import streamlit as st
from llm.llm_model import llm
import streamlit as st
from hive_thrift.HiveClient import HiveClient
from validator.IcebergDDLValidator import IcebergDDLValidator
import boto3
import time

athena = boto3.client("athena")

# --- Initialize the Hive client ---
@st.cache_resource
def get_hive_client():
    client = HiveClient(host="localhost", port=10000, username="hive")
    client.connect()
    return client
# --- Fetch databases ---
def fetch_databases(client: HiveClient):
    client.cursor.execute("SHOW DATABASES")
    return [row[0] for row in client.cursor.fetchall()]

# --- Fetch tables for a selected database ---
def fetch_tables(client: HiveClient, database: str):
    client.cursor.execute(f"USE {database}")
    client.cursor.execute("SHOW TABLES")
    return [row[0] for row in client.cursor.fetchall()]

# --- Validate Iceberg DDL ---
def validate_iceberg_ddl(ddl: str):
    validate = IcebergDDLValidator(ddl)
    status = validate.validate()
    return status

# --- Create Iceberg DDL ---
def execute_athena_ddl(ddl: str):
    # Currently values are hard-coded . It can be generalised once
    # all steps are finalised
    # In Athena, the SQL syntax for Iceberg does not use 'USING iceberg'

    # Athena/Glue configuration
    CATALOG = "AwsDataCatalog"  # Default Glue catalog in Athena
    DATABASE = "cust_db"
    OUTPUT = "s3://aws-athena-query-results-20250730/"
    TABLE_PATH = "s3://aws-glue-demo-20250730/data-store/demo_csv_reports_iceberg_4"

    # Hard coded DDL query
    
    ddl = f"""
    CREATE TABLE {CATALOG}.{DATABASE}.demo_csv_reports_iceberg_4 (
        year bigint,
        industry_aggregation_nzsioc string,
        industry_code_nzsioc string,
        industry_name_nzsioc string,
        units string,
        variable_code string,
        variable_name string,
        variable_category string,
        value string,
        industry_code_anzsic06 string
    )
    LOCATION '{TABLE_PATH}'
    TBLPROPERTIES (
        'table_type'='iceberg',
        'compression_level'='3',
        'write_compression'='ZSTD',
        'format'='PARQUET'
    );
    """

    # Start query execution
    response = athena.start_query_execution(
        QueryString=ddl,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT}
    )

    # Get query execution ID
    query_execution_id = response['QueryExecutionId']

    # Wait for query to complete
    while True:
        query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        status = query_status['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

        print(f"Query status: {status}. Waiting...")
        time.sleep(5)

    print(f"Query finished with status: {status}")
    return status == 'SUCCEEDED'

# --- Streamlit UI ---
st.title("🔍 Hive to Iceberg DDL Converter")

# Connect to HiveServer2
client = get_hive_client()

# Step 1: Select Hive Database
hive_databases = fetch_databases(client)
selected_db = st.selectbox("Select a Hive Database:", hive_databases)

# Step 2: Once DB is selected, fetch its tables
if selected_db:
    hive_tables = fetch_tables(client, selected_db)
    st.write(f"✅ Found {len(hive_tables)} tables in `{selected_db}` database.")

    # Dropdown for single table selection
    selected_table = st.selectbox("Select a Table (Dropdown):", hive_tables)
    # # Checkbox list for multiple selection
    # selected_tables_checkbox = st.multiselect("Or select multiple tables (Checkbox):", hive_tables)

    # Step 3: Display selected table DDL (optional)
    if selected_table:
        ddl = client.get_table_ddl(selected_table)
        st.code(ddl, language="sql")

template = load_prompt("src/prompts/prompt_stores/hive_to_iceberg_ddl_template.json")

if st.button("Convert to Iceberg DDL"):
 if selected_db and selected_table and ddl:
     chain = template | llm
     with st.spinner("Converting... ⏳"):
         response = chain.invoke(
             {'hive_database': selected_db,
             'hive_table_name': selected_table,
             'hive_table_ddl': ddl
             }
         )
        #  result = chain.invoke(
        #      'hive_database': selected_db,
        #      'hive_table_name': selected_table,
        #      'hive_table_ddl': ddl
        #  )
     st.success("✅ Conversion Successful!")
     result = response.content
     #result_ddl = str(result.strip())
     st.session_state['result_ddl'] = response.content
     st.code(result, language="sql")
    # chain = template | llm
    # response = chain.invoke(
    #     {
    #         'hive_database': selected_db, 
    #         'hive_table_name': selected_table,
    #         'hive_table_ddl': ddl
    #     }
    # )
    # st.write(response.content)
 else:
     st.warning("⚠️ Please fill in all inputs before running the conversion.")

# if st.button("Validate Iceberg DDL"):
#     if validate_iceberg_ddl(result_ddl): # Replace result_ddl with the actual DDL string to validate
#     # if True:
#         st.success("The generated DDL is a valid Iceberg DDL.")     
#     else:
#         st.error("⚠️ The generated DDL is NOT a valid Iceberg DDL.")


# --- Validate Iceberg DDL button ---
if 'ddl_valid' in st.session_state:
    if st.session_state['ddl_valid']:
        st.success("✅ The generated DDL is a valid Iceberg DDL.")

        # --- Place buttons side by side ---
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Create DDL in Athena"):
                with st.spinner("Executing DDL in Athena... ⏳"):
                    query_status = execute_athena_ddl(st.session_state['result_ddl'])
                    if query_status:
                        st.success(f"✅ DDL submitted! Execution Status: {query_status}")
                    else:
                        st.warning("⚠️ DDL Execution failed")

        with col2:
            if st.button("Save DDL to S3 / Local"):
                st.info("💾 Placeholder: Save the DDL to S3 or local storage.")

        with col3:
            # --- Drop & Create with strict confirmation ---
            if st.button("Drop & Create DDL in Athena"):
                st.warning("⚠️ This will DROP the existing table and CREATE a new one!")
                user_input = st.text_input(
                    "Type 'CONFIRM' to allow dropping and recreating the table:", ""
                )

                if user_input == "CONFIRM":
                    with st.spinner("Dropping and creating table in Athena... ⏳"):
                        # Execute drop and create safely
                        # drop_query = f"DROP TABLE IF EXISTS cust_db.demo_csv_reports_iceberg_4"
                        # create_query = st.session_state['result_ddl']

                        # drop_status = execute_athena_ddl(drop_query)
                        # create_status = execute_athena_ddl(create_query)

                        # if drop_status and create_status:
                        #     st.success("✅ Table dropped and recreated successfully!")
                        # else:
                        #     st.warning("⚠️ Something went wrong during drop/create.")
                        st.info("💾 Placeholder: Dropping and creating table in Athena.")
                elif user_input:
                    st.error("❌ Confirmation text did not match. Action canceled.")

    else:
        st.error("⚠️ The generated DDL is NOT a valid Iceberg DDL.")

# if st.button("Close Connection"):
#     client.close()
#     st.success("Connection closed successfully.")
