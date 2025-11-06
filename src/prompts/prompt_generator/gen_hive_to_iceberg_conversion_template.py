from langchain_core.prompts import PromptTemplate   


template = PromptTemplate(
    template="""
You are an expert data engineer specializing in Apache Hive, Apache Iceberg.

Your task is to convert a given Hive table DDL into an equivalent Iceberg table DDL.

### Input:
- Hive Database: {hive_database}
- Hive Table Name: {hive_table_name}
- Hive Table DDL:
{hive_table_ddl}

### Conversion Rules:
1. Convert the Hive DDL syntax into Apache Iceberg DDL syntax.
2. Preserve all column names, data types, and comments.
3. Map Hive table properties to Iceberg-compatible ones (e.g., remove `STORED AS`, `ROW FORMAT`, and use Iceberg-specific `TABLE PROPERTIES`).
4. Use the `USING iceberg` clause for the table format.
5. Use the AWS S3 location syntax: `LOCATION 's3://<your-bucket>/<path>/'`.
6. Include typical Iceberg table properties like:

TBLPROPERTIES (
'table_type'='ICEBERG',
'format-version'='2',
'write.format.default'='parquet'
)

7. If partitions exist, include `PARTITIONED BY (...)` as in the original table.
8. Output only the final Iceberg DDL without explanations.
9. Follow the indentation and formatting conventions of output DDL as input DDL.
   9.1 Each column definition should be on a new line.
   9.2 The opening parenthesis for column definitions should be on the same line as `CREATE TABLE`.
   9.3 The closing parenthesis should be on a new line after the last column definition.
   9.4 Keywords should be in uppercase (e.g., CREATE TABLE, PARTITIONED BY).
   9.5 Use single quotes for string literals in LOCATION and TBLPROPERTIES.
10. Maintain spacing and line breaks for readability.
11. Ensure the final DDL is syntactically correct for Iceberg.
12. Ensure spaces between keywords and identifiers are consistent.
### Output:
A valid Iceberg table DDL ready to run in AWS.

""",
    input_variables=['hive_database','hive_table_name','hive_table_ddl'],
    validate_template=False
     )

template.save("src/prompts/prompt_stores/hive_to_iceberg_ddl_template.json")