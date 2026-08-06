# DB Pool Service
def execute_query(conn_pool, query):
    conn = conn_pool.get_connection()
    try:
        return conn.execute(query)
    finally:
        conn.close()
