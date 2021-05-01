# Import relevant packages
import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


#Ask users for filter criteria
def get_filters():
    
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    #List of expected input from users
    cities = ['chicago','new york city','washington']
    months = ['January','February','March','April','May','June','All']
    days_of_week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
    selection = ['y', 'n']
    
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
        while True:
            city = input('\nWhich city\'s data do you want to take a look at? \n\"Chicago\", \"New York City\" or \"Washington\"?. \nTo exist, click Ctrl+C \n:').lower()
            if city in cities:
                print('\n{} has been captured.'.format(city.title()))
                break
            else:
                print('\nThis city is invalid or there is no data for the City: {}. Please try again.'.format(city.title()))
            
    except KeyboardInterrupt:
        exit()
    
    #get user input for month (all, january, february, ... , june)
    try: 
        while True:
            month = input('\nDo you want to look at a specific month? \n\"January\", \"February\", \"March\",\"April\",\"May\",\"June\" ?. For all month, just type \"All\". \nTo exist, click Ctrl+C \n:').title()
            if month in months:
                print('\n{} has been captured.'.format(month.title()))
                break
            else:
                print('\nThis month is invalid or there is no data for the Month: {}. Please try again.'.format(month.title()))
             
            
    except KeyboardInterrupt:
        exit()
    
    #get user input for day of week (all, monday, tuesday, ... sunday)
    try:
        while True:
            day = input('\nDo you want to look at a specific day of week? \n\"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", \"Sunday\"?. For all week, just type \"All\". \nTo exist, click Ctrl+C \n:').title()
            if day in days_of_week:
                print('\n{} has been captured.'.format(day.title()))
                break
            else:
                print('\nThis day is invalid or there is no data for the Day: {}. Please try again.'.format(day.title()))
                

    except KeyboardInterrupt:
        exit()
    
    #Data filter verfication with restart option
    print("\nYour selection:\n City = " + city.upper() + "\n Month = " + month.upper() + "\n Day = " + day.upper())
    
    try:
        while True:
            select = input('\nIs the selection above correct?\nIf Yes, enter \"Y\" if not or to re-input enter \"N\".\nEnter Ctrl+C to exit \n:')
            if select.lower() in selection:

                if select.lower() == "y":
                    print("Below is the requested data")
                    break
                elif select.lower() == "n":
                    main()
           
            else:
                print('\nInput not recognized! Please try again!\n')
                

    except KeyboardInterrupt:
        exit()
   
    print('-' * 40)
    print('\n')
    return city, month, day

# Loading data for analysis based on city, month, and day filters
def load_data(city, month, day):
   
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day from Start Time column to create a new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Month filter - using the index of the month from list to get corresponding int
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # Created new dataframe for month
        df = df[df['month'] == month]

    # Day filter
    if day != 'All':
        
        # Created new dataframe for day
        df = df[df['day_of_week'] == day.title()]

    return df

# Most frequent times of travel function
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #display the most common month
    df['Month'] = df['Start Time'].dt.month
    common_month = df['Month'].mode()[0]

    #display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day
    common_day = df['day_of_week'].mode()[0]

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print('Most common month: ', calendar.month_name[common_month])
    print('-' * 20)
    print('Most common day: ', common_day)
    print('-' * 20)
    print('Most popular hour: ', common_hour)
    print('-' * 20)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

#Most popular stations and trip function
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    df['common_start'] = df['Start Station']
    common_Start = df['common_start'].mode()[0]
    print ('The most common start station is: ', common_Start)
    print('-' * 20)

    #display most commonly used end station
    df['common_end'] = df['End Station']
    common_end = df['common_end'].mode()[0]
    print('The most common end station is: ', common_end)
    print('-' * 20)

    #display most frequent combination of start station and end station trip
    common_trip = df['common_start'] + ' to ' + df['common_end']
    print('The most common trip is: ', common_trip.mode()[0])
    print('-' * 20)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

#Total and average trip duration function
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    start_time = time.time()

    # Trip start time
    trip_start = pd.to_datetime(df['Start Time'])

    # Trip end time
    trip_end = pd.to_datetime(df['End Time'])

    #display total travel time
    df['Trip Total Time'] =  trip_end - trip_start
    total_time =  df['Trip Total Time'].sum()
    print("The total amount of time for a trip is: " + str(total_time), "hh:mm:ss")
    print('-' * 20)

    #display mean travel time
    mean_time = df['Trip Duration'].mean()
    minutes_ = int(mean_time/60)
    seconds_ = mean_time%60

    print('The average time of a trip is:', minutes_, "minutes", seconds_, "seconds")
    print('-' * 20)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

#Various statistics functions
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_type = df['User Type'].value_counts()

    #Display counts of gender
    gender = df['Gender'].value_counts()

    #Display earliest, most recent, and most common year of birth
    earliest_year = df.sort_values('Birth Year').iloc[0]
    most_recent = df['Birth Year'].max()
    common_year = df['Birth Year'].mode()[0]

    print('Count of user types: ', user_type)
    print('-' * 20)
    print('Count of gender: ', gender)
    print('-' * 20)
    print('Oldest person to rent: ', earliest_year['Birth Year'])
    print('-' * 20)
    print('Most recent: ', most_recent)
    print('-' * 20)
    print('Most common birth year: ', common_year)
    print('-' * 20)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40,'\n')

#prompt the user if they want to see 5 lines of raw data for the selected city
def display_data(df):
    try:
        next_ = 0
        while True: 
            user_prompt = input('Would you like to see (more) 5 lines of raw data for the  selected city?\nIf Yes, enter \"Y\" if No enter \"N\". \n:') 
            if user_prompt == 'y': 
                next_ += 1 
                print ('\n')
                print (df.iloc[(next_ -1)*5:next_ *5])
                print('-' * 40 ,'\n')
                continue
            elif user_prompt == 'n':
                break

            else:
                print('\nInput not recognized! Please try again!\n')
                continue

    except KeyboardInterrupt:
        pass

# Main funtion call to all the funtions
def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

            restart = input('\nWould you like to restart?\nEnter \"Y\" for Yes or \"N\" for No.\n')
            if restart.lower() != 'y':
                exit()
                break

    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()