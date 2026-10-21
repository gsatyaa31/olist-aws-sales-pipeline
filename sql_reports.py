import os 
import pymysql
from dotenv import load_dotenv

load_dotenv()

connection=pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=3306
)
cursor=connection.cursor()

#1 total revenue per month
query1="""
SELECT year,month,ROUND(SUM(revenue),2) AS total_revenue
FROM monthly_state_revenue
GROUP BY year,month
ORDER BY year,month
"""

cursor.execute(query1)
rows=cursor.fetchall()

print("Q1: TOTAL REVENUE PER MONTH ")
for row in rows:
    print(row)

#2 top 5 products by revenue
query2="""
SELECT product_id,product_category_name,revenue
FROM top_products
ORDER BY revenue DESC
LIMIT 5
"""
cursor.execute(query2)
rows=cursor.fetchall()
print("Q2 top 5 products by revenue ")
for row in rows:
    print(row)

#3 top 10 customers by spend 
query3="""
SELECT customer_unique_id,total_spend
FROM top_customers
ORDER BY total_spend DESC
LIMIT 10
"""
cursor.execute(query3)
rows=cursor.fetchall()
print("Q3 top 10 customers by spend ")
for row in rows:
    print(row)

#4 day with the highest sales
query4="""
SELECT order_date,num_orders,revenue
FROM daily_sales
ORDER BY revenue DESC
LIMIT 1
"""
cursor.execute(query4)
rows=cursor.fetchall()
print("Q4 DAY WITH THE HIGHEST SALES ")
for row in rows:
    print(row)

#5 rank states by total revenue
query5="""
SELECT customer_state,ROUND(SUM(revenue),2) AS total_revenue,
RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM monthly_state_revenue
GROUP BY customer_state
ORDER BY revenue_rank
"""
cursor.execute(query5)
rows=cursor.fetchall()
print("Q5 STATES RANKED BY REVENUE")
for row in rows:
    print(row)

    

connection.close()