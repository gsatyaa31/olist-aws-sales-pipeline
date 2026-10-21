import os
from config import BUCKET,get_s3

s3=get_s3()

DATA_DIR = "data"
FILES = [
    "olist_orders_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_items_dataset.csv",
]

for name in FILES:
    local_path=os.path.join(DATA_DIR, name)
    key= f"raw/{name}"

    if not os.path.exists(local_path):
        print(f"missing locally: {local_path}")
        continue

    s3.upload_file(local_path, BUCKET, key)
    print(f"uploaded {local_path} to s3://{BUCKET}/{key}")