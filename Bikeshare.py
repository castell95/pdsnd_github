import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA=['january','february','march','april','may','june','all']

DAY_DATA=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

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
    city_input=''
    while city_input.lower() not in CITY_DATA:
        city_input=input('Please choose one of the cities Chicago, New York City or Washington: \n')
        if city_input.lower() in CITY_DATA:
            city=CITY_DATA[city_input.lower()]
        elif city_input.lower()=='new york':
            city_input='new york city'
            city=CITY_DATA[city_input]
        else:
            print("The city you have selected is not available.")

    # get user input for month (all, january, february, ... , june)
    month_input=''
    while month_input.lower() not in MONTH_DATA:
        month_input=input('Please choose a month between January and June: or type in all: \n')
        if month_input.lower() in MONTH_DATA:
            month=month_input.lower()
        else:
            print("The month you have selected is not valid. Please try again \n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input=''
    while day_input.lower() not in DAY_DATA:
        day_input=input('Please choose a weekday or take all: \n')
        if day_input.lower() in DAY_DATA:
            day=day_input.lower()
        else:
            print("The day you have selected is not valid. Please try again \n")

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
    df=pd.read_csv(city) #Load .csv city data
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month_num']=df['Start Time'].dt.month
    df['month_name']=df['Start Time'].dt.month_name()
    df['day_name']=df['Start Time'].dt.day_name()
    df['day_of_week']=df['Start Time'].dt.weekday
    df['hour']=df['Start Time'].dt.hour

    if month !='all':
        month=MONTH_DATA.index(month)+1
        df=df.loc[df['month_num']== month]
    if day!='all':
        df=df.loc[df['day_name']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month=df['month_name'].mode()[0]
    print("The most popular month is: ", popular_month)
    # display the most common day of week
    popular_day=df['day_name'].mode()[0]
    print("The most popular day is: ", popular_day)

    # display the most common start hour
    popular_hour=df['hour'].mode()[0]
    print("The most popular hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start=df['Start Station'].mode()[0]
    print("The most popular start station is: ", popular_start)

    # display most commonly used end station
    popular_end=df['End Station'].mode()[0]
    print("The most popular end station is: ", popular_end)

    # display most frequent combination of start station and end station trip
    df['combo']=df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo=df['combo'].mode()[0]
    print("The most popular combination is: ", combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time=df['Trip Duration'].sum()
    total_time_hours=total_time//3600
    total_round=round(total_time, 0)
    print("The total travel time in seconds is: ", str(total_time)+"sec")
    print("The total travel time in hours is: ", str(total_time_hours)+"hours")

    # display mean travel time
    mean_time=df['Trip Duration'].mean()
    mean_round=round(mean_time, 0)
    print("The mean travel duration is: ", str(mean_round)+"sec")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    try:
        count_of_user=df['User Type'].value_counts()
        print(str(count_of_user))
    # Display counts of gender of chicago and new york city
        count_of_gender=df['Gender'].value_counts()
        print(str(count_of_gender))
    # Display earliest, most recent, and most common year of birth
        earliest=df['Birth Year'].min()
        most_recent=df['Birth Year'].max()
        most_common=df['Birth Year'].mode()[0]
        print("The earliest year of birth: "+str(earliest))
        print("The most recent year of birth: "+str(most_recent))
        print("The most common year of birth: "+str(most_common))

    except:
        print("User stats: User Type and Gender is not available for Washington D.C.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    """ Displays 5 lines of raw data if the user wants to."""
    """ If the user types something different than yes than the raw data function breaks"""

    i=0 #Counter of the rows
    while True:
        user_input=input("Do you want to display 5 lines of the raw data?\n").lower()
        if user_input== 'yes':
            print(df.iloc[i:i+5])
            i=i+5
            continue
        else:
            break

    return df

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
