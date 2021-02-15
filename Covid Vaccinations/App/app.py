import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly import tools
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


@st.cache
def load_data():
    a = pd.read_csv('https://raw.githubusercontent.com/asad-mahmood/66DaysOfData/main/Covid%20Vaccinations/country_vaccinations.csv')
    return a

def home_display():
    st.subheader("Dataset Information")
    st.write("This dataset was accquired from [Github](https://github.com/owid/covid-19-data/tree/master/public/data) and is maintained by [Our World in Data.](https://ourworldindata.org/coronavirus) This data is about vaccinations progress in countries all over the world and contains the following information:")

    "+ **Country**- this is the country for which the vaccination information is provided"
    "+ **Country ISO Code** - ISO code for the country"
    "+ **Date**- date for the data entry; for some of the dates we have only the daily vaccinations, for others, only the (cumulative) total"
    "+ **Total number of vaccinations** - this is the absolute number of total immunizations in the country"
    "+ **Total number of people vaccinated** - a person, depending on the immunization scheme, will receive one or more (typically 2) vaccines; at a certain moment, the number of vaccination might be larger than the number of people"
    "+ **Total number of people fully vaccinated** - this is the number of people that received the entire set of immunization according to the immunization scheme (typically 2); at a certain moment in time, there might be a certain number of people that received one vaccine and another number (smaller) of people that received all vaccines in the scheme"
    "+ **Daily vaccinations (raw)** - for a certain data entry, the number of vaccination for that date/country"
    "+ **Daily vaccinations** - for a certain data entry, the number of vaccination for that date/country"
    "+ **Total vaccinations per hundred** - ratio (in percent) between vaccination number and total population up to the date in the country"
    "+ **Total number of people vaccinated per hundred** - ratio (in percent) between population immunized and total population up to the date in the country"
    "+ **Total number of people fully vaccinated per hundred** - ratio (in percent) between population fully immunized and total population up to the date in the country"
    "+ **Number of vaccinations per day** - number of daily vaccination for that day and country"
    "+ **Daily vaccinations per million** - ratio (in ppm) between vaccination number and total population for the current date in the country"
    "+ **Vaccines used in the country** - total number of vaccines used in the country (up to date)"
    "+ **Source name** - source of the information (national authority, international organization, local organization etc.)"
    "+ **Source website** - website of the source of information"

    st.subheader("Objective")
    "This dashboards main focus is to look into these key questions:"

    "1. What vaccination schemes are used in various countries and which scheme is used the most?"
    "2. How many are vaccinated(total and as percent from population)?"
    "3. Daily vaccinations and daily vaccinations per million."
    "4. How the vaccination progressed over time all over the globe?"

def vacScheme(data_df):
    # Grouping data by country and creating a new df
    country_vaccine = data_df.groupby(["country", "iso_code", "vaccines"])['total_vaccinations',
                                                                           'total_vaccinations_per_hundred',
                                                                           'daily_vaccinations',
                                                                           'daily_vaccinations_per_million',
                                                                           'people_vaccinated',
                                                                           'people_vaccinated_per_hundred',
                                                                           'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred'
    ].max().reset_index()

    # Renaming columns of new df
    country_vaccine.columns = ["Country", "iso_code", "Vaccines", "Total vaccinations", "Percent", "Daily vaccinations",
                               "Daily vaccinations per million", "People vaccinated", "People vaccinated per hundred",
                               'People fully vaccinated', 'People fully vaccinated percent']

    vaccines = country_vaccine.Vaccines.unique()
    for v in vaccines:
        countries = country_vaccine.loc[country_vaccine.Vaccines == v, 'Country'].values

    vaccine = data_df.groupby(["vaccines"])['total_vaccinations', 'total_vaccinations_per_hundred',
                                            'daily_vaccinations', 'daily_vaccinations_per_million'].max().reset_index()
    vaccine.columns = ["Vaccines", "Total vaccinations", "Percent", "Daily vaccinations",
                       "Daily vaccinations per million"]

    return vaccine, country_vaccine

