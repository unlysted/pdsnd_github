import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }

# Added the word 'all' so the month's calendar number equals its index
MONTH_DATA = ['all','january','february','march','april','may','june',
              'july','august','september','october','november','december']

# Added the word 'all' and set monday as the zeroth index
# Each day's name index matches the 0-6 range for datetime days of the week
DAY_DATA = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

option = {'yes','no'}

def month_name(x):
    return MONTH_DATA[x]

def day_name(x):
    return DAY_DATA[x]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    city = ''
    while city.lower().strip() not in CITY_DATA.keys():
        city = input("Choose a city: ").lower().strip()
        if city not in CITY_DATA.keys():
            print("Use one of the following: Chicago, New York City, Washington")
        else:
            city = city.lower().strip()
    
    # get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower().strip() not in MONTH_DATA:
        month = input("Type a month name or type 'all': ").lower().strip()
        if month not in MONTH_DATA:
            print("\nTry again. Use one of the following:")
            print(*[m.title() for m in MONTH_DATA[-12:]],sep=', ')
        else:
            month = month.lower().strip()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.lower().strip() not in DAY_DATA:
        day = input("Type a day of the week name or type 'all': ").lower().strip()
        if day not in DAY_DATA:
            print("\nTry again. Use one of the following:")
            print(*[d.title() for d in DAY_DATA[:7]],sep=', ')
        else:
            day = day.lower().strip()
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # creates the dataframe 'df'
    df = pd.read_csv(CITY_DATA[city])
    
    # names the unnamed column
    df = df.rename(columns={"Unnamed: 0":"ID"})
    
    # casts the 'End Time' column as datetime
    time_col = 'End Time'
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col])
        
    # casts the 'Start Time' column as datetime and filters below
    time_col = 'Start Time'
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col])
            
        # filters 'df' against the chosen month except when month is 'all'
        if month != 'all':
            df = df[df[time_col].dt.month == MONTH_DATA.index(month)]
        
        # filters 'df' against the chosen day except when day is 'all'
        if day != 'all':
            df = df[df[time_col].dt.dayofweek == DAY_DATA.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    trip_start = 'Start Time'
    
    if trip_start in df.columns:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()
        
        # display the most common month
        month_mode = MONTH_DATA[df[trip_start].dt.month.mode()[0]].title()
        print('The most common rental month of the year:\t', month_mode)
    
        # display the most common day of week
        day_mode = DAY_DATA[df[trip_start].dt.dayofweek.mode()[0]].title()
        print('The most common rental day of the week:\t\t', day_mode)
    
        # display the most common start hour
        hr_mode = df[trip_start].dt.hour.mode()[0]
        if hr_mode < 12:
            hr_mode = str(hr_mode) + ' AM'
        else:
            hr_mode = str(hr_mode%12) + ' PM'
        print('The most common rental hour of the day:\t\t', hr_mode)
        
        print_total_time(start_time)
    else:
        print_no_info(trip_start)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start_stn = 'Start Station'
    end_stn = 'End Station'
    start_bool = True
    end_bool = True
    
    if start_stn in df.columns:
        # display most commonly used start station
        start_station = df[start_stn].mode()[0].title()
        print('The most common start station:\t{}\n'.format(start_station))
    else:
        print_no_info(start_stn)
        start_bool = False

    # display most commonly used end station
    if end_stn in df.columns:
        end_station = df[end_stn].mode()[0].title()
        print('The most common end station:\t{}\n'.format(end_station))
    else:
        print_no_info(start_stn)
        end_bool = False
    
    # display most frequent combination of start station and end station trip
    start_end = 'most common start, end station combination'
    if end_stn in df.columns and start_stn in df.columns:
        start_end_station = (df[start_stn] + ', ' + df[end_stn]).mode()[0]
        print('The {}:\t{}'.format(start_end, start_end_station))
    else:
        print('There is insufficient data to determine the {}.'.format(start_end))
    if not start_bool:
        print_no_info(start_stn)
    if not end_bool:
        print_no_info(end_stn)

    print_total_time(start_time)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    travel_time = 'Trip Duration'
    
    if travel_time in df.columns:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()
        
        # display total travel time
        total_trip = df[travel_time].sum()
        print('Total of all trip times:\n\t{} seconds or {}'.format(total_trip
                                                                    ,recast_time(total_trip)))
                    
        # display mean travel time
        mean_trip = df[travel_time].mean()
        print('Mean for all trip times:\n\t{} seconds or {}'.format(round(mean_trip,1)
                                    ,recast_time(mean_trip)))
        print_total_time(start_time)
    else:
        print_no_info(travel_time)

def recast_time(total_time):
    """
    Returns the total trip time in seconds as number of days with time in h:mm:ss.0 format
    """
    dec_time = round(total_time - int(total_time),1)
    if dec_time == 0:
        dec_time = ''
    total_time = int(total_time)
    m, s = divmod(total_time, 60)
    h, m = divmod(m, 60)
    dy, h = divmod(h, 24)
    
    hms = f'{h:d}:{m:02d}:{s:02d}'
    days = ''
    if dy > 0:
        days = f'{dy:d} days '
    
    return '{}{}{}'.format(days,hms,str(dec_time)[-2:])

def user_stats(df):
    """Displays statistics on bikeshare users."""
    user_type = 'User Type'
    gender = 'Gender'
    birth_year = 'Birth Year'
    
    gender_dict = {'Male': 'Male', 'Female':'Female', np.nan:'No Gender'}

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if user_type in df.columns:
        print('\nThe total counts of user types:\n')
        print(df[user_type].value_counts().to_string())
    else:
        print_no_info(user_type)

    # Display counts of gender
    # Addendum: counts NaN values in the gender column
    if gender in df.columns:
        print('\nThe total counts for users by gender:')
        # print(df[gender].value_counts(dropna=False).rename(index=gender_dict).sort_index().to_string())
        print(df[gender].value_counts(dropna=False).rename(index=gender_dict).sort_index().to_frame())
    else:
        print_no_info(gender)

    # Display earliest, most recent, and most common year of birth
    # Addendum: counts NaN values in the Birth Year column
    if birth_year in df.columns:
        print('\nThe earliest birth year:\t', int(df[birth_year].min()))
        print('The most recent birth year:\t', int(df[birth_year].max()))
        print('The most common birth year:\t', int(df[birth_year].mode()[0]))
        print('\nRows without a birth year:\t', df[birth_year].isnull().sum())
    else:
        print_no_info(birth_year)
        
    print_total_time(start_time)

def print_total_time(start_time):
    print("\nThis took %s seconds." % round((time.time() - start_time),6))
    print('-'*40)

def print_no_info(no_info):
    print('\nThis data set does not have {} information.'.format(no_info))

def display_data(df):
    keep = True
    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data?\nEnter yes or no: ').strip().lower()
    if view_data == 'no':
        keep = False
    
    while keep:
        while view_data not in option:
            view_data = input('Enter yes or no: ').strip().lower()
            if view_data == 'no':
                keep = False
        while (view_data == 'yes'):
            print(df.iloc[start_loc:(start_loc + 5)])
            start_loc += 5
            view_data = input('Do you wish to continue?: ').strip().lower()
            if view_data == 'no':
                keep = False

def main():
    """ 
    The main loops if the user enters yes after each run.
    It stops if the users enters no.
    Otherwise, it keeps asking for an appropriate input.
    
    """
    keep = True 
    while keep:
        # requests input from the user
        city, month, day = get_filters()
        
        # applies user input to create a dataframe
        df = load_data(city, month, day)
        display_data(df)

        # uses the dataframe to generate data
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # loop that runs until the user types yes or no as an input
        restart = ''
        while restart.lower().strip() not in option:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
            if restart not in option:
                print("Try again (yes or no).")
            if restart == 'no':
                keep = False


if __name__ == "__main__":
	main()
