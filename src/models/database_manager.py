from mysql.connector import connect, Error
import random

class DatabaseManager:
    def __init__(self):
        # Define the two servers
        self.servers = {
            'server1': {
                'host': 'localhost',  # Using localhost for testing
                'user': 'root',
                'password': 'root'
            },
            'server2': {
                'host': 'localhost',  # Using localhost for testing
                'user': 'root',
                'password': 'root'
            }
        }
        
        # Database distribution across servers
        self.db_server_map = {
            'patients_db': 'server1',     # Patients DB on Server 1
            'medical_db': 'server1',      # Medical DB on Server 1
            'appointments_db': 'server2', # Appointments DB on Server 2
            'billing_db': 'server2'       # Billing DB on Server 2
        }
        
        # Database configurations
        self.config = {
            'patients_db': {
                'database': 'patients_db'
            },
            'appointments_db': {
                'database': 'appointments_db'
            },
            'billing_db': {
                'database': 'billing_db'
            },
            'medical_db': {
                'database': 'medical_db'
            }
        }
        
    def _get_connection(self, db_name):
        try:
            # Get the server assigned to this database
            server_name = self.db_server_map.get(db_name)
            if not server_name:
                print(f"Error: No server mapping found for {db_name}")
                return None
                
            # Get server configuration
            server_config = self.servers.get(server_name)
            if not server_config:
                print(f"Error: Server configuration not found for {server_name}")
                return None
                
            # Combine server config with database config
            connection_config = {**server_config, **self.config[db_name]}
            
            # Debug information
            print(f"Attempting to connect to {db_name} on {server_name} with config: {connection_config}")
            
            # Connect to the database on the assigned server
            connection = connect(**connection_config)
            print(f"Successfully connected to {db_name} on {server_name}")
            return connection
        except Error as e:
            print(f"Error connecting to {db_name} on {server_name}: {e}")
            # Show more detailed error information
            import traceback
            traceback.print_exc()
            return None

    def execute_query(self, db_name, query, params=None):
        conn = self._get_connection(db_name)
        if not conn:
            print(f"Failed to get connection for {db_name}. Cannot execute query.")
            return None
        
        try:
            cursor = conn.cursor()
            print(f"Executing query on {db_name}: {query[:100]}{'...' if len(query) > 100 else ''}")
            
            if params:
                # Convert 'None' strings to None type for SQL NULL
                processed_params = [None if param == 'None' or param == '' else param for param in params]
                print(f"With parameters: {processed_params}")
                cursor.execute(query, processed_params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
                last_id = cursor.lastrowid
                print(f"Query executed successfully. Last inserted ID: {last_id}")
                return last_id
            else:
                results = cursor.fetchall()
                print(f"Query returned {len(results)} rows")
                if len(results) == 0:
                    print("WARNING: Query returned no results. This might be why no data appears.")
                elif len(results) < 5:  # Only print a few rows for debugging
                    print(f"Sample results: {results[:3]}")
                return results
        except Error as e:
            server_name = self.db_server_map.get(db_name, 'unknown')
            print(f"Error executing query on {db_name} (server: {server_name}): {e}")
            print(f"Failed query: {query}")
            if params:
                print(f"With parameters: {params}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
