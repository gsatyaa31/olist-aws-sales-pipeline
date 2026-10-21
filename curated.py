import os
import pandas as pd
import boto3
from dotenv import load_dotenv

load_dotenv()

region=os.getenv("AWS_DEFAULT_REGION")
bucket_name=os.getenv("BUCKET_NAME")

s3=boto3.client("s3",region_name=region)

os.makedirs("curated_local",exist_ok=True)

#readin the joined data\
df=pd.read_parquet("processed_local/olist_joined")
df["year"]=df["year"].astype(int)
df["month"]=df["month"].astype(int)
print("rows:",len(df))

#daily sales no of oreders and revenue oer day
df["order_date"]=df["order_purchase_timestamp"].dt.date

daily_sales = (
    df.groupby("order_date")
    .agg(num_orders=("order_id", "nunique"), revenue=("total_amount", "sum"))
    .reset_index()
)
daily_sales["revenue"] = daily_sales["revenue"].round(2)
print(daily_sales.head())

#top 20 products by revenue
top_products = (
    df.groupby(["product_id", "product_category_name"])
    .agg(revenue=("total_amount", "sum"))
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(20)
)
top_products["revenue"]=top_products["revenue"].round(2)
print(top_products.head())

#top customers by total spend
top_customers=(
    df.groupby("customer_unique_id")
    .agg(total_spend=("total_amount","sum"),num_orders=("order_id","nunique"))
    .reset_index()
    .sort_values("total_spend",ascending=False)
    .head(20)
)
print(top_customers.head())

#4 monthly revenue by customer state
monthly_state_revenue=(
    df.groupby(["year","month","customer_state"])
    .agg(revenue=("total_amount","sum"))
    .reset_index()
   
)
print(monthly_state_revenue.head())

#  Check the totals
print("Raw total:", round(df["total_amount"].sum(), 2))
print("Daily total:", round(daily_sales["revenue"].sum(), 2))
print("Monthly/state total:", round(monthly_state_revenue["revenue"].sum(), 2))

#saving data
daily_sales.to_parquet("curated_local/daily_sales.parquet", index=False)
top_products.to_parquet("curated_local/top_products.parquet", index=False)
top_customers.to_parquet("curated_local/top_customers.parquet", index=False)
monthly_state_revenue.to_parquet("curated_local/monthly_state_revenue.parquet", index=False)

#uploading the data
s3.upload_file("curated_local/daily_sales.parquet", bucket_name, "curated/daily_sales.parquet")
s3.upload_file("curated_local/top_products.parquet", bucket_name, "curated/top_products.parquet")
s3.upload_file("curated_local/top_customers.parquet", bucket_name, "curated/top_customers.parquet")
s3.upload_file("curated_local/monthly_state_revenue.parquet", bucket_name, "curated/monthly_state_revenue.parquet")

print("uploaded succesfully!")