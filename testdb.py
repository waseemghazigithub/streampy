import pymssql

try:
    conn = pymssql.connect(
        server='182.184.63.27',
        port=1434,
        user='sa',
        password='Maxicom777',
        database='Agriculture Management'
    )
    print("✅ Connected to SQL Server successfully.")
    conn.close()
except Exception as e:
    print("❌ Connection failed.")
    print(e)
