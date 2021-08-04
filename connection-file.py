import mariadb 
import sys

try:
    conn = mariadb.connect(
        user="yan2",
        password="yaN21525",
        host="3.109.48.72",
        port= 34768,
        database="final0729d"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


cur.execute( "SELECT * FROM sensorevents")

a = cur.fetchall()

for row in a:
    print(row)
    print("\n")

