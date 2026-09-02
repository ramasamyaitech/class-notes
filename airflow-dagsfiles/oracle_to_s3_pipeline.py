from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
from datetime import datetime

import pandas as pd
import boto3
import oracledb

# =====================================================
# ORACLE CONFIGURATION
# =====================================================


ORACLE_HOST = "host.docker.internal"
ORACLE_PORT = 1521
ORACLE_SERVICE = "XEPDB1"

ORACLE_USER = "hr"
ORACLE_PASSWORD = "hr"

# =====================================================
# AWS S3 CONFIGURATION
# =====================================================

BUCKET_NAME = "my-airflow-etl-bucket1"
AWS_REGION = "ap-south-1"

AWS_ACCESS_KEY = "your access key"
AWS_SECRET_KEY = "your secret key"


@dag(
    dag_id="oracle_to_s3_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["oracle", "s3", "etl"],
)
def oracle_to_s3_pipeline():

    @task
    def extract():

        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            host=ORACLE_HOST,
            port=ORACLE_PORT,
            service_name=ORACLE_SERVICE,
        )

        try:
            query = """
                SELECT
                    employee_id,
                    first_name,
                    salary,
                    department_id
                FROM employees
            """

            df = pd.read_sql(query, conn)
            df.columns = df.columns.str.lower()

            print(df.head())

            return df.to_dict(orient="records")

        finally:
            conn.close()

    @task
    def transform(records):

        df = pd.DataFrame(records)

        if df.empty:
            raise ValueError("No data returned from Oracle.")

        df.dropna(inplace=True)

        df["first_name"] = df["first_name"].str.upper()

        df = df[df["salary"] > 20000]

        output_file = "/tmp/employees.csv"

        df.to_csv(output_file, index=False)

        print(df.head())

        return output_file

    @task
    def load(file_name):      

        # Uses environment variables or IAM role automatically
        s3_client = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )

        s3_client.upload_file(
            Filename=file_name,
            Bucket=BUCKET_NAME,
            Key="employees/employees.csv",
        )

        print("Uploaded successfully to S3")

    records = extract()
    csv_file = transform(records)
    load(csv_file)


oracle_to_s3_pipeline()