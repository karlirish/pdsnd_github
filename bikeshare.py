import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city = input("Please specify the city you would like to analyze: Chicago, New York City, or Washington. ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("That is not an appropriate selection.")
        else:
            break

    while True:
        month = input("Please specify the month you would like to analyze, from January through June. Or type 'All' to analyze all months. ").lower()
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print("That is not an appropriate selection.")
        else:
            break

    while True:
        day = input("Please specify the day of the week you would like to analyze. Or type 'All' to analyze all days of the week. ").lower()
        if day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            print("That is not an appropriate selection.")
        else:
            break
            
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
            
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
           
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print("Month of most frequent bikeshare usage:", common_month)

    common_day_of_week = df['day_of_week'].mode()[0]
    print("Day of most frequent bikeshare usage:", common_day_of_week)

    common_hour = df['hour'].mode()[0]
    print("Hour of most frequent start time for bikeshare usage:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("Most popular start station:", common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print("Most popular end station:", common_end_station)

    popular_trip = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print("Most popular trip:", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum() / 3600
    print("Total time of all trips (in hours):", total_travel)

    mean_travel = df['Trip Duration'].mean() / 60
    print("Average trip duration (in minutes):", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Counts of user types:", user_types)

    try:
        gender_count = df['Gender'].value_counts()
        print("Counts of gender:", gender_count)
    except KeyError:
        print("Gender data is not available.")

    try:
        min_dob = df['Birth Year'].min()
        print("The earliest year of birth for a rider:", min_dob)
        max_dob = df['Birth Year'].max()
        print("The most recent year of birth for a rider:", max_dob)
        mode_dob = df['Birth Year'].mode()[0]
        print("The most common year of birth for a rider:", mode_dob)
    except KeyError:
        print("Birth year data is not available.")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
    
def five_raw_lines(df):
    """
    Prompts the user if they want to see 5 lines of raw data. Displays that data if the answer is 'yes'. Continues these prompts and displays until the user says 'no'.

    """
    x = 0
    while True:
        prompt = input("Would you like to see 5 lines of raw data from the dataframe? \nIf you've previously answered yes, would you like to see 5 more lines? \nPlease answer 'Yes' or 'No'. ").lower()
        if prompt not in ['yes', 'no']:
            print("That is not an appropriate selection")
        elif prompt == 'yes':
            print(df[x : x + 5])
            x = x + 5
        elif prompt == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        five_raw_lines(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