def draw_trace_bar_vaccine(data, feature, title, xlab, ylab, color='Blue'):
    data = data.sort_values(feature, ascending=False)
    trace = go.Bar(
        x=data['Vaccines'],
        y=data[feature],
        marker=dict(color=color),
        text=data['Vaccines']
    )
    data = [trace]

    layout = dict(title=title,
                  xaxis=dict(title=xlab, showticklabels=True, tickangle=45,
                             zeroline=True, zerolinewidth=1, zerolinecolor='grey',
                             showline=True, linewidth=2, linecolor='black', mirror=True,
                             tickfont=dict(
                                 size=10,
                                 color='black'), ),
                  yaxis=dict(title=ylab, gridcolor='lightgrey', zeroline=True, zerolinewidth=1,
                             zerolinecolor='grey',
                             showline=True, linewidth=2, linecolor='black', mirror=True),
                  width = 1300, height=800,
                  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)',
                  hovermode='closest'
                  )
    fig = dict(data=data, layout=layout)
    st.plotly_chart(fig)

def draw_trace_bar(data, feature, title, xlab, ylab,color='Blue'):
    data = data.sort_values(feature, ascending=False)
    trace = go.Bar(
            x = data['Country'],
            y = data[feature],
            marker=dict(color=color),
            text=data['Country']
        )
    data = [trace]

    layout = dict(title = title,
              xaxis = dict(title = xlab, showticklabels=True, tickangle=45,
                           zeroline=True, zerolinewidth=1, zerolinecolor='grey',
                           showline=True, linewidth=2, linecolor='black', mirror=True,
                          tickfont=dict(
                            size=10,
                            color='black'),),
              yaxis = dict(title = ylab, gridcolor='lightgrey', zeroline=True, zerolinewidth=1, zerolinecolor='grey',
                          showline=True, linewidth=2, linecolor='black', mirror=True),
              plot_bgcolor = 'rgba(0, 0, 0, 0)', paper_bgcolor = 'rgba(0, 0, 0, 0)',
              hovermode = 'closest'
             )
    fig = dict(data = data, layout = layout)
    st.plotly_chart(fig)

def plot_custom_scatter(df, x, y, size, color, hover_name, title):
    fig = px.scatter(df, x=x, y=y, size=size, color=color,
               hover_name=hover_name, size_max=80, title = title,
                     width = 1600, height=500)
    fig.update_layout({'legend_orientation':'h'})
    fig.update_layout(legend=dict(yanchor="top", y=-0.2))
    fig.update_layout({'legend_title':'Vaccine scheme'})
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='grey')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='grey')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    st.plotly_chart(fig)

def plot_time_variation_countries_group(data_df, feature, title, countries):
    data = []
    for country in countries:
        df = data_df.loc[data_df.Country==country]
        trace = go.Scatter(
            x = df['Date'],y = df[feature],
            name=country,
            mode = "markers+lines",
            marker_line_width = 1,
            marker_size = 8,
            marker_symbol = 'circle',
            text=df['Country'])
        data.append(trace)
    layout = dict(title = title,
          xaxis = dict(title = 'Date', showticklabels=True,zeroline=True, zerolinewidth=1, zerolinecolor='grey',
                       showline=True, linewidth=2, linecolor='black', mirror=True,
                       tickfont=dict(size=10,color='darkblue'),),
          yaxis = dict(title = feature, gridcolor='lightgrey', zeroline=True, zerolinewidth=1, zerolinecolor='grey',
                       showline=True, linewidth=2, linecolor='black', mirror=True, type="log"),
                       plot_bgcolor = 'rgba(0, 0, 0, 0)', paper_bgcolor = 'rgba(0, 0, 0, 0)',
         hovermode = 'x',
         width = 1600, height=800
         )
    fig = dict(data=data, layout=layout)
    st.plotly_chart(fig)
##############################################
############## Web App Title
##############################################
st.set_page_config(page_title='Covid-19 Vaccination Progress',
                   layout='wide')

st.title("Covid-19 Vaccination Progress")
st.write("**Made By: Asad Mahmood**")

########
######## Sidebar
########

st.header('Navigation')
tabs = ('Overview of Project', 'Dataset Report', 'Dashboard')
tab = st.selectbox("",tabs)

