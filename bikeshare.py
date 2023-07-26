import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
DAY_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
FILTER_USED = "none"

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = None
    while city is None:
        city = input("Would you like to see the data for Chicago, New York or Washington: ").lower()
        if city in ("chicago", "new york", "washington"):
            print("Looks like you want to hear about {}!  "
                  "If this is not not true, restart the program now".format(city.title()))
        else:
            city = None
            print("Name you entered is invalid!")
            print("Allowed values are: chicago, new york, washington ")

    # get user input for filter (month, day or none)
    filters = None
    while filters is None:
        filters = input("\nWould you like to filter the data by month, day, both or not at all? "
                        "Type none for no filter ").lower()
        if filters in ("month", "day", "both", "none"):
            print("we will make sure to filter by:  {}!  ".format(filters.title()))
            if filters == "none":
                filters = "all"
        else:
            filters = None
            print("Filter you entered is invalid!")
            print("Allowed values are: Month, day or none")

    # get user input for month (all, january, february, ... , june)
    if filters == "month" or filters == "both":
        month = None
        while month is None:
            month = input("\nWhich month? all, January, February, March, April, May, or June? "
                            "Please type the full name ").lower()
            if month in ("all", "january", "february", "march", "april", "may", "june"):
                print("Just one moment...  loading data")
            else:
                month = None
                print("The Month you entered is invalid!")
                print("Allowed values are: January, February, March, April, May, or June")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filters == "day" or filters == "both":
        day = None
        while day is None:
            day = input("\nWhich day? all, monday, tuesday, ... sunday? "
                            "Please type the full name ").lower()
            if day in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
                print("Just one moment...  loading data")
            else:
                day = None
                print("The day of the week you entered is invalid!")
                print("Allowed values are: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday")

    if filters == "all":
        month = "all"
        day = "all"
    elif filters == "month":
        day = "all"
    elif filters == "day":
        month = "all"

    global FILTER_USED
    FILTER_USED = filters

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
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_start_month = df['month'].mode()[0]
    print('Most common month:', MONTHS[popular_start_month-1])

    # display the most common day of week
    popular_start_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_start_day)


    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common End station:', popular_end_station)


    # display most frequent combination of start station and end station trip
    print('Most popular start and end station:')
    print((df['Start Station'] + '  <---->  ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Duration:',  convert_seconds_days(df['Trip Duration'].sum()))

    # display count of travel time
    print('Count of trip: {:,}'.format(df['Trip Duration'].count()))

    # display mean travel time
    print('Average Travel Duration:', convert_seconds_days(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\ncounts of each user type:')
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender,  check if available for the city
    print('\ncounts of each gender')
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No gender data to share')


    # Display earliest, most recent, and most common year of birth
    print('\nCalculating statistics')
    if 'Birth Year' in df.columns:
        print("most recent year of birth is: {}".format(int(df['Birth Year'].max())) )
        print("earliest year of birth is: {}".format(int(df['Birth Year'].min())) )
        print("most common year of birth is: {}".format(int(df['Birth Year'].mode()[0])) )
    else:
        print('No birth year data to share')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert_seconds_days(seconds):
    weeks = seconds // 604800
    seconds %= 604800
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    result = ""
    if weeks > 0:
        result += f" {weeks} weeks, "
    if days > 0:
        result += f" {days} days, "
    if hours > 0:
        result += f" {hours} hours, "
    if minutes > 0:
        result += f" {minutes:.0f} minutes, "
    if seconds > 0:
        result += f" {seconds:.2f} seconds"

    return  result


def main():

    while True:
        city, month, day = get_filters()
        print("Selected city: {}".format(city))
        print("Filter Type: {}".format(FILTER_USED))
        print("month: {}".format(month))
        print("day: {}\n\n".format(day))

        df = load_data(city, month, day)

        if df.shape[0] == 0:
            print("No data available for the selected filter")
        else:
            print('starting analysis')
            print('-' * 50)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            start = 0
            stop  = 0
            view_records = None
            while view_records is None:
                view_records = input("\nWould you like to view individual trip data, Type 'yes or 'no' ").lower()
                if view_records in ('yes', 'no'):
                    if view_records == 'yes':
                        start = stop
                        stop = stop + 5
                        print(df.iloc[start:stop].to_json(orient="records"))
                        print('-' * 40)
                        view_records = None
                else:
                    view_records = None
                    print("input is invalid! Type 'yes or 'no'")




        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
