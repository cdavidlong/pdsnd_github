"""
David Long

c.david.long@gmail.com

Programming for data science

Explore US Bikeshare Data Project submission

Reference sites consulted:

Getting execution time of queries:
https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution

Converting seconds to weeks, days, hours, minutes, seconds
https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
"""

import pandas as pd
import time
from datetime import date

# Dictionary used to key the data files
CITY_DATA = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}

# Dictionary used to key days of the week alternative naming
DAY_DATA = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thur': 'Thursday', 'fri': 'Friday', 'sat': 'Saturday', 'sun': 'Sunday'}

# List used for checking valid months
months = ['january', 'february', 'march', 'april', 'may', 'june']

def display_raw_data(df, displaycount):
    """ Prompts the user if they want to see 5 lines of raw data. Displays that
    data if the answer is 'yes'. Continues these prompts and displays until
    the user says 'no'.
    INPUT:
    df: dataframe. Containing the data to be displayed
    displaycount: int - The number of records to display
    OUTPUT:
    Nothing
    """
    start = 0 # Start from the first recored at position 0
    while True:
        prompt = input('\nWould you like to see ' + str(displaycount) + ' records of raw data from the dataframe? Enter \'y\' or \'n\': ').lower()
        if prompt not in ['yes', 'no', 'y', 'n']:
            print("Enter \'y\' or \'n\': ")
        elif prompt == 'yes' or prompt == 'y':
            print(df[start : start + displaycount])
            start = start + displaycount
        elif prompt == 'no' or prompt == 'n':
            break

def display_time(seconds, granularity):
    """ Determines the weeks, days, hours, minutes and seconds from a given seconds value
    INPUT:
    seconds: int. The number of seconds to be converted
    granularity: int. The granularity to convert the seconds to from weeks, through days, hours, minutes, seconds
    OUTPUT:
    list: list. The conversion of seconds into week, days, hours, minutes and seconds
    """
    # Dictionary used for the display_time function
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def load_data(userselection):
    """ Load data for the specified city and filter by month and day if applicable.
    INPUT:
    userselection: list comprised of the city - name of the city to analyze,
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    OUTPUT:
    df: pandas DataFrame containing city data filtered by month and day as requested by user
    """
    print("\nLoading data for: {}".format(', '.join(userselection)))
    city = userselection[0]
    month = userselection[1]
    if userselection[-1] != "all":
        day = DAY_DATA[userselection[-1]]
    else:
        day = userselection[-1]

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Sort the records by start time
    df = df.sort_values('Start Time',ascending=True)
    return df


