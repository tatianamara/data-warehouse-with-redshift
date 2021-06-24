import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load staging tables using the queries in `copy_table_queries` list.
    Args:
        cur: database cursor.
        conn: database cunnection.   
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
        print(f'load staging table {query} successfully')


def insert_tables(cur, conn):
    """
    Insert data in fact and dimension tables using the queries in `insert_table_queries` list.
    Args:
        cur: database cursor.
        conn: database cunnection.   
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Get sensible data from dwh.cfg to connect with redshift cluster
        
    - Establishes connection with the redshift database and gets
    cursor to it.  
    
    - Loads stanging tables.  
    
    - Inserts data in fact and dimension tables. 
    
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()