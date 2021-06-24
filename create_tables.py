import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    Args:
        cur: database cursor.
        conn: database cunnection.   
    """
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables dropped succesfuly")
    except psycopg2.Error as e:
        print("Error dropping tables")
        print(e)


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    Args:
        cur: database cursor.
        conn: database cunnection.
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables created succesfuly")
    except psycopg2.Error as e:
        print("Error creating tables")
        print(e)


def main():
    """
    - Get sensible data from dwh.cfg to connect with redshift cluster
        
    - Establishes connection with the redshift database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()