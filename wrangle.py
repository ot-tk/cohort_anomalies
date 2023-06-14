"""
Wrangle Codeup Curriculum Access Logs

Functions:
- wrangle_logs
    - get_db_url

"""

##### IMPORTS #####

# imports
import pandas as pd
import numpy as np
import os
# local
from env import username,password,host

##### FUNCTIONS #####

def get_db_url(db,user=username,password=password,host=host):
    """
    Returns a formatted string that contains the database URL using the provided parameters: db, user,
    password, and host. The URL is in the format of 'mysql+pymysql://user:password@host/db'.
    """
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def wrangle_logs():
    """
    Returns a pandas DataFrame that has been cleaned and sorted. Specifically, it is returning a
    DataFrame of logs data that has been read from a CSV file or a SQL database, cleaned by dropping
    null values and filling missing values, and sorted by datetime index.
    """
    # fire file
    filename = 'logs.csv'
    # check for file
    if not os.path.isfile(filename):
        df = pd.read_sql('''
                        select l.date,l.time,l.path,l.user_id,l.cohort_id,l.ip,
                                c.name,c.start_date,c.end_date,c.program_id
                        from logs as l
                        left join cohorts as c on l.cohort_id=c.id
                        ''',get_db_url('curriculum_logs'))
        # Drop the one null in column: 'path'
        df = df[df['path'].notna()]
        # Replace missing values with 0 in column: 'cohort_id'
        # Replace missing values with "unknown" in column: 'name'
        df = df.fillna({'cohort_id': 0,'name': "unknown"})
        # Derive column 'datetime' from columns: 'date', 'time'
        df.insert(2, 'datetime', df.apply(lambda row: f'{row.date} {row.time}', axis=1))
        # drop old date and time columns
        df = df.drop(columns=['date','time'])
        # cache it
        df.to_csv(filename,index=False)
    # get prebuilt csv
    else:
        # read prebuilt csv
        df = pd.read_csv(filename)
    # Change column type to datetime64[ns] for columns: 'datetime', 'start_date', 'end_date'
    df = df.astype({'datetime': 'datetime64[ns]', 'start_date': 'datetime64[ns]', 'end_date': 'datetime64[ns]'})
    # make datetime index and sort
    return df.set_index('datetime').sort_index()