def user_data_selection():
    """ Prompts user for the city to analyze, the month, the day of the week and accepts 'all' as month and day also
    INPUT:
    None
    OUTPUT:
    list (city, month, day)
        city - name of the city to analyze
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Welcome message
    print('\nHello and welcome to the bikeshare data anayzer!\n\nLet\'s explore some US bikeshare data.')

    # Prompt user for the city to analyze
    while True:
        try:
            city = input('\nWould you like to see data for Chicago, New York or Washington?\n').lower()
            if city not in CITY_DATA:
                print('\nSorry,{} is not a valid city.\n\nPlease choose again by entering either Chicago, New York City OR Washington.'.format(city))
                continue
            else:
                break
        except ValueError as error:
            print('Exception occurred:{}'.format(error))

    # Prompt user for time period to filter by
    while True:
        try:
            userfilter = input('\nWould you like to filter the data by month, day, both, or not at all?\nType \'none\' for no time period filter, and \'both\' to choose a month and a day.\n').lower()
            if userfilter in['day', 'month', 'both', 'none']:
                break
            else:
                print('\nSorry,{} is not a valid selection'.format(userfilter))
                continue
        except ValueError as error:
            print('Exception occurred:{}'.format(error))

    # Prompt user for the month and day to filter by if they chose to filter by month and day by selecting 'both'
    if userfilter == "both":
        while True:
            try:
                usermonth = input('\nWhich month, January, February, March, April, May or June? Please type out the full month name or \'all\' for all.\n').lower()
                if usermonth in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                elif usermonth in ['july', 'august', 'september', 'october', 'november', 'december']:
                    print('\n,{} \'s data is not available.'.format(usermonth))
                    continue
                elif usermonth == "all":
                    break
                else:
                    print('\n{} is not a valid selection'.format(usermonth))
                    continue
            except ValueError as error:
                print('Exception occurred:{}'.format(error))
        while True:
            try:
                userday = input('\nWhich day, Mon, Tue, Wed, Thu, Fri , Sat or Sun? Type \'all\' to include all.\n').lower()
                if userday in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                    break
                elif userday == "all":
                    break
                else:
                    print('\nSorry,{} is not a valid day selection'.format(userday))
                    continue
            except ValueError as error:
                print('Exception occurred:{}'.format(error))

    # Prompt user for the month to filter by if they chose to filter by month
    elif userfilter == "month":
        while True:
            try:
                usermonth = input('\nWhich month, January, February, March, April, May or June? Please type out the full month name or \'all\' for all.\n').lower()
                if usermonth in ['january', 'february', 'march', 'april', 'may', 'june','all']:
                    break
                elif usermonth in ['july', 'august', 'september', 'october', 'november', 'december']:
                    print('\n,{} \'s data is not available.'.format(usermonth))
                    continue
                elif usermonth == "all":
                    break
                else:
                    print('\n{} is not a valid selection'.format(usermonth))
                    continue
            except ValueError as error:
                print('Exception occurred:{}'.format(error))

    # Prompt user for the day to filter by if they chose to filter by day
    elif userfilter == "day":
        while True:
            try:
                userday = input('\nWhich day, Mon, Tue, Wed, Thu, Fri , Sat or Sun? Type \'all\' to include all.\n').lower()
                if userday in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']:
                    break
                elif userday == "all":
                    break
                else:
                    print('\nSorry,{} is not a valid day selection'.format(userday))
                    continue
            except ValueError as error:
                print('Exception occurred:{}'.format(error))

    # Set userselection string which is used to load the dataframe with the locations and period selected by the user
    if userfilter == 'both':
       userselection = [city, usermonth, userday]
    elif userfilter == 'day':
        userselection = [city, 'all', userday]
    elif userfilter == 'month':
         userselection = [city, usermonth, 'all']
    elif userfilter == 'none':
        userselection = [city, 'all', 'all']
    return userselection


# Prompt user for filter selections
usersel = user_data_selection()

# Load the dataframe based on the user selection
start = time.time()
df = load_data(usersel)
end = time.time()
print('\nThat took: ' + str(end - start) + 'seconds to load the dataframe.')

# There follows a series of statistical results derived from the loaded dataset

# Most popular day for a journey in the requested period
print('\nMost popular day for journeys in: ' + str(usersel[0]).title() + '\n')
print('During the period: ')
print('\n  From: ' + str(df['Start Time'].iloc[0]))
print('\n    To: ' + str(df['Start Time'].iloc[-1]))

# Most popular day of the week to start a journey
print('\nJourneys by day of the week:\n')
start = time.time()
print(df['day_of_week'].value_counts())
end = time.time()
print('\nThat took: ' + str(end - start) + 'seconds to execute.')

# Most popular hour to start a journey during  the requested period
print('\nCount of hourly journeys throughout a day:\n')
start = time.time()
df['start_hour'] = df['Start Time'].dt.hour
print(df['start_hour'].value_counts())
end = time.time()
print('\nThat took: ' + str(end - start) + 'seconds to execute.')

# Total duration of all journeys taken in the requested period
start = time.time()
duration_sum = df['Trip Duration'].sum(skipna = True)
duration_mean = df['Trip Duration'].mean(skipna = True)
print('\nTotal duration of journeys taken: ' + str(duration_sum) + ' seconds\n')
print(display_time(duration_sum, 4) + "\n")
print('\nMean duration of journeys taken: ' + str(duration_mean) + ' seconds\n')
print(display_time(duration_mean, 4) + "\n")
end = time.time()
print('\nThat took: ' + str(end - start) + 'seconds to execute.')

# Age mean and median of riders during  the requested period
# Chck city as the Washington data set does not provide a 'Birth Year' column
if usersel[0] != "washington":
    start = time.time()
    # Fill in any NaN values for Birth Year with the mean
    df["Birth Year"].fillna(df["Birth Year"].mean(), inplace=True)
    current_year = date.today().year
    df['age'] = current_year - df['Birth Year']
    print('\nMean age of subscribers who took journeys: ' + str(df['age'].mean()))
    print('\nMedian age of subscribers who took journeys: ' + str(df['age'].median()))
    end = time.time()
    print('\nThat took: ' + str(end - start) + 'seconds to execute.')

# Popular Start and End stations
start = time.time()
print('\nThe most popular station to start a journey for this period was: ' + str(df['Start Station'].value_counts().idxmax()))
print('\nThe most popular station to end a journey for this period was: ' + str(df['End Station'].value_counts().idxmax()) +'\n' )
end = time.time()
print('\nThat took: ' + str(end - start) + 'seconds to execute.')

# Prompt user if they would like to see raw data, 5 records at at time, exit of the answer is No.
display_raw_data(df, 5)
