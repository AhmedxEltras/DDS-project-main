import mysql.connector
from mysql.connector import Error
import time

class DatabaseManager:
    def __init__(self):
        self.connections = {}
        self.databases = ['patients_db', 'appointments_db', 'billing_db', 'medical_db']
        
        for db in self.databases:
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='root',
                    database=db
                )
                if connection.is_connected():
                    self.connections[db] = connection
            except Error as e:
                print(f"Error connecting to {db}: {e}")

    def get_connection(self, db_name):
        if db_name in self.connections:
            # If connection is closed, try to reconnect
            if not self.connections[db_name].is_connected():
                try:
                    self.connections[db_name] = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='root',
                        database=db_name
                    )
                except Error as e:
                    print(f"Error reconnecting to {db_name}: {e}")
                    return None
            return self.connections[db_name]
        return None

    def execute_query(self, db_name, query, params=None):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            cursor = None
            try:
                connection = self.get_connection(db_name)
                if not connection:
                    print(f"No connection available for {db_name}")
                    return None
                    
                cursor = connection.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                    
                if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                    connection.commit()
                    return True
                else:
                    results = cursor.fetchall()
                    return results
                    
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                if err.errno == 2013:  # Lost connection error
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(1)  # Wait before retrying
                        continue
                return None
                
            finally:
                if cursor:
                    cursor.close()
        
        return None

    def close_connections(self):
        for connection in self.connections.values():
            if connection and connection.is_connected():
                connection.close()