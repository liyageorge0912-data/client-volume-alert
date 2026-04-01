import psycopg2
import random
from datetime import datetime, timedelta
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def insert_clients(cursor):
    clients = [
        "FashionNova UK",
        "HomeDecor Plus",
        "SportGear Direct",
        "BeautyBox London",
        "TechAccessories Co",
        "PetSupplies Hub",
        "KidsWear Boutique",
        "GourmetFood Shop",
        "OutdoorAdventure Ltd",
        "LuxuryWatches UK"
    ]
    
    for client in clients:
        cursor.execute(
            "INSERT INTO clients (client_name) VALUES (%s)",
            (client,)
        )
    
    print(f"Inserted {len(clients)} clients")


def insert_campaigns(cursor):
    campaigns = [
        (1, "Winter Sale"),
        (1, "New Arrivals"),
        (2, "Home Refresh"),
        (2, "Summer Collection"),
        (3, "Sports Event"),
        (4, "Beauty Bundle"),
        (5, "Tech Deals"),
        (6, "Pet Care"),
        (7, "Kids Summer"),
        (8, "Gourmet Box"),
        (9, "Adventure Pack"),
        (10, "Watch Launch")
    ]

    for client_id, campaign_name in campaigns:
        cursor.execute(
            "INSERT INTO campaigns (client_id, campaign_name) VALUES (%s, %s)",
            (client_id, campaign_name)
        )

    print(f"Inserted {len(campaigns)} campaigns")

def insert_targets(cursor):
    today = datetime.today()
    
    client_campaigns = {
        1: [1, 2],
        2: [3, 4],
        3: [5],
        4: [6],
        5: [7],
        6: [8],
        7: [9],
        8: [10],
        9: [11],
        10: [12]
    }
    
    for day_offset in range(30):
        date = today - timedelta(days=day_offset)
        
        for client_id, campaign_ids in client_campaigns.items():
            for campaign_id in campaign_ids:
                
                volume = random.randint(50, 500)
                
                if day_offset == 0 and client_id in [3, 7]:
                    volume = 0
                elif day_offset == 0 and client_id in [5, 9]:
                    volume = random.randint(1, 40)
                
                for customer_num in range(volume):
                    customer_id = f"CUST_{client_id}_{campaign_id}_{day_offset}_{customer_num}"
                    cursor.execute(
                        "INSERT INTO campaign_targets (client_id, campaign_id, customer_id, date_sent) VALUES (%s, %s, %s, %s)",
                        (client_id, campaign_id, customer_id, date.strftime("%Y-%m-%d"))
                    )
        
        print(f"Inserted data for {date.strftime('%Y-%m-%d')}")
    
    print("All target data inserted")

def main():
    print("Connecting to database...")
    conn = connect()
    cursor = conn.cursor()
    print("Connected successfully")
    
    print("Inserting clients...")
    insert_clients(cursor)
    
    print("Inserting campaigns...")
    insert_campaigns(cursor)
    
    print("Inserting campaign targets...")
    insert_targets(cursor)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete")

main()