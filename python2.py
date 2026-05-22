import mysql.connector
import pandas as pd
import numpy as np

conn = mysql.connector.connect(
    host="35.199.115.174",
    user="looqbox-challenge",
    password="looq-challenge"
)

cursor = conn.cursor()
cursor.execute("USE `looqbox-challenge`")

# ----------------------------------------------------------------------------------------------------------------------------
# QUERY 1 -> STORE_NAME
# ----------------------------------------------------------------------------------------------------------------------------
q1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

df_stores = pd.read_sql(q1, conn)

# ----------------------------------------------------------------------------------------------------------------------------
# QUERY 2 -> SALES
# ----------------------------------------------------------------------------------------------------------------------------
q2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

df_sales = pd.read_sql(q2, conn)

conn.close()


df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])

df_sales = df_sales[
    (df_sales["DATE"] >= "2019-10-01") &
    (df_sales["DATE"] <= "2019-12-31")
]


df = df_sales.merge(df_stores, on="STORE_CODE", how="left")

df_grouped = df.groupby(["STORE_NAME", "BUSINESS_NAME"]).agg(
    total_sales=("SALES_VALUE", "sum"),
    total_qty=("SALES_QTY", "sum")
).reset_index()

df_grouped["TM"] = np.round(df_grouped["total_sales"] / df_grouped["total_qty"],2)

final_df = df_grouped[[
    "STORE_NAME",
    "BUSINESS_NAME",
    "TM"
]]

final_df.columns = ["Loja", "Categoria", "TM"]

final_df = final_df.sort_values(by="Loja", ascending=True)

print(final_df)