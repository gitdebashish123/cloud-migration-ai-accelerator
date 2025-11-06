import boto3
import time
from dotenv import load_dotenv

load_dotenv()
# athena = boto3.client("athena", region_name="ap-south-1")
athena = boto3.client("athena")
CATALOG = "AwsDataCatalog" #When you use Athena, by default it queries tables from your Glue Data Catalog through AwsDataCatalog
DATABASE = "cust_db"
OUTPUT = "s3://aws-athena-query-results-20250730/"
TABLE_PATH = "s3://aws-glue-demo-20250730/data-store/demo_csv_reports_iceberg_4"

query = f"""
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
  industry_code_anzsic06 string)
LOCATION '{TABLE_PATH}'
TBLPROPERTIES (
  'table_type'='iceberg',
  'compression_level'='3',
  'write_compression'='ZSTD',
  'format'='PARQUET'
);
"""

# Run query
response = athena.start_query_execution(
    QueryString=query,
    QueryExecutionContext={'Database': DATABASE},
    ResultConfiguration={'OutputLocation': OUTPUT}
)

# Get query execution id
query_execution_id = response['QueryExecutionId']

# Wait for query to complete
while True:
    query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
    status = query_status['QueryExecution']['Status']['State']

    if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break

    print(f"Query status: {status}. Waiting...")
    time.sleep(5)

if status == 'SUCCEEDED':
    print("Iceberg table created successfully!")
else:
    print(f"Query failed or was cancelled with status: {status}")
