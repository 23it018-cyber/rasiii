import sqlite3

def check_db():
    print("Checking Database file 'database.db'...")
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in c.fetchall() if t[0] != 'sqlite_sequence']
        print(f"Tables Created: {tables}")
        
        for table in tables:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"- {table}: {count} records")
            
        conn.close()
    except Exception as e:
        print(f"Error accessing DB: {e}")

if __name__ == '__main__':
    check_db()
