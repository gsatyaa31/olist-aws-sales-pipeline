import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client("s3", region_name=os.getenv("AWS_DEFAULT_REGION"))
bucket_name = os.getenv("BUCKET_NAME")

# good file
s3.upload_file("data/olist_customers_dataset.csv", bucket_name, "raw/olist_customers_dataset.csv")

# bad file (wrong name)
with open("wrong_file.csv", "w") as f:
    f.write("a,b,c\n1,2,3\n")
s3.upload_file("wrong_file.csv", bucket_name, "raw/wrong_file.csv")

print("Both uploaded")