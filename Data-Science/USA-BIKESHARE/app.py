import streamlit as st
from buisness import GetData

# Setting page config
st.set_page_config(page_title='Us Bikeshare', layout='wide')

# Setting page title
st.title('Us Bikeshare Data Web app')
st.sidebar.write('Please choose a dataset to get started!')

# Setting sidebar width
st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 250px;
            }}
        </style>
    ''',
    unsafe_allow_html=True)

# Hidding unwanted things
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Making a start session state
if 'started' not in st.session_state:
    st.session_state.started = False

# Callback function for dataset selectbox


def change_started():
    st.session_state.started = True


# Dataset selectbox
city = st.sidebar.selectbox(
    'Select Dataset', ('None', 'Chicago', 'New york', 'Washington'), on_change=change_started).lower()

if st.session_state.started:
    error = False
    try:
        # Using The GetData object
        gd = GetData(f'data/{city}.csv')
    except:
        error = True
        st.warning('Choose A Correct Dataset.')
    if not error:
        st.write(f'#### lets explore **{city.title()}** Dataset')
        st.write('---')
        st.sidebar.write(
            f'#### Click the button to **clean** the data and get started.')

        # Clean button season state
        if 'check' not in st.session_state:
            st.session_state.check = False

        # Clean button callback
        def clean_button_callback():
            st.session_state.check = True

        check = st.sidebar.button('Clean 🧹', on_click=clean_button_callback)
        if check or st.session_state.check:
            # Clean the data
            df = gd.wrangle()

            st.sidebar.success('The data has been cleaned successfully.')
            st.sidebar.write('Please Choose the filter conditions you want')
            # Filter selectbox
            filter_condition = st.sidebar.selectbox(
                'Select filter by', ('None', 'Month', 'Day', 'Both'))

            def get_condition(condition):
                """
                    Display a selectbox in which to choose a specified filter

                    Params:
                        condition: str

                    Returns:
                    month: str
                        the month in which we filter by if None then no filter
                    day: str
                        the day in which we filter by if None then no filter
                """
                month, day = None, None
                if condition == 'Month':
                    month = st.sidebar.selectbox('Select Month', ('all', 'January',
                                                                  'February', 'March', 'April', 'May', 'June')).lower()
                elif condition == 'Day':
                    day = st.sidebar.selectbox('Select Day', ('all', 'Monday', 'Tuesday',
                                                              'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')).lower()
                elif condition == 'Both':
                    month = st.sidebar.selectbox('Select Month', ('all', 'January',
                                                                  'February', 'March', 'April', 'May', 'June')).lower()

                    day = st.sidebar.selectbox('Select Day', ('all', 'Monday', 'Tuesday',
                                                              'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')).lower()

                return month, day

            month, day = get_condition(filter_condition)

            # Filtering data upon selected month and day
            df = gd.filter_data(month, day)

            # Data Container
            with st.container():

                c1, c2, c3 = st.columns(3)

                if 'number_of_rows' not in st.session_state:
                    st.session_state.number_of_rows = 5

                # A button if clicked displays 1 more row of the data
                increment = c1.button('Add one row ⬆️')
                if increment:
                    st.session_state.number_of_rows += 1

                # A button if clicked displays 1 less row of the data
                decrement = c2.button('Remove one row ⬇️')
                if decrement:
                    st.session_state.number_of_rows -= 1

                download_button = c3.download_button(
                    label='Download ✅', data=df.to_csv(index=False), file_name=f'{city}.csv')

                st.write(
                    f'Cleaned Data')
                st.write(df.head(st.session_state.number_of_rows))
                st.write('Shape of data', df.shape)
                st.write('---')

            # Information Container
            with st.container():

                st.write(
                    f'#### Lets Check Now Some Interesting Information for {city.title()} data')

                # Getting stats
                time_stats = gd.time_stats()
                st.write(f'''The most busy month is **{time_stats["month"]}**,
                            The most used day is **{time_stats["day"]}**,
                            The most used hour is **{time_stats["hour"]}**
                        ''')

                # Getting stats
                station_stats = gd.station_stats()
                add_day = f' in {day}' if day != 'all' else ''

                st.write(f'''The most used start station is **{station_stats["start_station"]}**,
                            The most used track is **{station_stats["track"]}{add_day}**
                        ''')

                # Getting stats
                avg_ride_dur = gd.avg_trip_duration()

                st.write(
                    f'**The Average Ride Duration** = **{avg_ride_dur}{add_day}**')

                # Getting stats
                user_stats = gd.user_stats(city)

                # Checking city name for different returns check user_stats function for more details
                if city != "washington":

                    n_sub = user_stats['users']['Subscriber']
                    if 'Customer' in user_stats['users'].keys():
                        n_cus = user_stats['users']['Customer']
                    else:
                        n_cus = 0

                    n_male = user_stats['gender']['Male']
                    n_female = user_stats['gender']['Female']
                    common_year = user_stats['common_year']
                    youngest_year = user_stats['youngest_year']
                    oldest_year = user_stats['oldest_year']
                    st.write(
                        f'''Total number of Subscribers = **{n_sub}**,
                            Total number of Customers = **{n_cus}**,
                            Total number of males = **{n_male}**,
                            Total number of Females = **{n_female}**,
                            Total most common age = **{common_year}**,
                            youngest age = **{youngest_year}**,
                            oldest age = **{oldest_year}** {add_day}''')
                else:
                    n_sub = user_stats['users']['Subscriber']
                    n_cus = user_stats['users']['Customer']
                    st.write(
                        f'''**Total number of Subscribers** = **{n_sub}**,
                        **Total number of Customers = **{n_cus}** {add_day}''')

            # Checking city to display different options
            check_city = True if city != 'washington' else False

            if check_city:

                plot = st.sidebar.selectbox(
                    'Select Feature', ('Start Station', 'End Station', 'Day', 'Age', 'Gender', 'User type'), key='plot')
            else:
                plot = st.sidebar.selectbox(
                    'Select Feature', ('Start Station', 'End Station', 'Day', 'User type'), key='plot')

            def choose_plot_duration(plot):
                """
                    Returns a bar plot of the trip duration for the feature and agg func in specified city

                    Params:
                        plot: str
                             Name of the feature to plot

                    Returns:
                        fig
                """
                if plot == 'Start Station':
                    return gd.display_duration(city, 'Start Station', agg_func)
                elif plot == 'End Station':
                    return gd.display_duration(city, 'End Station', agg_func)
                elif plot == 'Day':
                    return gd.day_plot(city, agg_func)
                elif plot == 'Age':
                    return gd.display_duration(city, 'age', agg_func)
                elif plot == 'Gender':
                    return gd.display_duration(city, 'Gender', agg_func)
                else:
                    return gd.display_duration(city, 'User Type', agg_func)

            def choose_plot_count(plot):
                """
                    Returns a barh plot of the value count for the feature in specified city

                    Params:
                        plot: str
                             Name of the feature to plot

                    Returns:
                        fig
                """
                if plot == 'Start Station':
                    return gd.display_count(city, 'Start Station')
                elif plot == 'End Station':
                    return gd.display_count(city, 'End Station')
                elif plot == 'Day':
                    return gd.display_count(city, 'day')
                elif plot == 'Age':
                    return gd.display_count(city, 'age')
                elif plot == 'Gender':
                    return gd.display_count(city, 'Gender')
                else:
                    return gd.display_count(city, 'User Type')

            st.write('---')
            # Plot Container
            with st.container():
                st.write(
                    '#### Now lets explore some plots! choose a Feature to plot from the selectbox in the sidebar')
                st.write(
                    '###### You can switch between chicago and new york to compare plots')

                # Radio button to choose different agg functions
                agg_func = st.radio('**Choose Agg Function**',
                                    ('Mean', 'Sum')).lower()

                fig1 = choose_plot_duration(plot)
                fig2 = choose_plot_count(plot)
                # Splitting the layout to two equal columns
                c1, c2 = st.columns(2)

                # Plotting first plot in first column
                c1.pyplot(fig1)

                # Plotting second plot in first column'
                c2.pyplot(fig2)
