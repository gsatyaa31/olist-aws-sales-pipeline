import boto3
from dotenv import load_dotenv

load_dotenv()

REGION = "ap-southeast-2"
BUCKET = "olist-pipeline-gsatyaa31"

folders=["raw/", "processed/", "curated/", "rejected/","reports/"]

def get_s3():
    return boto3.client("s3", region_name=REGION)