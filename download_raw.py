import os
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_DEFAULT_REGION")
bucket_name = os.getenv("BUCKET_NAME")

s3 = boto3.client("s3", region_name=region)

folder = "downloaded_raw"
os.makedirs(folder, exist_ok=True)

files = [
    "olist_orders_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_items_dataset.csv",
]

for name in files:
    s3.download_file(bucket_name, f"raw/{name}", f"{folder}/{name}")
    print("downloaded", name)

orders = pd.read_csv(f"{folder}/olist_orders_dataset.csv")
customers = pd.read_csv(f"{folder}/olist_customers_dataset.csv")
products = pd.read_csv(f"{folder}/olist_products_dataset.csv")
order_items = pd.read_csv(f"{folder}/olist_order_items_dataset.csv")

print("orders rows:", len(orders))
print("customer rows:", len(customers))
print("products rows:", len(products))
print("order items rows:", len(order_items))