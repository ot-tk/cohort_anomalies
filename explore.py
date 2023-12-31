"""
Explore Access Logs for the Codeup Curriculum

Functions:
- prep_1235
- question1
- question2
- question3
- question5

"""

##### IMPORTS #####

import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler

##### FUNCTIONS #####

def prep_1235(df):
    """
    The function filters and cleans a given dataframe by replacing missing values, filtering rows based
    on certain columns and returns the cleaned dataframe.
    
    :param df: a pandas DataFrame containing web traffic data
    :return: a modified DataFrame with missing values replaced, and certain rows filtered out based on
    the values in the 'path' and 'name' columns. The modified DataFrame is then reset to a new index and
    returned.
    """
    # Replace missing values with 0 in column: 'program_id'
    df = df.fillna({'program_id': 0})
    # Filter rows based on column: 'path'
    df = df[df['path'] != "/"]
    # Filter rows based on column: 'path'
    df = df[df['path'] != "toc"]
    # Filter rows based on column: 'path'
    df = df[df['path'] != "search/search_index.json"]
    # Filter rows based on column: 'name'
    df = df[df['name'] != "Staff"]
    # Filter rows based on column: 'name'
    df = df[df['name'] != "unknown"]
    return df.reset_index()

"""------------------------------------------------------------------------------------------------------------------"""

def question1(df):
    """
    The function performs aggregation and sorting on a dataframe, and prints the top lesson and count
    for web development and data science programs.
    """
    # prep it
    df2 = prep_1235(df)
    # Performed 1 aggregation grouped on columns: 'program_id', 'path'
    pg_path = df2.groupby(['program_id', 'path']).agg(path_count=('path', 'count')).reset_index()
    # Sort by column: 'path_count' (descending)
    pg_path = pg_path.sort_values(['path_count'], ascending=[False])
    # make web dev df
    wd = pg_path[pg_path.program_id!=3]
    print('Web Dev')
    print(f'lesson: {wd.head(10).tail(1).path.values[0]}')
    print(f'count: {wd.head(10).tail(1).path_count.values[0]}')
    print()
    # make data science df
    ds = pg_path[pg_path.program_id==3]
    print('Data Science')
    print(f'lesson: {ds.head(1).path.values[0]}')
    print(f'count: {ds.head(1).path_count.values[0]}')

'''------------------------------------------------------------------------------------------------------------------'''   

def question2(df):
    """
    This function performs an aggregation on a dataframe grouped by program ID, name, and path, sorts
    the result by path count in descending order, and returns the rows where the path is
    "classification/overview".
    
    :param df: The parameter `df` is a pandas DataFrame that contains data related to programs and their
    paths. The function `question2` takes this DataFrame as input and performs some operations on it to
    return a new DataFrame
    :return: a DataFrame that contains the count of occurrences of the path "classification/overview"
    for each unique combination of program_id, name, and path in the input DataFrame. The DataFrame is
    sorted in descending order based on the path_count column.
    """
    # prep it
    df2 = prep_1235(df)
    # Performed 1 aggregation grouped on columns: 'program_id', 'name', 'path'
    glossy = df2.groupby(['program_id', 'name', 'path']).agg(path_count=('path', 'count')).reset_index()
    # Sort by column: 'path_count' (descending)
    glossy = glossy.sort_values(['path_count'], ascending=[False])
    return glossy[glossy['path'] == "classification/overview"].iloc[:,1:]

"""------------------------------------------------------------------------------------------------------------------"""

