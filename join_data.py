import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("olist_join").master("local[*]").getOrCreate()

folder = "downloaded_raw"
output_folder = "processed_local/olist_joined"

# 1. Read the raw files
orders = spark.read.csv(f"{folder}/olist_orders_dataset.csv", header=True, inferSchema=True)
customers = spark.read.csv(f"{folder}/olist_customers_dataset.csv", header=True, inferSchema=True)
products = spark.read.csv(f"{folder}/olist_products_dataset.csv", header=True, inferSchema=True)
order_items = spark.read.csv(f"{folder}/olist_order_items_dataset.csv", header=True, inferSchema=True)

# 2. Remove duplicates
orders = orders.drop_duplicates()
customers = customers.drop_duplicates()
products = products.drop_duplicates()
order_items = order_items.drop_duplicates()

# 3. Handle nulls
products = products.fillna({"product_category_name": "unknown"})

# 4. Convert data types
orders = orders.withColumn("order_purchase_timestamp", f.to_timestamp("order_purchase_timestamp"))
order_items = order_items.withColumn("price", f.col("price").cast("double"))
order_items = order_items.withColumn("freight_value", f.col("freight_value").cast("double"))

# 5. Remove cancelled orders (keep a copy for the reconciliation check)
all_orders = orders
orders = orders.filter(f.col("order_status") != "canceled")

# 6. Join: items + orders + customers + products
df = order_items.join(orders, on="order_id", how="inner")
df = df.join(customers, on="customer_id", how="inner")
df = df.join(products, on="product_id", how="left")

# 7. New columns
df = df.withColumn("total_amount", f.round(f.col("price") + f.col("freight_value"), 2))
df = df.withColumn("year", f.year("order_purchase_timestamp"))
df = df.withColumn("month", f.month("order_purchase_timestamp"))

# 8. Reconciliation
cancelled = all_orders.filter(f.col("order_status") == "canceled")
print("order_items rows:", order_items.count())
print("rows after joining the data:", df.count())
print("items in cancelled orders:", order_items.join(cancelled, on="order_id", how="inner").count())

df.select("order_id", "product_id", "customer_state", "price",
          "freight_value", "total_amount", "year", "month").show(5)

# 9. Save as Parquet, partitioned by year and month (PyArrow, no winutils needed)
pdf = df.toPandas()
os.makedirs("processed_local", exist_ok=True)
pdf.to_parquet(output_folder, partition_cols=["year", "month"], index=False)
print("Parquet written:", len(pdf), "rows")

spark.stop()