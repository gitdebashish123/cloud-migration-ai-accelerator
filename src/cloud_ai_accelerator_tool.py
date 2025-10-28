from langchain_core.prompts import load_prompt
#from langchain.chains import LLMChain
from dotenv import load_dotenv
import streamlit as st
from llm.llm_model import llm

load_dotenv()

# --- Page title ---
st.title("Hive to Iceberg DDL Converter")

# --- Step 1: User Inputs ---
#hive_database = st.text_input("Enter Hive Database Name:")
#hive_table_name = st.text_input("Enter Hive Table Name:")
#hive_table_ddl = st.text_area("Paste Hive Table DDL:", height=300, placeholder="CREATE TABLE ...")


# Streamlit input UI
hive_database = st.selectbox(
    "Select Hive Database Name", 
    ['sales', 'transaction', 'reporting', 'silver', 'bronze']
)

hive_table_name = st.selectbox(
    "Select Hive Table Name",
    ['abc_sales', 'pqr_transaction']
)

hive_table_ddl = st.text_area("Paste Hive Table DDL:", height=300, placeholder="CREATE TABLE ...")


# length_input = st.selectbox(
#     "Top rated",
#     ['2', '5', '10']
# )

# Define the prompt

template = load_prompt("src/prompts/prompt_stores/hive_to_iceberg_ddl_template.json")

# response = llm.invoke("Who is the president of the United States?")
# print(response.content)



# --- Step 4: Run Conversion ---
if st.button("Convert to Iceberg DDL"):
 if hive_database and hive_table_name and hive_table_ddl:
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
            'hive_database': hive_database, 
            'hive_table_name': hive_table_name,
            'hive_table_ddl': hive_table_ddl
        }
    )
    st.write(response.content)
 else:
     st.warning("⚠️ Please fill in all inputs before running the conversion.")