def question3(df,plot=False):
    """
    The function performs aggregations and filtering on a given dataframe, and optionally plots a
    scatter plot of the results.
    
    :param df: The input dataframe containing information about user activity in a course
    :param plot: A boolean parameter that determines whether or not to plot the results. If set to True,
    a scatter plot will be generated showing the difference in days between the course duration and the
    number of days the student was active, for each lazy student in the top three cohorts. If set to
    False, the function, defaults to False (optional)
    :return: If `plot` is `True`, a scatter plot showing the difference in days between course duration
    and student active days for the top cohorts with lazy students is returned. If `plot` is `False`,
    value counts for program id and cohort name are returned.
    """
    # prep it
    df2 = prep_1235(df)
    active = (df2['datetime'] >= df2['start_date']) & (df2['datetime'] <= df2['end_date'])
    lazy_users = df2.assign(active=active)
    # Performed 4 aggregations grouped on columns: 'user_id', 'program_id', 'name'
    lazy_users = lazy_users[lazy_users.active==True].groupby(['user_id', 'program_id', 'start_date', 'end_date', 'name']).agg(path_count=('path', 'count'), datetime_first=('datetime', 'first'), datetime_last=('datetime', 'last'), ip_mode=('ip', lambda s: s.value_counts().index[0])).reset_index()
    # Derive column 'duration' from columns: 'start_date', 'end_date'
    lazy_users.insert(4, 'duration', lazy_users.apply(lambda row : (row['end_date']-row['start_date']).days, axis=1))
    # Derive column 'days_active' from columns: 'datetime_first', 'datetime_last'
    lazy_users.insert(9, 'days_active', lazy_users.apply(lambda row : (row['datetime_last']-row['datetime_first']).days, axis=1))
    # Filter rows based on column: 'path_count'
    lazy_users = lazy_users[lazy_users['path_count'] < lazy_users['duration']]
    print('Top Cohorts with # of less active students')
    print(lazy_users.name.value_counts()[:3])
    if plot ==True:
        # set plot sizes
        fig, ax = plt.subplots(figsize=(14,6))
        # set course duration plot
        ax.scatter(lazy_users.user_id, lazy_users.duration-lazy_users.days_active, label='Other Cohorts', alpha=.5)
        # top cohorts with lazy students
        ax.scatter(lazy_users[lazy_users.name=='Oberon'].user_id, lazy_users[lazy_users.name=='Oberon'].duration-lazy_users[lazy_users.name=='Oberon'].days_active, label='Oberon', alpha=.5)
        ax.scatter(lazy_users[lazy_users.name=='Neptune'].user_id, lazy_users[lazy_users.name=='Neptune'].duration-lazy_users[lazy_users.name=='Neptune'].days_active, label='Neptune', alpha=.5)
        ax.scatter(lazy_users[lazy_users.name=='Sequoia'].user_id, lazy_users[lazy_users.name=='Sequoia'].duration-lazy_users[lazy_users.name=='Sequoia'].days_active, label='Sequoia', alpha=.5)
        # set legend loc and ylabel
        ax.legend(loc='lower right')
        ax.set_ylabel('Number of days')
        ax.set_xlabel('Student User ID')
        plt.title('Less Active Students\nDifference in days from Course Duration and Student Active Days')
        # plot it
        plt.show()

"""------------------------------------------------------------------------------------------------------------------"""        

# Question 4
# functions for anomaly detection
def one_user_df_prep(df, user):
    df = df[df.user_id == user].copy()
    df = df.sort_index()
    pages_one_user = df['path'].resample('d').count()
    return pages_one_user

