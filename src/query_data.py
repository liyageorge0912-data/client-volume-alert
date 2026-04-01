import psycopg2
import pandas as pd
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_daily_volumes():
    conn = connect()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            c.client_name,
            COUNT(ct.customer_id) as volume
        FROM clients c
        LEFT JOIN campaign_targets ct 
            ON c.client_id = ct.client_id
            AND ct.date_sent = CURRENT_DATE
        GROUP BY c.client_name
        ORDER BY volume ASC
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["client_name", "volume"]
    
    cursor.close()
    conn.close()
    
    df = pd.DataFrame(rows, columns=columns)
    return df

if __name__ == "__main__":
    df = get_daily_volumes()
    print(df)