import pymssql

try:
    conn = pymssql.connect(
        server='111.111.63.27',
        port=1434,
        user='sa',
        password='Max',
        database='Agriculture Management'
    )
    print("✅ Connected to SQL Server successfully.")
    conn.close()
except Exception as e:
    print("❌ Connection failed.")
    print(e)