def compute_pct_b(pages_one_user, span, k, user):
    midband = pages_one_user.ewm(span=span).mean()
    stdev = pages_one_user.ewm(span=span).std()
    ub = midband + stdev*k
    lb = midband - stdev*k
    
    my_df = pd.concat([pages_one_user, midband, ub, lb], axis=1)
    my_df.columns = ['pages_one_user', 'midband', 'ub', 'lb']
    
    my_df['pct_b'] = (my_df['pages_one_user'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def plot_bands(my_df, user):
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(my_df.index, my_df.pages_one_user, label='Number of Pages, User: '+str(user))
    ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
    ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
    ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
    ax.legend(loc='best')
    ax.set_ylabel('Number of Pages')
    plt.show()

def find_anomalies(df, user, span, weight, plot=False):
    pages_one_user = one_user_df_prep(df, user)
    
    my_df = compute_pct_b(pages_one_user, span, weight, user)
    
    if plot:
        plot_bands(my_df, user)
    
    return my_df[my_df.pct_b>1]

def anomaly_loop(df,span=30 ,k=3.5):
   
    anomalies = pd.DataFrame()
    for u in df.user_id.unique():
        df_user = find_anomalies(df,u, span, k)
        anomalies = pd.concat([anomalies, df_user]) 
    return anomalies

def get_lower_and_upper_bounds(col, k=1.5):

    #calculate our q1 and q3
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    
    iqr = q3-q1    
    
    #create fence
    lower_fence = q1 - (iqr*k) 
    upper_fence = q3 + (iqr*k) 
    
    return lower_fence, upper_fence



def print_lower_and_upper_bounds(anomalies, lower_fence, upper_fence):
    '''print("Lower Fence for pages_one_user")    
    print(anomalies["pages_one_user"] [(anomalies["pages_one_user"] < lower_fence)].to_markdown())
    print("-------------------------------------------")
    print("Upper Fence for pages_one_user")
    print(anomalies[["pages_one_user","user_id"]] [(anomalies["pages_one_user"] > upper_fence)].to_markdown())'''
    df_upper_fence = anomalies[["pages_one_user","user_id"]] [(anomalies["pages_one_user"] > upper_fence)]
    return df_upper_fence
    """------------------------------------------------------------------------------------------------------------------"""

def question5(df,program):
    """
    The function takes in a dataframe and a program type, and returns the most recent data science paths
    accessed by web development or the most recent java/javascript paths accessed by data science.
    
    :param df: The input dataframe containing user activity data
    :param program: The parameter 'program' is a string that specifies which program's data to analyze.
    It can be either 'wd' for web development or 'ds' for data science
    :return: the most recent data science paths accessed by web development students if the program
    parameter is 'wd', and the most recent java/javascript paths accessed by data science students if
    the program parameter is 'ds'.
    """
    # prep it
    cutoff = prep_1235(df)
    if program == 'wd':
        # make web dev df
        wd = cutoff[cutoff.program_id!=3]
        # show most recent data science paths accessed by web dev
        return wd[wd['path'].str.contains("data-science", na=False, case=False)][['datetime','path','program_id']].tail(15)
    if program == 'ds':
        # make data science df
        ds = cutoff[cutoff.program_id==3]
        # show most recent java/javascript paths accessed by data science
        return ds[ds['path'].str.contains("java", na=False, case=False)][['datetime','path','program_id']].tail(5)

"""------------------------------------------------------------------------------------------------------------------"""

# question 6
#function to make a df for events after graduation
def after_grad(df):
    df_after_grad = df.sort_values(by=['user_id','end_date'])
    df_after_grad = df_after_grad[df_after_grad.index > df_after_grad.end_date] 
    return df_after_grad
#function to clean up the df_after_grad
def clean_after_grad(df_after_grad):
    df_after_grad = df_after_grad[df_after_grad.name != 'Staff']
    df_after_grad=df_after_grad.drop(columns=['cohort_id','user_id','cohort_id','ip','name','start_date','end_date'])
    df_after_grad['path'] = df_after_grad['path'].str.replace('content/', '')
    df_after_grad['path'] = df_after_grad['path'].str.split('/').str[0]
    df_after_grad['path'] = df_after_grad['path'].str.replace('\d+', '')
    df_after_grad['path'] = df_after_grad['path'].str.replace('.jpg', '')
    df_after_grad['path'] = df_after_grad['path'].str.replace('appendix', '')
    df_after_grad['path'] = df_after_grad['path'].str.replace('search', '')
    df_after_grad['path'] = df_after_grad['path'].str.replace('^-', '')
    df_after_grad = df_after_grad[df_after_grad['path'] != '']
    df_after_grad = df_after_grad[df_after_grad['path'] != '.jpeg']
    df_after_grad = df_after_grad[df_after_grad['path'] != 'index.html']
    df_after_grad = df_after_grad[df_after_grad['path'] != 'toc']
    return df_after_grad



