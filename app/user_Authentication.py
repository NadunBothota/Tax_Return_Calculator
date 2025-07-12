import getpass
from db_connection import connect_db

def register_user():
    conn = connect_db()
    cur = conn.cursor()
    username = input("Enter new username: ").strip()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        print("Username already exists.")
        cur.close()
        conn.close()
        return False
    password = input("Enter new password: ").strip()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()
    conn.close()
    print("Registration successful.")
    return True

def login_user():
    conn = connect_db()
    cur = conn.cursor()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        if row[0] == password:
            print("Login successful.\n")
            return True
        else:
            print("Invalid password.\n")
            return False
    print("Invalid username.\n")
    return False
