import sqlite3

#Assuming the db name is eastvantage.db"

conn = sqlite3.connect("eastvantage.db")
curr = conn.cursor()

query = """
SELECT
    c.customer_id AS customer,
    c.age AS age,
    i.item_name AS item,
    SUM(COALESCE(o.quantity, 0)) AS quantity
FROM CUSTOMER c
JOIN SALES s
    ON c.customer_id = s.customer_id
JOIN ORDERS o
    ON s.sales_id = o.sales_id
JOIN ITEMS i
    ON o.item_id = i.item_id
WHERE c.age BETWEEN 18 AND 35
GROUP BY c.customer_id, c.age, i.item_name
HAVING Quantity > 0;
"""

curr.execute(query)
rows = curr.fetchall()

with open("output.csv", "w") as f:
    f.write("Customer;Age;Item;Quantity\n")
    for row in rows:
        f.write(f"{row[0]};{row[1]};{row[2]};{row[3]}\n")

conn.close()

#results are stored in output.csv file 
