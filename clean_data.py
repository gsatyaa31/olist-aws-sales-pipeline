import pandas as pd

folder="downloaded_raw"

orders = pd.read_csv(f"{folder}/olist_orders_dataset.csv")
customers = pd.read_csv(f"{folder}/olist_customers_dataset.csv")
products = pd.read_csv(f"{folder}/olist_products_dataset.csv")
order_items = pd.read_csv(f"{folder}/olist_order_items_dataset.csv")

#1 removing the duplicates
orders = orders.drop_duplicates()
customers = customers.drop_duplicates()
products = products.drop_duplicates()
order_items = order_items.drop_duplicates()

#2 handling the nulls
products['product_category_name']=products['product_category_name'].fillna('unknown')

#3 changing the data types
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"])
orders["order_delivered_carrier_date"] = pd.to_datetime(orders["order_delivered_carrier_date"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])
order_items["shipping_limit_date"] = pd.to_datetime(order_items["shipping_limit_date"])
order_items["price"]=order_items["price"].astype(float)
order_items["freight_value"]=order_items["freight_value"].astype(float)

#4 removing the cancelled orders
print("orders before : ", len(orders))
orders=orders[orders["order_status"]!="canceled"]
print("orders after : ", len(orders))

print(orders.dtypes)

cancelled_ids= pd.read_csv(f"{folder}/olist_orders_dataset.csv")
cancelled_ids=cancelled_ids[cancelled_ids["order_status"]=="cancelled"]["order_id"]

print("itms in cancelled orders: ",order_items["order_id"].isin(cancelled_ids).sum())

print("Distinct orders in order_items:", order_items["order_id"].nunique())