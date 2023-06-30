from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class GetData:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.__filepath = filepath

    def wrangle(self):
        '''Wrangle function
        Return:
            df : pd.DataFrame
        '''

        # Removing missing values
        self.df.dropna(inplace=True)

        # Filtering data
        self.df = self.df[self.df['User Type'] != 'Dependent']

        # Converting Start time and End time columns to DateTime
        self.df['Start Time'] = pd.to_datetime(self.df['Start Time'])
        self.df['End Time'] = pd.to_datetime(self.df['End Time'])

        # Extracting month
        self.df['month'] = self.df['Start Time'].dt.strftime('%B')

        # Extracting Day
        self.df['day'] = self.df['Start Time'].dt.day_name()

        # Extracting Hour
        self.df['hour'] = self.df['Start Time'].dt.hour

        # Converting Trip Durations from sec to min
        self.df['Trip Duration'] = round(self.df['Trip Duration']/60, 2)

        if 'washington' not in self.__filepath:
            # Adding age column
            current_year = date.today().year
            self.df['age'] = self.df['Birth Year'].apply(
                lambda x: current_year - x).astype(int)
            # Removing outliers
        self.df = self.df[self.df['Trip Duration'] < 26]
        if 'washington' not in self.__filepath:
            self.df = self.df[(self.df['age'] > 8) & (self.df['age'] < 65)]

            # Dropping Birth year column
            self.df.drop(['Birth Year'], axis=1, inplace=True)

        # Dropping unwanted columns
        self.df.drop(['Id', 'Start Time', 'End Time'], axis=1, inplace=True)

        return self.df

    def filter_data(self, month, day):
        """
        filters by month and day if applicable.
        Params:
             month: str
                name of the month to filter by, or "all" to apply no month filter
             day: str
                name of the day of week to filter by, or "all" to apply no day filter
        Returns:
             df: pd.DataFrame
                Pandas DataFrame containing city data filtered by month and day if specified
        """

        if month:
            if month != "all":
                self.df = self.df[self.df['month'] == month.title()]

        if day:
            if day != "all":
                self.df = self.df[self.df['day'] == day.title()]

        self.df = self.df[self.df['User Type'] != 'Dependent']
        return self.df

    def time_stats(self):
        """Returns statistics on the most frequent times of travel.

            Returns:
                dict
                  A dictionary containg the most common month, day, hour in the df
        """

        most_common_month = self.df['month'].mode()[0]

        most_common_day = self.df['day'].mode()[0]

        most_common_hour = self.df['hour'].mode()[0]

        return {
            'month': most_common_month,
            'day': most_common_day,
            'hour': most_common_hour
        }

    def station_stats(self):
        """Displays statistics on the most popular stations and trip.

         Returns:
                dict
                  A dictionary containg the most used starting, ending station and most used trip
        """

        # Getting most used start station
        most_common_start_station = self.df['Start Station'].mode()[0]

        # Getting most used ending station
        most_common_end_station = self.df['End Station'].mode()[0]

        # Adding a track column
        self.df['track'] = self.df['Start Station'] + \
            "/" + self.df['End Station']

        # Getting the most used track
        most_common_track = self.df['track'].mode()[0]

        return {
            'start_station': most_common_start_station,
            'end_station': most_common_end_station,
            'track': most_common_track
        }

    def avg_trip_duration(self):
        """Calculates average trip duration.

         Returns:
                avg_time: int
                   Average trip duration.
        """

        avg_time = (self.df['Trip Duration']).mean().round()

        return avg_time

    def user_stats(self, city):
        """Displays statistics on bikeshare users.


        Returns:
                dict
                  A dictionary Containg the number of users for each user type and for each gender, the most common, youngest, oldest ages using bikes
                       if the city is not 'washington'
        """

        # Getting count for each user type
        user_types_count = self.df['User Type'].value_counts().to_dict()

        if city != "washington":

            # Getting count for each gender
            gender_count = self.df['Gender'].value_counts().to_dict()

            # Getting the most occurred age
            most_common_age = self.df['age'].mode()[0]

            # Getting the youngest age
            oldest = abs(self.df['age'].max())

            # Getting the oldest age
            youngest = abs(self.df['age'].min())

            return {
                'users': user_types_count,
                'gender': gender_count,
                'common_year': most_common_age,
                'youngest_year': youngest,
                'oldest_year': oldest
            }

        return {
            'users': user_types_count
        }

    def display_count(self, city, feature):
        """Plot the distribution of a numeric feature or the value count of a feature

            Params:
                city: str
                    Name of city
                feature: str
                    Name of the feature
            Returns:
                fig
        """
        fig, ax = plt.subplots()
        if self.df[feature].dtype == 'O':
            feature_count = self.df[feature].value_counts(
            ).sort_values().tail(10)
            sns.barplot(
                x=feature_count.values, y=feature_count.index, palette='mako', ax=ax, orient='h')
            title = f'Top 10 used {feature} in {city}' if self.df[feature].nunique(
            ) >= 10 else f'Count of {feature} in {city}'
            plt.title(title)
            plt.xlabel('Count')
            plt.ylabel(feature)
            plt.xticks(rotation=90)
        else:
            sns.histplot(self.df[feature], ax=ax)
            plt.title(f'Distribution of {feature} in {city}')
            plt.xlabel(feature)
            plt.ylabel('Count')
            plt.xticks(rotation=90)

        return fig

    def display_duration(self, city, feature, agg_func):
        """Displays ride duration for each age with a specified agg_func

        Params:
            city: str
                Name of the city

            feature: str
                Name of the feature

                agg_func: str
                    Accepts only 'mean' and 'sum'

                Returns:
                    fig    
        """
        if agg_func not in ['mean', 'sum']:
            raise Exception(
                f'The agg_func but be only "mean" or "sum" not {agg_func}')

        top_10_feature = self.df.groupby(feature)['Trip Duration'].agg(
            {agg_func}).squeeze(axis=1).sort_values().tail(10).astype(int)
        fig, ax = plt.subplots()
        sns.barplot(x=top_10_feature.values, y=top_10_feature.index,
                    palette='mako', ax=ax, orient='h')
        word = 'Avg' if agg_func == 'mean' else 'Total'
        title = f'Top 10 {word} ride duration per {feature} in {city}'
        plt.title(title)
        plt.xlabel(f'{word} Ride Duration (min)')
        plt.ylabel(feature)

        return fig

    def day_plot(self, city, agg_func):
        """Plots average trip duration for each day

        Params:
            city : str
                the city to get the data from

            agg_func: str
                accepts only 'mean' and 'sum'
        Returns:
            fig
        """
        def day_sort(counts):
            """Sort array `counts` from Saturday to Friday"""

            labels = ['Saturday', 'Sunday', 'Monday',
                      'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            mapping = {k: v for v, k in enumerate(labels)}
            sort_order = [mapping[c] for c in counts]
            return sort_order

        if agg_func not in ['mean', 'sum']:
            raise Exception(
                f'The agg_func but be only "mean" or "sum" not {agg_func}')

        fig, ax = plt.subplots()
        day_grouped = self.df.groupby(
            'day')['Trip Duration'].agg({agg_func}).squeeze(axis=1)
        day_grouped.sort_index(key=day_sort, inplace=True)
        sns.barplot(x=day_grouped.values, y=day_grouped.index,
                    ax=ax, palette='mako', orient='h')

        word = 'Avg' if agg_func == 'mean' else 'Total'
        plt.xlabel(f'{word} trip Duration (min)')
        plt.ylabel('Day')
        plt.title(f'{word} Trip Duration for each day in {city} city')

        return fig
