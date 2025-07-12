import Pyro5.api
from db_connection import connect_db

@Pyro5.api.expose
class PITDServer:
    def __init__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tax_data (
                tfn TEXT,
                income REAL,
                withheld REAL
            )
        """)
        self.conn.commit()

    def get_tax_records(self, tfn):
        self.cursor.execute("SELECT income, withheld FROM tax_data WHERE tfn = %s", (tfn,))
        return self.cursor.fetchall()

    def add_tax_record(self, tfn, income, withheld):
        self.cursor.execute(
            "INSERT INTO tax_data (tfn, income, withheld) VALUES (%s, %s, %s)",
            (tfn, income, withheld)
        )
        self.conn.commit()


def main():
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(PITDServer)
    print("Server 2 (PITD) running. URI:", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()