import sqlite3
import pandas as pd

#Assuming the db name is eastvantage.db"
conn = sqlite3.connect("eastvantage.db")

df = pd.read_sql("""
SELECT
    c.customer_id,
    c.age,
    i.item_name,
    o.quantity
FROM CUSTOMER c
JOIN SALES s
    ON c.customer_id = s.customer_id
JOIN ORDERS o
    ON s.sales_id = o.sales_id
JOIN ITEMS i
    ON o.item_id = i.item_id
WHERE c.age BETWEEN 18 AND 35
""", conn)

df["quantity"] = df["quantity"].fillna(0)

output_df = df.groupby(["customer_id", "age", "item_name"])["quantity"].sum().reset_index()
output_df = output_df[output_df["quantity"] > 0]
output_df.columns = ["Customer", "Age", "Item", "Quantity"]

output_df.to_csv("output.csv", sep=";", index=False)

conn.close()
