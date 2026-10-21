import os
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_DEFAULT_REGION")
bucket_name = os.getenv("BUCKET_NAME")

s3 = boto3.client("s3", region_name=region)

os.makedirs("reports_local", exist_ok=True)

folder = "downloaded_raw"

# Read the 4 raw files
orders = pd.read_csv(f"{folder}/olist_orders_dataset.csv")
customers = pd.read_csv(f"{folder}/olist_customers_dataset.csv")
products = pd.read_csv(f"{folder}/olist_products_dataset.csv")
order_items = pd.read_csv(f"{folder}/olist_order_items_dataset.csv")

# Put them in one dictionary so we can loop
datasets = {
    "orders": orders,
    "customers": customers,
    "products": products,
    "order_items": order_items,
}

# Build one row per dataset
report_rows = []

for name, df in datasets.items():
    rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    null_cells = int(df.isnull().sum().sum())
    total_cells = rows * len(df.columns)
    null_percentage = round(null_cells / total_cells * 100, 2)

    report_rows.append({
        "dataset": name,
        "rows": rows,
        "duplicate_rows": duplicate_rows,
        "null_cells": null_cells,
        "null_percentage": null_percentage,
    })

# Adding the final cleaned dataset (row count only)
cleaned = pd.read_parquet("processed_local/olist_joined")
report_rows.append({
    "dataset": "final_cleaned_joined",
    "rows": len(cleaned),
    "duplicate_rows": "",
    "null_cells": "",
    "null_percentage": "",
})

report = pd.DataFrame(report_rows)
print(report)

# Save and upload
report.to_csv("reports_local/data_quality_report.csv", index=False)
s3.upload_file("reports_local/data_quality_report.csv", bucket_name, "reports/data_quality_report.csv")

print("Report uploaded to reports/")