df = load_data()

if tab == 'Overview of Project':
    st.header('**Overview of Project**')
    st.subheader('Input DataFrame')
    st.write(df.head())
    home_display()

elif tab == 'Dataset Report':
    st.header("**Exploratory Data Analysis**")
    pr = ProfileReport(df, minimal=True)
    st.header('Input DataFrame')
    st.write(df.head())
    st.write('---')
    st_profile_report(pr)

elif tab == 'Dashboard':
    st.header("**Dashboard**")
    st.subheader("Vaccination Progress All Over Globe")
    vaccine, country_vaccine = vacScheme(df)
    col1, col2 = st.beta_columns((3, 1))

    with col1:
        draw_trace_bar_vaccine(vaccine, 'Total vaccinations', 'Total per vaccine scheme', 'Vaccine', 'Vaccination total', "darkmagenta" )

    with col2:
        "**Some countries are using a mixed vaccination scheme (they are using more than one vaccine).**"

        "The mapping is as following:"
        "* Moderna, Pfizer/BioNTech - **USA**;"
        "* CNBG, Sinovac - **China**;"
        "* Oxford/AstraZeneca, Pfizer/BioNTech', 'Pfizer/BioNTech - **UK**;"
        "* Pfizer/BioNTech - mostly **EU**;"
        "* Pfizer/BioNTech, Sinopharm - **UAE**;"
        "* Sinovac - **Turkey**;"
        "* Covaxin, Covishield - **India**;"

    #####################
    st.subheader("Vaccination Progress Per Countries")
    "To see the vaccination scheme distribution per countries, we will use treemap representations. We look to the total vaccinations, to daily vaccinations values as well as total people vaccinated."
    "NOTE: click on a treemap item to navigate down the tree structure and expand the current branch."
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        fig1 = px.treemap(country_vaccine, path=['Vaccines', 'Country'], values='Total vaccinations',
                          title = 'Total vaccinations per country, grouped by vaccine scheme')
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.treemap(country_vaccine, path=['Vaccines', 'Country'], values='Daily vaccinations',
                          title = 'Daily vaccinations per country, grouped by vaccine scheme')
        st.plotly_chart(fig2)
    with col3:
        fig3 = px.treemap(country_vaccine, path=['Vaccines', 'Country'], values='People vaccinated',
                          title = 'People vaccinated per country, grouped by vaccine scheme')
        st.plotly_chart(fig3)

    #####################
    st.subheader("Population Vaccinated")
    "Let's look now to the countries statistics, irrespective to the vaccine scheme. We will look to the top of the countries by:"
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        "- Total number of vaccinations;"
        "- Percent of vaccinations from entire population;"
    with col2:
        "- Daily number of vaccinations;"
        "- Daily number of vaccination per million population;  "
    with col3:
        "- People vaccinated;"
        "- Percent of vaccinated people from entire population."

    col1, col2 = st.beta_columns(2)
    with col1:
        draw_trace_bar(country_vaccine, 'Total vaccinations', 'Vaccination total per country', 'Country',
                       'Vaccination total', "Darkgreen")
    with col2:
        draw_trace_bar(country_vaccine, 'Percent', 'Vaccination percent per country', 'Country', 'Vaccination percent')

    col1, col2 = st.beta_columns(2)
    with col1:
        draw_trace_bar(country_vaccine, 'Daily vaccinations', 'Daily vaccinations per country', 'Country', 'Daily vaccinations', "red" )
    with col2:
        draw_trace_bar(country_vaccine, 'Daily vaccinations per million', 'Daily vaccinations per million per country',
                       'Country', \
                       'Daily vaccinations per million', "magenta")

    col1, col2 = st.beta_columns(2)
    with col1:
        draw_trace_bar(country_vaccine, 'People vaccinated', 'People vaccinated per country', 'Country', \
                       'People vaccinated', "lightblue")
    with col2:
        draw_trace_bar(country_vaccine, 'People vaccinated per hundred', 'People vaccinated per hundred per country',
                       'Country', \
                       'People vaccinated per hundred', "orange")

    #####################
    st.subheader("Vaccination Grouped per Country and Vaccination Schemes")
    plot_custom_scatter(country_vaccine, x="Total vaccinations", y="Percent", size="Total vaccinations",
                        color="Vaccines",
                        hover_name="Country",
                        title="Vaccinations (Percent vs. total), grouped per country and vaccines")

    plot_custom_scatter(country_vaccine, x="Total vaccinations", y="Daily vaccinations", size="Total vaccinations",
                        color="Vaccines",
                        hover_name="Country", title="Vaccinations (Total vs. Daily) grouped per country and vaccines")

    plot_custom_scatter(country_vaccine, x="Percent", y="Daily vaccinations per million", size="Total vaccinations",
                        color="Vaccines",
                        hover_name="Country",
                        title="Vaccinations (Daily / million vs. Percent) grouped per country and vaccines")
    #####################
    st.subheader("Vaccination GeoPlots")
    col1, col2 = st.beta_columns(2)
    with col1:
        trace = go.Choropleth(
            locations=country_vaccine['Country'],
            locationmode='country names',
            z=country_vaccine['Total vaccinations'],
            text=country_vaccine['Country'],
            autocolorscale=False,
            reversescale=True,
            colorscale='viridis',
            marker=dict(
                line=dict(
                    color='rgb(0,0,0)',
                    width=0.5)
            ),
            colorbar=dict(
                title='Total vaccinations',
                tickprefix='')
        )

        data = [trace]
        layout = go.Layout(
            title='Total vaccinations per country',
            geo=dict(
                showframe=True,
                showlakes=False,
                showcoastlines=True,
                projection=dict(
                    type='natural earth'
                )
            )
        )

        fig = dict(data=data, layout=layout)
        st.plotly_chart(fig)
        with col2:
            trace = go.Choropleth(
                locations=country_vaccine['Country'],
                locationmode='country names',
                z=country_vaccine['Percent'],
                text=country_vaccine['Country'],
                autocolorscale=False,
                reversescale=True,
                colorscale='viridis',
                marker=dict(
                    line=dict(
                        color='rgb(0,0,0)',
                        width=0.5)
                ),
                colorbar=dict(
                    title='Percent',
                    tickprefix='')
            )

            data = [trace]
            layout = go.Layout(
                title='Total vaccinations per hundred per country',
                geo=dict(
                    showframe=True,
                    showlakes=False,
                    showcoastlines=True,
                    projection=dict(
                        type='natural earth'
                    )
                )
            )

            fig = dict(data=data, layout=layout)
            st.plotly_chart(fig)

    col1, col2 = st.beta_columns(2)
    with col1:
        trace = go.Choropleth(
            locations=country_vaccine['Country'],
            locationmode='country names',
            z=country_vaccine['Daily vaccinations'],
            text=country_vaccine['Country'],
            autocolorscale=False,
            reversescale=True,
            colorscale='viridis',
            marker=dict(
                line=dict(
                    color='rgb(0,0,0)',
                    width=0.5)
            ),
            colorbar=dict(
                title='Daily vaccinations',
                tickprefix='')
        )

        data = [trace]
        layout = go.Layout(
            title='Daily vaccinations per country',
            geo=dict(
                showframe=True,
                showlakes=False,
                showcoastlines=True,
                projection=dict(
                    type='natural earth'
                )
            )
        )

        fig = dict(data=data, layout=layout)
        st.plotly_chart(fig)
    with col2:
        trace = go.Choropleth(
            locations=country_vaccine['Country'],
            locationmode='country names',
            z=country_vaccine['Daily vaccinations per million'],
            text=country_vaccine['Country'],
            autocolorscale=False,
            reversescale=True,
            colorscale='viridis',
            marker=dict(
                line=dict(
                    color='rgb(0,0,0)',
                    width=0.5)
            ),
            colorbar=dict(
                title='Daily vaccinations per million',
                tickprefix='')
        )

        data = [trace]
        layout = go.Layout(
            title='Daily vaccinations per million per country',
            geo=dict(
                showframe=True,
                showlakes=False,
                showcoastlines=True,
                projection=dict(
                    type='natural earth'
                )
            )
        )

        fig = dict(data=data, layout=layout)
        st.plotly_chart(fig)
    col1, col2 = st.beta_columns(2)
    with col1:
        trace = go.Choropleth(
            locations=country_vaccine['Country'],
            locationmode='country names',
            z=country_vaccine['People vaccinated'],
            text=country_vaccine['Country'],
            autocolorscale=False,
            reversescale=True,
            colorscale='viridis',
            marker=dict(
                line=dict(
                    color='rgb(0,0,0)',
                    width=0.5)
            ),
            colorbar=dict(
                title='People vaccinated',
                tickprefix='')
        )

        data = [trace]
        layout = go.Layout(
            title='People vaccinated per country',
            geo=dict(
                showframe=True,
                showlakes=False,
                showcoastlines=True,
                projection=dict(
                    type='natural earth'
                )
            )
        )

        fig = dict(data=data, layout=layout)
        st.plotly_chart(fig)
    with col2:
        trace = go.Choropleth(
            locations=country_vaccine['Country'],
            locationmode='country names',
            z=country_vaccine['People vaccinated per hundred'],
            text=country_vaccine['Country'],
            autocolorscale=False,
            reversescale=True,
            colorscale='viridis',
            marker=dict(
                line=dict(
                    color='rgb(0,0,0)',
                    width=0.5)
            ),
            colorbar=dict(
                title='People vaccinated per hundred',
                tickprefix='')
        )

        data = [trace]
        layout = go.Layout(
            title='People vaccinated per hundred per country',
            geo=dict(
                showframe=True,
                showlakes=False,
                showcoastlines=True,
                projection=dict(
                    type='natural earth'
                )
            )
        )

        fig = dict(data=data, layout=layout)
        st.plotly_chart(fig)

    #####################
    st.subheader("How the vaccination progressed overtime?")
    "1) Let's look to the way the vaccination progressed."
    "2) We will look to the values of total vaccination and daily vaccination."

    country_vaccine_time = df[["country", "vaccines", "date", 'total_vaccinations',
                                    'total_vaccinations_per_hundred', 'people_vaccinated',
                                    'people_vaccinated_per_hundred',
                                    'daily_vaccinations', 'daily_vaccinations_per_million',
                                    'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred'
                                    ]].dropna()
    country_vaccine_time.columns = ["Country", "Vaccines", "Date", 'Total vaccinations', 'Percent', 'People vaccinated',
                                    'People percent',
                                    "Daily vaccinations", "Daily vaccinations per million",
                                    'People fully vaccinated', 'People fully vaccinated percent']

    countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland',
                 'France', 'Germany',
                 'Greece', 'Hungary', 'Ireland', 'Israel', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
                 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovakia', 'Spain', 'Sweden',
                 'United Kingdom', 'United States', 'China']


    plot_time_variation_countries_group(country_vaccine_time, 'Percent',
                                        'Total vaccination percent evolution (selected countries, log scale)',
                                        countries)

    plot_time_variation_countries_group(country_vaccine_time, 'Total vaccinations',
                                        'Total vaccination evolution (selected countries, log scale)', countries)

    plot_time_variation_countries_group(country_vaccine_time, 'People percent',
                                        'People vaccinated percent evolution (selected countries, log scale)',
                                        countries)
    plot_time_variation_countries_group(country_vaccine_time, 'People vaccinated',
                                        'People vaccinated evolution (selected countries, log scale)', countries)

    plot_time_variation_countries_group(country_vaccine_time, 'Daily vaccinations',
                                        'Daily vaccinations evolution (selected countries, log scale)', countries)

    plot_time_variation_countries_group(country_vaccine_time, 'Daily vaccinations per million',
                                        'Daily vaccinations per million evolution (selected countries, log scale)',
                                        countries)

    plot_time_variation_countries_group(country_vaccine_time, 'People fully vaccinated percent',
                                        'People fully vaccinated percent evolution (selected countries, log scale)',
                                        countries)

    plot_time_variation_countries_group(country_vaccine_time, 'People fully vaccinated',
                                        'People fully vaccinated evolution (selected countries, log scale)', countries)
else:
    'Error Not Found'