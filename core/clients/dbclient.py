#######
# Database client
# Provides access to querying local sqlite3 database
########
import sqlite3
import apiclient
import excel_client

DATABASE_PATH = "../../db.sqlite3"

def build_tables():
    '''
    Builds tables using SQL setup script.
    '''
    con = sqlite3.connect(DATABASE_PATH)
    u = con.cursor()
    with open('../scripts/setup.sql') as f:
        commands = f.read()
        u.executescript(commands)
    con.close()

def setup():
    '''
    Builds empty tables in SQL database, creates pandas dataframes
    from API and excel files, and fills the tables with the information
    from the dataframes.
    '''

    build_tables()
    progress_df = apiclient.get_progress_report_data()
    profile_df = apiclient.get_profile_data() # enrollment
    sqrp_excel = excel_client.make_final_df()
    sqrp_df = sqrp_excel.merge(progress_df, on="school_id", how="inner")
    #print("sqrp looks like: ", sqrp_df.columns)
    insert_into_database(profile_df, 'enrollment')
    insert_into_database(sqrp_df, 'sqrp') # need to make this joined df


def set_up_db():
    put_df_in_database(get_enrollment_data(), 'enrollment')
    put_df_in_database(get_location_data(), 'location')
    put_df_in_database(get_attainment_data(), 'attainment')

def insert_into_database(df, table_name):
    '''
    Inserts new data into database.
    Note: This function does not perform updates to existing tables.
    '''
    con = sqlite3.connect(DATABASE_PATH)
    u = con.cursor()
    df.to_sql(table_name, con=con, index=False, if_exists='append')
    con.close()