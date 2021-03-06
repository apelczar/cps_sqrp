'''
dbclient.py
-----------
Facilitates operations against the local sqlite3 database.
'''

from core.clients import apiclient
from core.clients import excel_client
from pathlib import Path
import pandas as pd
import sqlite3
import sys
import os

DATABASE_PATH = "db.sqlite3"

def setup():
    '''
    Rebuilds or newly creates the 'sqrp' and 'enrollment' tables in the 
    sqlite3 database and then populates those tables with data extracted and 
    cleaned from the Chicago Public School District's API sources and 
    Excel files(s).

    Inputs:
        None

    Returns:
        None
    '''
    build_tables()
    progress_df = apiclient.get_progress_report_data()
    profile_df = apiclient.get_profile_data() # enrollment
    social_media = apiclient.get_social_media_data()
    sqrp_excel = excel_client.make_final_df()
    sqrp_df = sqrp_excel.merge(progress_df, on="school_id", \
              how="inner").merge(social_media, on="school_id", how="inner")
    insert_records(profile_df, 'enrollment')
    insert_records(sqrp_df, 'sqrp')


def build_tables():
    '''
    Creates the 'sqrp' and 'enrollment' tables using a SQL setup script.

    Inputs:
        None

    Returns:
        None
    '''
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    with open('core/scripts/setup.sql') as f:
        commands = f.read()
        cursor.executescript(commands)
    conn.close()


def insert_records(df, table_name):
    '''
    Inserts new records into the specified database table. Note: This function
    does not perform updates to existing data and will err if the user
    attempts to insert a record whose key already exists in the table.

    Inputs:
        df (pandas.DataFrame): the records
        table_name (str): the table name

    Returns:
        None
    '''
    conn = sqlite3.connect(DATABASE_PATH)
    df.to_sql(table_name, con=conn, index=False, if_exists='append')
    conn.close()


def get_records():
    '''
    Retrieves all school and enrollment records from the respective 'sqrp'
    and 'enrollment' database tables.
    
    Inputs:
        None

    Returns:
        A tuple consisting of two items: (1) list of dictionaries, where each
            dictionary represents a school and (2) a pandas DataFrame
            holding school enrollment data.
    '''
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sqrp ORDER BY school_name;")
    rows = cursor.fetchall()
    schools = [dict(r) for r in rows]
    enrollment = pd.read_sql_query("SELECT * FROM enrollment",
                                   conn, index_col="school_id")
    conn.close()
    return schools, enrollment


if __name__ == "__main__":
    print("Rebuilding sqrp and enrollment tables in database 'db.sqlite3'")
    setup()
    print("Tables rebuilt successfully")