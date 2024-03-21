import requests 
import psycopg2
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
import os 

load_dotenv()


database_config = {
        "database": os.environ.get('database'),
        "user": os.environ.get('user'),
        "password": os.environ.get('sql_password'),
        "host": os.environ.get('host'),
        "port": "5432"  # Default PostgreSQL port
    }

def get_json_latest():
  response = requests.get(url="https://api.coindesk.com/v1/bpi/currentprice.json").json()
  recent_update = response['time']['updatedISO']
  price = response['bpi']['GBP']['rate_float']
  return recent_update, price


def sql_get_latest_update_date():
    try:
        with psycopg2.connect(**database_config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT MAX(date_time)  
                    FROM lc_example_price
                """)

                result = cur.fetchone()
                if result[0]:
                    return result[0]
                else:
                    return None

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        return None

def update_table(new_date, new_price):
    try:
        with psycopg2.connect(**database_config) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    insert into lc_example_price
                    Values('{new_date}', {new_price})                    
                """)

                conn.commit()  # Commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)

sql_date = sql_get_latest_update_date()
ts, amount = get_json_latest()
ts = datetime.fromisoformat(ts)
ts = ts.replace(tzinfo=None)

if ts - sql_date > timedelta(minutes=1):
  update_table(ts.strftime("%Y-%m-%d %H:%M:%S"), amount)
