from langchain_core.prompts import load_prompt
from dotenv import load_dotenv
import streamlit as st
from llm.llm_model import llm
import streamlit as st
from hive_thrift.HiveClient import HiveClient

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
    #  with st.spinner("Converting... ⏳"):
    #      result = chain.run(
    #          hive_database=hive_database,
    #          hive_table_name=hive_table_name,
    #          hive_table_ddl=hive_table_ddl
    #      )
    #  st.success("✅ Conversion Successful!")
    #  st.code(result, language="sql")
    chain = template | llm
    response = chain.invoke(
        {
            'hive_database': selected_db, 
            'hive_table_name': selected_table,
            'hive_table_ddl': ddl
        }
    )
    st.write(response.content)
 else:
     st.warning("⚠️ Please fill in all inputs before running the conversion.")

if st.button("Close Connection"):
    client.close()
    st.success("Connection closed successfully.")
