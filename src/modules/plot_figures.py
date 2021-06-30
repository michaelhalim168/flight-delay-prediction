import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def df_for_plot(df):

    '''
    Extract relevant features from flight dataframe.
        Input: Raw dataframe
        Output: Dataframe with relevant features for analysis
    '''
    
    new_df = df.drop(['branded_code_share', 'mkt_carrier', 'mkt_carrier_fl_num',
                      'op_carrier_fl_num', 'cancellation_code', 'carrier_delay', 'weather_delay', 
                      'nas_delay', 'security_delay', 'late_aircraft_delay', 'first_dep_time',
                      'total_add_gtime', 'longest_add_gtime', 'no_name'], axis=1).dropna()
    
    new_df['fl_date'] = pd.to_datetime(new_df['fl_date'], format='%Y-%m-%d')
    new_df['is_arr_delay'] = new_df.apply(lambda row: 0 if row.arr_delay <= 0 else 1, axis=1)

    return new_df

def get_flight_pattern(df):
    
    '''
    Computes total flights in a year, categorized by month and year.
        Input: Dataframe of flights in that year
        Output: Dataframe of total flights separated by months and weekday. Plots figures.
    '''
    if len([df['fl_date'].dt.year[0]]) == 1:
        year = df['fl_date'].dt.year[0]
   
    try:
        if len(df['fl_date'].dt.year[0]) == 2:
            year = '2018-2019'
    except:
        pass
    
    month_flights = df.groupby('fl_date').size().reset_index()
    month_flights = month_flights.groupby(month_flights['fl_date'].dt.month).sum().reset_index()
    month_flights.columns = ['month', 'tot_flights']
    month_delays = df[['fl_date', 'is_arr_delay']].groupby([df['fl_date'].dt.month]).sum().reset_index().rename(columns={'fl_date':'month'})
    month_flights = pd.merge(month_flights, month_delays)
    
    weekday_mapper = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                      4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    weekday_flights = pd.DataFrame(df.groupby(df['fl_date'].dt.weekday).size()).reset_index().rename(columns={'fl_date': 'weekday', 0:'tot_flights'})
    weekday_delays = df[['fl_date', 'is_arr_delay']].groupby([df['fl_date'].dt.weekday]).sum().reset_index().rename(columns={'fl_date':'weekday'})
    weekday_flights = pd.merge(weekday_flights, weekday_delays)
    weekday_flights['weekday'] = weekday_flights['weekday'].map(weekday_mapper)
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
    
    sns.set_color_codes('pastel')
    sns.barplot(x='month', y='tot_flights', data=month_flights, color='b', edgecolor='.2', ax=ax[0], label='Total Flights')
    sns.set_color_codes('muted')
    sns.barplot(x='month', y='is_arr_delay', data=month_flights, color='b', edgecolor='.2', ax=ax[0], label='Delayed Flights')
    ax[0].set(xlabel='Month', ylabel='Number of Flights')
    ax[0].set_title(f'{year} Monthly Flight Patterns',fontdict= { 'fontsize': 16, 'fontweight':'bold'}, x =0.3, y=1.05)
    
    sns.set_color_codes('pastel')
    sns.barplot(x='weekday', y='tot_flights', data=weekday_flights, color='b', edgecolor='.2', ax=ax[1], label='Total Flights')
    sns.set_color_codes('muted')
    sns.barplot(x='weekday', y='is_arr_delay', data=weekday_flights, color='b', edgecolor='.2', ax=ax[1], label='Delayed Flights')
    ax[1].set(xlabel='Day of Week', ylabel='Number of Flights')
    ax[1].set_title(f'{year} Weekday Flight Patterns',fontdict= {'fontsize': 16, 'fontweight':'bold'}, x =0.3, y=1.05)
    sns.despine()
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
    
    return month_flights, weekday_flights

def get_airlines_pattern(df):
    
    if len([df['fl_date'].dt.year[0]]) == 1:
        year = df['fl_date'].dt.year[0]
   
    try:
        if len(df['fl_date'].dt.year[0]) == 2:
            year = '2018-2019'
    except:
        pass
    
    #Compute total number of flights by each airline
    airlines = df.groupby('mkt_unique_carrier').size().reset_index().rename(columns={0:'num_flights'})
    airlines_delay = df.groupby('mkt_unique_carrier')[['is_arr_delay']].sum().reset_index()
    airlines = pd.merge(airlines, airlines_delay, on='mkt_unique_carrier')
    
    #Plot total flights and delay by airline
    fig, ax = plt.subplots(figsize=(6,4))
    
    sns.set_color_codes('pastel')
    sns.barplot(x='mkt_unique_carrier', y='num_flights', data=airlines, color='b', edgecolor='.2', ax=ax, label='Total Flights')
    sns.set_color_codes('muted')
    sns.barplot(x='mkt_unique_carrier', y='is_arr_delay', data=airlines, color='b', edgecolor='.2', ax=ax, label='Delayed Flights')
    ax.set(xlabel='Airlines', ylabel='Number of Flights')
    ax.set_title(f'{year} Airline Flight Patterns',fontdict= { 'fontsize': 16, 'fontweight':'bold'}, x =0.3, y=1.05)
    sns.despine()
    plt.show()
    
    return airlines

def get_popular_cities(df):
    
    if len([df['fl_date'].dt.year[0]]) == 1:
        year = df['fl_date'].dt.year[0]
   
    try:
        if len(df['fl_date'].dt.year[0]) == 2:
            year = '2018-2019'
    except:
        pass
    
    cities_origin = df.groupby('origin_city_name').size().sort_values(ascending=False).reset_index().rename(columns={0:'num_flights'})
    cities_dest = df.groupby('dest_city_name').size().sort_values(ascending=False).reset_index().rename(columns={0:'num_flights'})
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,6))
    
    sns.set_color_codes('muted')
    sns.barplot(x='num_flights', y='origin_city_name', data=cities_origin[:10], ax=ax[0], color='b', edgecolor='.2')
    ax[0].set(xlabel='Number of Flights', ylabel='')
    ax[0].set_title(f'{year} Most Popular Departure Cities',fontdict= { 'fontsize': 16, 'fontweight':'bold'}, x =0.5, y=1.05)
    
    sns.set_color_codes('muted')
    sns.barplot(x='num_flights', y='dest_city_name', data=cities_dest[:10], ax=ax[1], color='b', edgecolor='.2')
    ax[1].set(xlabel='Number of Flights', ylabel='')
    ax[1].set_title(f'{year} Most Popular Destination Cities',fontdict= { 'fontsize': 16, 'fontweight':'bold'}, x =0.5, y=1.05)
    
    sns.despine()
    plt.show()
   
    return cities_origin, cities_dest

