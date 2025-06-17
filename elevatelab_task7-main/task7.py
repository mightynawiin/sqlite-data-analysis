import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create the database and sales table with sample data
def create_db():
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        quantity INTEGER,
        price REAL
    )
    """)
    
    # Insert sample data (only if table is empty)
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_data = [
            ("Apple", 10, 0.5),
            ("Banana", 20, 0.3),
            ("Orange", 15, 0.4),
            ("Apple", 5, 0.5),
            ("Banana", 10, 0.3),
            ("Orange", 10, 0.4),
            ("Mango", 8, 1.0)
        ]
        cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
        conn.commit()
    
    conn.close()

# Step 2: Connect to DB, run queries and plot results
def analyze_sales():
    conn = sqlite3.connect("sales_data.db")
    
    # Query 1: Total quantity and revenue by product
    query1 = """
    SELECT product, 
           SUM(quantity) AS total_qty, 
           SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product
    """
    
    df1 = pd.read_sql_query(query1, conn)
    print("Sales summary by product:")
    print(df1)
    
    # Plot revenue by product
    df1.plot(kind='bar', x='product', y='revenue', legend=False, title='Revenue by Product')
    plt.ylabel('Revenue ($)')
    plt.tight_layout()
    plt.show()
    
    # Query 2: Total revenue overall
    query2 = "SELECT SUM(quantity * price) AS total_revenue FROM sales"
    total_revenue = pd.read_sql_query(query2, conn).iloc[0, 0]
    print(f"\nTotal revenue across all products: ${total_revenue:.2f}")
    
    conn.close()

if __name__ == "__main__":
    create_db()
    analyze_sales()
