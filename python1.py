import mysql.connector
import pandas as pd
from datetime import datetime

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def retrieve_data(product_code:int, store_code:int, date:list):

    if not isinstance(date, list) or len(date) != 2:
        raise ValueError("date must be a list with [start_date, end_date]")
    

    start_date, end_date = date
    if start_date > end_date:
        raise ValueError("start_date must be <= end_date")
    
    if not validate_date(start_date) or not validate_date(end_date):
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    #conectar com o banco de dados
    try:
        conn = mysql.connector.connect(
            host="35.199.115.174",
            user="looqbox-challenge",
            password="looq-challenge"
        )
        cursor = conn.cursor()
        cursor.execute("USE `looqbox-challenge`")
        """
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")

        for db in cursor:
            print(db)
        """
        
        

        query = """
            SELECT *
            FROM data_product_sales
            WHERE PRODUCT_CODE = %s
            AND STORE_CODE = %s
            AND DATE BETWEEN %s AND %s
        """

        params = (product_code, store_code, start_date, end_date)

        df = pd.read_sql(query,conn,params=params)

        conn.close()
        return df

    finally:
        if conn:
            conn.close()

PRODUCT_CODE = 18
STORE_CODE = 1
START_DATE = '2019-01-01'
END_DATE = '2019-01-31'

my_data = retrieve_data(
    product_code=PRODUCT_CODE,
    store_code=STORE_CODE,
    date=[START_DATE, END_DATE]
)

print(my_data.head(10))