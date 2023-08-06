import mysql.connector as connector
connection = None
    
def get_db_connection():
    global connection
    if connection is not None:
        print('Return existed connection...')
        return connection
    print("get db connection...")
    from dm_modules.analytics_dao.gservice_dao import get_secret
    mlmd_config = get_secret("MLMD_CONFIG")
    connection = connector.connect(
    host=mlmd_config.get("MLMD_HOST"),
    user=mlmd_config.get("MLMD_USER"),
    password=mlmd_config.get("MLMD_PASSWORD"),
    database=mlmd_config.get("MLMD_DB")
    )
    return connection

def ensure_connection():
    global connection
    if connection is None:
        connection = get_db_connection()
    if not connection.is_connected():
        connection.reconnect(3) 


def execute_query(query, parameters_array, commit=True):
    global connection
    ensure_connection()
    dbcursor = connection.cursor()
    dbcursor.executemany(query, parameters_array)
    if commit:
        connection.commit()
    r = dbcursor.rowcount
    dbcursor.close()
    return r

def execute_query_one(query, parameters, commit=True):
    global connection
    ensure_connection()
    dbcursor = connection.cursor()
    dbcursor.execute(query, parameters)
    if commit:
        connection.commit()
    r = dbcursor.rowcount
    dbcursor.close()
    return r

def execute_select_query(query, parameters, commit=True):
    global connection
    ensure_connection()
    dbcursor = connection.cursor()
    dbcursor.execute(query, parameters)
    r = dbcursor.fetchall()
    if commit:
        connection.commit()
    dbcursor.close()
    return r
