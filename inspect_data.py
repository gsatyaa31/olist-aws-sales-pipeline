import pandas as pd

folder="downloaded_raw"

orders = pd.read_csv(f"{folder}/olist_orders_dataset.csv")
customers = pd.read_csv(f"{folder}/olist_customers_dataset.csv")
products = pd.read_csv(f"{folder}/olist_products_dataset.csv")
order_items = pd.read_csv(f"{folder}/olist_order_items_dataset.csv")

print('======ORDERS======')
print(orders.dtypes)
print('duplicates :',orders.duplicated().sum())
print(orders.isnull().sum())

print('=======customers======')
print(customers.dtypes)
print('duplicates :', customers.duplicated().sum())
print(customers.isnull().sum())

print('======products======')
print(products.dtypes)
print('duplicates :',products.duplicated().sum())
print(products.isnull().sum())

print('=====order items======')
print(order_items.dtypes)
print('duplicates :',order_items.duplicated().sum())
print(order_items.isnull().sum())

print('======order status======')
print(orders['order_status'].value_counts())

print('============key duplicates=============')
print('orders order_id : ',orders['order_id'].duplicated().sum())
print('customers customer_id : ',customers['customer_id'].duplicated().sum())
print('products product_id : ',products['product_id'].duplicated().sum())
print('order_items : ',order_items.duplicated(subset=['order_id','order_item_id']).sum())
