import streamlit as st
from hive_thrift.HiveClient import HiveClient

# --- Initialize the Hive client ---
@st.cache_resource
def get_hive_client():
    client = HiveClient(host="localhost", port=10000, username="hive")
    client.connect()
    return client

# --- Fetch databases ---
#@st.cache_data
def fetch_databases(client: HiveClient):
    client.cursor.execute("SHOW DATABASES")
    return [row[0] for row in client.cursor.fetchall()]

# --- Fetch tables for a selected database ---
#@st.cache_data
def fetch_tables(client: HiveClient, database: str):
    client.cursor.execute(f"USE {database}")
    client.cursor.execute("SHOW TABLES")
    return [row[0] for row in client.cursor.fetchall()]

# --- Streamlit UI ---
st.title("🔍 Hive Database Explorer")

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

# Optional close button
if st.button("Close Connection"):
    client.close()
    st.success("Connection closed successfully.")
