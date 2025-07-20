import sqlite3

def query(db_path):

    tier_query = """
        WITH CustomerSpending AS (
            SELECT 
                Customers.first_name || ', ' || Customers.last_name AS customer_name, 
                coalesce(SUM(Books.price * Orders.quantity),0.00) AS total_spent
            FROM Customers
            LEFT JOIN Orders ON Orders.customer_id=Customers.customer_id
                AND Orders.order_date BETWEEN '2023-10-01' AND '2023-12-31'
            LEFT JOIN Books ON Orders.book_id=Books.book_id
            GROUP BY Customers.customer_id, first_name, last_name
            )
        SELECT CustomerSpending.total_spent, CustomerSpending.customer_name,
            CASE
                WHEN CustomerSpending.total_spent > 20.0 THEN 'Gold'
                WHEN CustomerSpending.total_spent >= 10.0 THEN 'Silver'
                WHEN CustomerSpending.total_spent > 0.0 THEN 'Bronze'
                ELSE 'Inactive'
            END AS customer_tier
        FROM CustomerSpending
        ORDER BY total_spent DESC;
        """
    
    conn = None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(tier_query)

        result = cursor.fetchall()

        print(result)

    except:
        print("something happened")
        return None
    
    finally:
        if conn:
            conn.close()
        

if __name__ == "__main__":
    query_result = query("test.db")
