import mariadb 
import sys

try:
    conn = mariadb.connect(
        user="yan2",
        password="yaN21525",
        host="3.109.48.72",
        port=3306,
        database="employees"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)