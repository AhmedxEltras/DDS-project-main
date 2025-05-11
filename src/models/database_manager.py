from mysql.connector import connect, Error

class DatabaseManager:
    def __init__(self):
        self.config = {
            'patients_db': {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'database': 'patients_db'
            },
            'appointments_db': {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'database': 'appointments_db'
            },
            'billing_db': {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'database': 'billing_db'
            },
            'medical_db': {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'database': 'medical_db'
            }
        }
        
    def _get_connection(self, db_name):
        try:
            return connect(**self.config[db_name])
        except Error as e:
            print(f"Error connecting to {db_name}: {e}")
            return None

    def execute_query(self, db_name, query, params=None):
        conn = self._get_connection(db_name)
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            if params:
                # Convert 'None' strings to None type for SQL NULL
                processed_params = [None if param == 'None' or param == '' else param for param in params]
                cursor.execute(query, processed_params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
                return cursor.lastrowid
            else:
                return cursor.fetchall()
        except Error as e:
            print(f"Error executing query on {db_name}: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
