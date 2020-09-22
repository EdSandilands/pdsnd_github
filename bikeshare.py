import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    # The definitions for the months and days
bs_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'all']
bs_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter the city you wish to see:').lower()
    while city.lower() not in CITY_DATA:
        print('Sorry, we don\'t have data for that city. Please enter Chicago, Washington or New York City')
        city = input('Please enter the city you wish to see:').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please enter the month name (or enter all) that you wish to see:').lower()
    while month.lower() not in bs_months:
        print('Sorry, we don\'t have data for that month. Please Enter data for months January - July or enter "all"')
        month = input('Please select from january, february, march, april, may, june or all:').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter the day name (or enter all) that you wish to analyse:').lower()
    while day.lower() not in bs_days:
        print('Sorry, we don\'t have data for that day')
        day = input('Please enter the day name (or select all) that you wish to see:').lower()

    print('-'*40)
    
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
    
    # Load data file into dataframe
    df = pd.read_csv(CITY_DATA[city], index_col = 0)
    
    # Convert start times into date times and extract month and day
    df['start time'] = pd.to_datetime(df['Start Time'])
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.weekday_name
    df['start_hour'] = pd.to_datetime(df['Start Time']).dt.hour
    
    # Filter by month and week
    if month != 'all':
        allmonths = ['january', 'february', 'march', 'april', 'may', 'june']
        month = allmonths.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    all_months = df['month'].mode()[0] - 1
    mc_month = bs_months[all_months].title()
    print('The most common month is ', mc_month)

    # TO DO: display the most common day of week
    mc_day = df['day_of_week'].mode()[0]
    print('The most common day is ', mc_day)

    # TO DO: display the most common start hour
    mc_hour = df['start_hour'].mode()[0]
    print('The most common hour in the day is hour ', mc_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mc_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is ', mc_start)

    # TO DO: display most commonly used end station
    mc_end = df['End Station'].mode()[0]
    print('The most commonly used end station is ', mc_end)

    # TO DO: display most frequent combination of start station and end station trip
    travel = df.groupby(['Start Station', 'End Station']).count()
    print('The most commonly used combination of start station and end station are ', mc_start, mc_end)
    
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total travel time is ', sum(df['Trip Duration']), 'seconds')

    # TO DO: display mean travel time
    print('The mean travel time is ', df.loc[:, 'Trip Duration'].mean(), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Here is the data for user types:\n', df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
        if 'Gender' in df:
            print('\nHere is the data for gender:')
            print('Male: ', df.query('Gender == "Male"').Gender.count())
            print('Female: ', df.query('Gender == "Female"').Gender.count())
    except KeyError:
            print('Gender\nSorry, we do not have this data')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        min_year = df['Birth Year'].min()
        print('\nEarliest birth year:', min_year)
    except KeyError:
        print('Earliest Birth Year:\nSorry, we do not have this data')
    
    try:
        max_year = df['Birth Year'].max()
        print('\nLatest birth year:', max_year)
    except KeyError:
        print('Latest Birth Year:\nSorry, we do not have this data')       
    
    try:
        mc_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost common birth year:', mc_year)
    except KeyError:
        print('Most Common Birth Year:\nSorry, we do not have this data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Ask the user if they would like to see some raw data
def raw_data(df):
    row = 0
    answer = input('Would you like to see 5 rows of raw data?').lower()    
    while True:
        if answer == 'yes':
            row +=5
            print(df.head(row))
            answer = input('Would you like to see 5 more rows of raw data?').lower()
        elif answer == 'no':
            break
        else:
            print("You must enter 'yes' or 'no'")
            continue
    

    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
