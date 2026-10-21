import os
import boto3
from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_DEFAULT_REGION")
bucket_name = os.getenv("BUCKET_NAME")

s3 = boto3.client("s3", region_name=region)

local_folder = "processed_local/olist_joined"
count = 0

for root, dirs, files in os.walk(local_folder):
    for file in files:
        # skip Spark helper files (none expected with PyArrow, but harmless)
        if file.endswith(".crc") or file == "_SUCCESS":
            continue

        local_path = os.path.join(root, file)

        # processed_local\olist_joined\year=2017\month=5\x.parquet
        #   -> olist_joined/year=2017/month=5/x.parquet
        relative = os.path.relpath(local_path, "processed_local").replace("\\", "/")

        # final S3 key
        key = f"processed/{relative}"

        s3.upload_file(local_path, bucket_name, key)
        count += 1
        print("Uploaded", key)

print("Total files uploaded:", count)