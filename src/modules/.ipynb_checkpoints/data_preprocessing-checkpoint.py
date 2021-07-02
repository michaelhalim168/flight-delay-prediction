import pandas as pd

def extract_features_df(df):
    
    '''
    Extract relevant features from flight dataframe.
        Input: Raw dataframe
        Output: Dataframe with relevant features for analysis
    '''
    
    new_df = df.drop(['branded_code_share', 'mkt_carrier', 'mkt_carrier_fl_num',
                      'op_carrier_fl_num', 'cancellation_code', 'carrier_delay', 'weather_delay', 
                      'nas_delay', 'security_delay', 'late_aircraft_delay', 'first_dep_time',
                      'total_add_gtime', 'longest_add_gtime', 'no_name'], axis=1).dropna()

    new_df = new_df[['fl_date', 'mkt_unique_carrier', 'origin', 'dest', 'crs_dep_time', 
                     'crs_arr_time', 'crs_elapsed_time', 'flights', 'distance']]
    
    new_df['fl_date'] = pd.to_datetime(new_df['fl_date'], format='%Y-%m-%d')

    return new_df

def extract_output_df(df):

    new_df = df[['fl_date', 'mkt_unique_carrier', 'dep_delay', 'arr_delay']]
    new_df['fl_date'] = pd.to_datetime(new_df['fl_date'], format='%Y-%m-%d')
    new_df['is_arr_delay'] = new_df.apply(lambda row: 0 if row.arr_delay <= 0 else 1, axis=1)
    new_df['is_dep_delay'] = new_df.apply(lambda row: 0 if row.dep_delay <= 0 else 1, axis=1)

    return new_df