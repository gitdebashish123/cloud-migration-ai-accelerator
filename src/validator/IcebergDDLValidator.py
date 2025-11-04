import re

class IcebergDDLValidator:
    """
    Simple rule-based validator for Apache Iceberg CREATE TABLE DDLs.
    """

    def __init__(self, ddl: str):
        self.ddl = ddl.strip()
        self.errors = []
        self.warnings = []

    def validate(self):
        ddl = self.ddl.lower()
        print("Validating DDL:")
        print(ddl)

        # 1. Must start with CREATE TABLE
        if not ddl.startswith("create table"):
            self.errors.append("DDL must start with 'CREATE TABLE'.")

        # 2. Must contain USING iceberg
        if "using iceberg" not in ddl:
            self.errors.append("Missing 'USING iceberg' clause (required for Iceberg tables).")
        
        # Rules will be set as per requirements later

        # # 3. Columns block presence
        # if not re.search(r"\(.*?\)", ddl, re.DOTALL):
        #     self.errors.append("No column definition block found (missing parentheses).")

        # # 4. Check for LOCATION (optional but often used)
        # if "location" not in ddl:
        #     self.warnings.append("No LOCATION clause found — Iceberg tables often specify a storage path.")

        # # 5. Table properties check (recommended)
        # if "tblproperties" not in ddl:
        #     self.warnings.append("No TBLPROPERTIES found — recommended for Iceberg metadata configs.")

        # # 6. Parquet/ORC/Avro storage clauses should NOT appear
        # if any(fmt in ddl for fmt in ["stored as", "row format", "serde"]):
        #     self.errors.append("Invalid Hive-style storage clause found (not supported in Iceberg).")

        # # 7. Check for schema evolution keywords (optional)
        # if "partitioned by" in ddl:
        #     self.warnings.append("Partitioning syntax found — ensure it follows Iceberg’s PARTITIONED BY format.")

        # # 8. Validate semicolon termination
        # if not ddl.endswith(";"):
        #     self.warnings.append("DDL should end with a semicolon ';'.")

        # Final decision
        is_valid = len(self.errors) == 0
        return is_valid
        # return {
        #     "is_valid": is_valid,
        #     "errors": self.errors,
        #     "warnings": self.warnings
        # }

# # --- Example Usage ---
# if __name__ == "__main__":
#     ddl = """
#     CREATE TABLE sales_summary (
#         region STRING,
#         total_sales DOUBLE,
#         year INT
#     )
#     USING iceberg
#     LOCATION 's3://warehouse/sales_summary'
#     TBLPROPERTIES ('format-version'='2');
#     """

#     validator = IcebergDDLValidator(ddl)
#     result = validator.validate()

#     print("✅ Valid:", result["is_valid"])
#     print("❌ Errors:", result["errors"])
#     print("⚠️ Warnings:", result["warnings"])
