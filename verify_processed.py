import os
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

s3=boto3.client("s3",region_name=os.getenv("AWS_DEFAULT_REGION"))
bucket_name=os.getenv("BUCKET_NAME")

os.makedirs("check_processed",exist_ok=True)
s3.download_file(
    bucket_name, "processed/olist_joined/year=2018/month=9/6fa9bfe07d414fe294d1a59db7417123-0.parquet",
    "check_processed/sample.parquet"
)

df=pd.read_parquet("check_processed/sample.parquet")
print(len(df),"rows")
print(df.dtypes)