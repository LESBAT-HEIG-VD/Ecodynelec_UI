import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots




colors = ['#006749', '#40A578', '#9DDE8B', '#E3E790', '#54DEFD',
          '#D7B49E', '#EE964B', '#583E23', '#8E9DCC', '#D00000']




ordered_countries = ['CH', 'DE', 'FR', 'AT', 'IT', 'Other']






def create_combined_time_series(flows_df, consumption_df, title, resolution='daily'):
    """
    Crée et affiche un graphique de séries temporelles pour les flux et la consommation totale,
    avec prise en charge des résolutions quotidienne et horaire.

    Args:
    - flows_df (pd.DataFrame): DataFrame contenant les données des flux.
    - consumption_df (pd.Series): Série contenant les données de consommation totale.
    - title (str): Titre du graphique.
    - resolution (str): La résolution temporelle des données ('daily' ou 'hourly').
    """
    # Keep the datetime index intact
    flows_df.index = pd.to_datetime(flows_df.index)

    # Adjust the formatting for the hovertemplate and tick format based on resolution
    if resolution == 'daily':
        # Daily resolution formatting
        hovertemplate_format = '%a %d %b %y'
        tickformat = '%a %d %b %y'
    elif resolution == 'hourly':
        # Hourly resolution formatting
        hovertemplate_format = '%H:%M<br>%a %d %b %y'
        tickformat = '%a %d %b %y %H:%M'

    # Create the graph with Graph Objects
    fig = go.Figure()

    # Add trace for production
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['production'], mode='lines', name='Production',
                             hovertemplate=f'%{{fullData.name}}: %{{y:.0f}} GWh<br>Date: %{{x|{hovertemplate_format}}}<extra></extra>'))

    # Add trace for imports
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['imports'], mode='lines', name='Imports',
                             hovertemplate=f'%{{fullData.name}}: %{{y:.0f}} GWh<br>Date: %{{x|{hovertemplate_format}}}<extra></extra>'))

    # Add trace for exports
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['exports'], mode='lines', name='Exports',
                             hovertemplate=f'%{{fullData.name}}: %{{y:.0f}} GWh<br>Date: %{{x|{hovertemplate_format}}}<extra></extra>'))

    # Add trace for total consumption
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['total_consumption'], mode='lines', name='Total Consumption',
                             hovertemplate=f'%{{fullData.name}}: %{{y:.0f}} GWh<br>Date: %{{x|{hovertemplate_format}}}<extra></extra>'))

    # Update layout and axes
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Quantity (GWh)',
        legend_title='Series',
        legend=dict(x=0.5, y=-0.7, xanchor='center', yanchor='top', orientation='h'),xaxis=dict(
            tickangle=45,  # Increase tick angle for better readability
            nticks=10  # Reduce the number of ticks to avoid overcrowding
        )
    )

    # Format the x-axis based on resolution
    fig.update_xaxes(title_text='',tickformat=tickformat, tickangle=45)

    fig.update_yaxes(title='', rangemode='tozero')

    # Add annotation for unit
    fig.add_annotation(text="GWh", xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False, font=dict(size=12))

    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.6,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')

    # Display the graph in Streamlit
    st.plotly_chart(fig)



def create_area_chart(dataframe, title, unit="GWh", resolution="daily"):
    """
    Crée et affiche un graphique en aires avec des données spécifiées.

    Args:
    - dataframe (pd.DataFrame): DataFrame contenant les données à tracer.
    - title (str): Titre du graphique.
    - unit (str): Unité pour l'affichage dans le hovertemplate (par défaut: 'GWh').
    - resolution (str): La résolution temporelle des données ('daily' ou 'hourly').
    """
    # Define the color palette
    colors = px.colors.qualitative.Alphabet

    # Ensure the index is in datetime format
    dataframe.index = pd.to_datetime(dataframe.index)

    # Adjust the formatting for the hovertemplate and tick format based on resolution
    if resolution == 'daily':
        # Daily resolution formatting
        hovertemplate_format = '%a %d %b %y'
        tickformat = '%a %d %b %y'
    elif resolution == 'hourly':
        # Hourly resolution formatting
        hovertemplate_format = '%H:%M<br>%a %d %b %y'
        tickformat = '%a %d %b %y %H:%M'

    # Define ordered_countries list (Make sure these columns exist in the dataframe)
    ordered_countries = ['CH', 'DE', 'FR', 'AT', 'IT', 'Other']

    # Check if all columns in ordered_countries are present in the dataframe
    missing_columns = [col for col in ordered_countries if col not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in the dataframe: {missing_columns}")

    # Create custom hover data based on value conditions
    hover_data = dataframe.copy()
    for col in hover_data.columns:
        hover_data[col] = hover_data[col].apply(lambda x: f'{x:.1e}' if x < 1 else f'{x:.0f}')

    # Create the area chart
    fig = px.area(dataframe, x=dataframe.index, y=ordered_countries,
                  title=title, color_discrete_sequence=colors)

    # Update x and y axes
    fig.update_xaxes(title='', tickformat=tickformat, tickangle=45)  # Update tick format based on resolution
    fig.update_yaxes(title='', rangemode='tozero')

    # Update layout for better readability
    fig.update_layout(
        legend=dict(x=0.7, y=-0.8, xanchor='right', yanchor='top', orientation='h'),
        xaxis=dict(nticks=10),legend_title_text=''  # Reduce the number of ticks to avoid overcrowding
    )

    # Apply the custom hover data (with conditional formatting)
    custom_hovertext = hover_data.apply(
        lambda row: '<br>'.join([f'{col}: {row[col]} {unit}' for col in ordered_countries]), axis=1)

    # Update the hovertemplate to use the custom hovertext and format for the resolution
    fig.update_traces(hovertemplate=custom_hovertext.apply(lambda x: f'{x}<br>Date: %{{x|{hovertemplate_format}}}<extra></extra>'))
    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.6,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    # Add annotation for the unit at the top
    fig.add_annotation(text=f"{unit}", xref="paper", yref="paper", x=-0.05, y=1.1,
                       showarrow=False, font=dict(size=12), xanchor='left', yanchor='top')

    # Display the chart in Streamlit
    st.plotly_chart(fig)





def create_area_mixte(df, title, text="GWh", resolution='daily'):
    """
    Create an area chart to visualize energy consumption data with a custom unit in the hovertemplate.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the energy data.
    - title (str): The title of the chart.
    - text (str): The unit to be displayed in the hovertemplate (default is 'GWh').
    - resolution (str): The time resolution of the data ('daily' or 'hourly').
    """
    # Define the color palette
    colors = px.colors.qualitative.Alphabet

    # Ensure the index is in datetime format
    df.index = pd.to_datetime(df.index)

    # Adjust the formatting for the hovertemplate and tick format based on resolution
    if resolution == 'daily':
        # Daily resolution formatting
        hovertemplate_format = '%a %d %b %y'
        tickformat = '%a %d %b %y'
    elif resolution == 'hourly':
        # Hourly resolution formatting
        hovertemplate_format = ' %a %d %b %y %H:%M'
        tickformat = '%a %d %b %y %H:%M'

    # Create a new DataFrame for the custom hover data based on the condition
    hover_data = df.copy()
    for col in hover_data.columns:
        hover_data[col] = hover_data[col].apply(lambda x: f'{x:.1e}' if x < 1 else f'{x:.0f}')

    # Create the area chart
    fig = px.area(df, x=df.index, y=df.columns, title=title, color_discrete_sequence=colors)

    # Update layout and add annotations
    fig.update_layout(
        legend=dict(x=1, y=-0.7, xanchor='right', yanchor='top', orientation='h'),  # Move legend to the bottom
        xaxis=dict(
            tickangle=45,  # Increase tick angle for better readability
            nticks=10,  # Reduce the number of ticks to avoid overcrowding
            tickformat=tickformat  # Set the tick format based on the resolution
        ),
        coloraxis_colorbar=dict(title=text), legend_title_text='' # Dynamic colorbar title based on the unit (text)
    )

    # Use the custom hovertext for each point
    custom_hovertext = hover_data.apply(lambda row: '<br>'.join([f'{col}: {row[col]} {text}' for col in df.columns]), axis=1)

    # Update hovertemplate to show dynamic hover data based on resolution
    fig.update_traces(hovertemplate=custom_hovertext.apply(lambda x: f'{x}<br>Date: %{{x|{hovertemplate_format}}}<extra></extra>'),
                      customdata=hover_data.values)

    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.6,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    # Add annotation for unit
    fig.add_annotation(text=text, xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False, font=dict(size=12))

    # Display the chart in Streamlit
    st.plotly_chart(fig)


# Fonction pour créer le menu d'agrégation
def aggregation_menu(menu_title="Type of Aggregation:"):
    st.write(menu_title)
    selection = option_menu(
        menu_title="",  # Intitulé du menu
        options=["Mixed", "By Technology", "Country of origin"],
        icons=["filter", "cogs", "globe"],
        menu_icon="cast",  # Icône pour le menu
        default_index=0,  # Option par défaut
        orientation="horizontal",  # Affichage horizontal
        styles={
            "container": {"padding": "0", "margin": "0"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff5f5f"},
        }
    )
    return selection




def create_column_mapping(suffix):
    return {
        'Mix_Other': 'Other',
        f'Residual_Hydro_Run-of-river_and_poundage_{suffix}': f'Hydro_run-of-river_{suffix}',
        f'Biomass_{suffix}': f'Biomass_{suffix}',
        f'Fossil_Coal-derived_gas_{suffix}': f'Gas_{suffix}',
        f'Fossil_Oil_{suffix}': f'Oil_{suffix}',
        f'Geothermal_{suffix}': f'Geothermal_{suffix}',
        f'Hydro_Run-of-river_and_poundage_{suffix}': f'Hydro_run-of-river_{suffix}',
        f'Marine_{suffix}': 'Other',
        f'Solar_{suffix}': f'Solar_{suffix}',
        f'Residual_Hydro_Water_Reservoir_{suffix}': f'Hydro_lake_{suffix}',
        f'Residual_Other_{suffix}': f'Other_{suffix}',
        f'Fossil_Brown_coal/Lignite_{suffix}': f'Coal_{suffix}',
        f'Fossil_Gas_{suffix}': f'Gas_{suffix}',
        f'Fossil_Oil_shale_{suffix}': f'Oil_{suffix}',
        f'Hydro_Pumped_Storage_{suffix}': f'Hydro_storage_{suffix}',
        f'Hydro_Water_Reservoir_{suffix}': f'Hydro_lake_{suffix}',
        f'Nuclear_{suffix}': f'Nuclear_{suffix}',
        f'Waste_{suffix}': f'Waste_{suffix}',
        f'Fossil_Hard_coal_{suffix}': f'Coal_{suffix}',
        f'Fossil_Peat_{suffix}': f'Coal_{suffix}',
        f'Other_fossil_{suffix}': 'Other',
        f'Wind_Offshore_{suffix}': f'Wind_{suffix}',
        f'Other_renewable_{suffix}': 'Other',
        f'Wind_Onshore_{suffix}': f'Wind_{suffix}'
    }


def Merge(dict1, dict2, dict3, dict4,dict5):
    res = {**dict1, **dict2, **dict3, **dict4,**dict5}
    return res


mapping_cols = Merge(create_column_mapping('CH'),create_column_mapping('FR'),create_column_mapping('DE'),create_column_mapping('AT'),create_column_mapping('IT'))

# Fonction pour sommer les colonnes se terminant par un suffixe spécifique
def group_by_src(df):

    df = df.rename(columns=mapping_cols)
    df = df.groupby(df.columns, axis=1).sum()

    return df


def sum_columns_with_suffix(df, suffix):
    columns = [col for col in df.columns if col.endswith(f"_{suffix}")]
    return df[columns].sum(axis=1)
Country = {'Switzerland': 'CH', 'France': 'FR', 'Germany': 'DE', 'Austria': 'AT', 'Italy': 'IT'}

def aggregate_by_country(selected_country,selected_df):
    """
        Aggregate data by country using a specified DataFrame and country name.

        Parameters:
            selected_country (str): The country name which corresponds to the suffix to be used.
            selected_df (pd.DataFrame): The DataFrame to be aggregated.

        Returns:
            pd.DataFrame: The aggregated DataFrame with data summed by the relevant country suffix.

        This function first identifies the suffix for the selected country, aggregates the relevant data, and then sums and deletes data for all other countries.
        """
    suffix = Country[selected_country]
    aggregated_data =group_by_src(selected_df)

    # Ajouter les colonnes des autres pays
    for country, code in Country.items():
        if code != suffix:
            aggregated_data[code] = sum_columns_with_suffix(selected_df, code)
            columns_to_delete= [col for col in aggregated_data.columns if col.endswith(f"_{code}")]
            aggregated_data.drop(columns=columns_to_delete, inplace=True)
    return aggregated_data







def process_data_by_month(df, selected_year, country_name, month_dict, aggregation_function):
    """
    Process the dataframe for a specific year and aggregate by country.

    Parameters:
        df (pd.DataFrame): Dataframe to be processed.
        selected_year (int): Year to filter the data.
        country_name (str): Country name for specific data aggregation.
        month_dict (dict): Dictionary to map month numbers to month names.
        aggregation_function (function): Function to aggregate data by country.

    Returns:
        pd.DataFrame: Processed dataframe.
    """
    # Filter data for the selected year
    df_filtered = df[df.index.year == selected_year]
    # Resample monthly, sum and convert units
    df_monthly = df_filtered.resample('M').sum() / 1000
    # Aggregate by country
    df_aggregated = aggregation_function(country_name, df_monthly)
    # Remap the index to month names
    df_aggregated.index = df_aggregated.index.month.map(lambda x: month_dict[x])

    return df_aggregated

def process_ghg_data_by_month(df, selected_year, country_name, month_dict, aggregation_function):

    # Filter data for the selected year
    df_filtered = df[df.index.year == selected_year]
    # Resample monthly, sum and convert units
    df_monthly = df_filtered.resample('M').mean()
    # Aggregate by country
    df_aggregated = aggregation_function(country_name, df_monthly)
    # Remap the index to month names
    df_aggregated.index = df_aggregated.index.month.map(lambda x: month_dict[x])

    return df_aggregated




def create_pivot_table(df, timestamp_col='Date', value_col='sum'):
    """
    Create a pivot table from a DataFrame by splitting a timestamp column into date and time.

    Parameters:
        df (pd.DataFrame): The DataFrame to process.
        timestamp_col (str): The name of the column containing the timestamp data.
        value_col (str): The column name which contains the values to be summed.

    Returns:
        pd.DataFrame: A pivot table with dates as index, hours as columns, and sums of values.
    """
    df = df.reset_index()


    # Extract date and time into separate columns
    df['D'] = df[timestamp_col].dt.date
    df['Hour'] = df[timestamp_col].dt.time

    df=df[['D', 'Hour'] + df.columns.tolist()[1:-2]]

    # Create the pivot table, handling missing data by filling with 0
    pivot_table = df.pivot_table(values=value_col, index='D', columns='Hour', aggfunc='sum', fill_value=0)

    return pivot_table

def create_heatmap(pivot_table, title):
    """
        Create a heatmap visualization from a pivot table.

        Parameters:
            pivot_table (pd.DataFrame): A pivot table with dates as rows, hours as columns, and aggregated data.
            title (str): The title of the heatmap.

        This function uses Plotly's imshow function to create a heatmap, which is then displayed using Streamlit.
        """

    fig = px.imshow(pivot_table.T, color_continuous_scale='Viridis')
    fig.update_layout(title=title, legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'),
                      xaxis=dict(tickangle=30), coloraxis_colorbar=dict(title='gCO2eq/kWh'))
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    #fig.update_traces(hovertemplate='%{y:.0f} gCO2eq/kWh<br>Date: %{x}<extra></extra>')
    # Apply hovertemplate to round hover values
    fig.update_traces(hovertemplate='%{z:.0f} gCO2eq/kWh<br>Date: %{x}<br>Hour: %{y}<extra></extra>')

    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.25,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    # Show the figure
    st.plotly_chart(fig)

#def create_heatmap(pivot_table, title):
#    """
#    Create a heatmap visualization from a pivot table.
#
#    Parameters:
#        pivot_table (pd.DataFrame): A pivot table with dates as rows, hours as columns, and aggregated data.
#        title (str): The title of the heatmap.
#
#    This function uses Plotly's imshow function to create a heatmap, which is then displayed using Streamlit.
#    """
#
#    # Ensure the index is in datetime format
#    pivot_table.index = pd.to_datetime(pivot_table.index)
#
#    # Format the x-axis labels to include the day name
#    x_labels = pivot_table.index.strftime('%a %d %b  %y ')
#
#    # Create the heatmap using Plotly Express
#    fig = px.imshow(pivot_table.T, x=x_labels, color_continuous_scale='Viridis')
#
#    # Update layout to make the x-axis wider
#    fig.update_layout(
#        title=title,
#        legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'),
#        xaxis=dict(
#            tickangle=45,  # Increase tick angle for better readability
#            nticks=10  # Reduce the number of ticks to avoid overcrowding
#        ),  # Keep the tick angle to prevent overlap
#        coloraxis_colorbar=dict(title='gCO2eq/kWh')
#    )
#
#    # Update the x-axis and y-axis titles
#    fig.update_xaxes(title='')
#    fig.update_yaxes(title='', rangemode='tozero')
#
#    # Apply hovertemplate to round hover values and show both date and hour
#    fig.update_traces(hovertemplate='%{z:.0f} gCO2eq/kWh<br>Date: %{x}<br>Hour: %{y}<extra></extra>')
#
#    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0.5, y=-0.2,
#                       showarrow=False, font=dict(size=12, color="gray"), xanchor='center')
#
#    # Display the heatmap in Streamlit
#    st.plotly_chart(fig)



def bar_group_consumption(df, title, y_cols, text="", barmode=""):
    """
        Create a grouped or stacked bar chart to visualize consumption data.

        Parameters:
            df (pd.DataFrame): DataFrame containing the data to plot.
            title (str): The title of the bar chart.
            y_cols (list): List of column names in df that contain the data to be plotted.
            text (str): Annotation text to add additional information.
            barmode (str): Mode of the bar chart, 'group' or 'stack'.

        This function uses Plotly to create the bar chart and Streamlit to display it.
        """

    # Create the bar chart using Plotly Express
    fig = px.bar(df, x=df.index, y=y_cols,
                 barmode=barmode, title=title,
                 color_discrete_sequence=colors)
    # Update the hover template to round to 0 decimal places and include custom text
    hovertemplate = '%{fullData.name}: %{y:.0f} ' + text + '<br>Date: %{x}<extra></extra>'
    fig.update_traces(hovertemplate=hovertemplate)

    #fig = px.bar(df, x=df.index, y=y_cols,
    #             barmode=barmode, title=title)
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text=text, xref="paper", yref="paper", x=-0.05, y=1.07, showarrow=False, font=dict(size=12))
    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.2,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    fig.update_layout(legend_title_text='',legend=dict(x=0.5, y=-0.2,xanchor='center',  yanchor='top',  orientation='h'  ),margin=dict(l=40, r=40, t=40, b=50) )
    st.plotly_chart(fig)

def bar_group_ghg(df, title):
    """
        Create a bar chart to visualize greenhouse gas emissions data by category.

        Parameters:
            df (pd.DataFrame): DataFrame containing the data.
            title (str): The title of the bar chart.

        This function creates a bar chart using Plotly and displays it using Streamlit.
        """
    fig = px.bar(df, x=df.index, y=df,title=title,color_discrete_sequence=colors)
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text="gCO2eq/kWh", xref="paper", yref="paper", x=-0.05, y=1.05, showarrow=False,
                       font=dict(size=12))
    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.2,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    fig.update_traces(hovertemplate='%{y:.0f} gCO2eq/KWh<br>Date: %{x}<extra></extra>')
    st.plotly_chart(fig)



def bar_consumption(df,title):
    """
        Create a bar chart to visualize energy consumption data.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the energy data, with indices representing categories or time and columns for data values.
            title (str): The title of the bar chart.

        This function generates a bar chart using Plotly and displays it via Streamlit, focusing on energy consumption measured in GWh.
        """
    colors = px.colors.qualitative.Alphabet
    fig = px.bar(df, x=df.index,y=df.columns,title=title,color_discrete_sequence=colors)
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text="GWh", xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False,font=dict(size=12))
    fig.update_layout(legend_title_text='',legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'))
    # Update hovertemplate to round values to 0 decimal places
    fig.update_traces(hovertemplate='%{fullData.name}: %{y:.0f} GWh<br>%{x}<extra></extra>')
    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.2,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    st.plotly_chart(fig)

def bar_ghg(df,title):
    """
        Create a bar chart to visualize greenhouse gas emissions data.

        Parameters:
            df (pd.DataFrame): The DataFrame containing emissions data, with indices as categories or time and columns for data values.
            title (str): The title of the bar chart.

        This function creates a bar chart focusing on GHG emissions per kWh, using Plotly for visualization and Streamlit for display.
        """
    colors = px.colors.qualitative.Alphabet
    fig = px.bar(df, x=df.index, y=df.columns, title=title, color_discrete_sequence=colors)
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text="gCO2eq/kWh", xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False,font=dict(size=12))
    fig.update_layout(legend_title_text='',legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'))
    fig.update_traces(hovertemplate='%{fullData.name}: %{y:.0f} gCO2eq/kWh<br>%{x}<extra></extra>')
    fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.2,
                       showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
    st.plotly_chart(fig)


def download_data_as_csv(dataframe, file_name):
    # Convertir le DataFrame en CSV
    data_as_csv = dataframe.to_csv(index=True).encode("utf-8")

    # Créer le bouton de téléchargement pour le fichier CSV
    st.download_button(
        label="Download data as CSV",
        data=data_as_csv,
        file_name=file_name,
        mime="text/csv"
    )



def create_line_plot(df, title, country_name):
    """
    Create a line plot to visualize GHG emissions over time.

    Args:
    - df (pd.DataFrame): The DataFrame containing the data to be plotted.
    - y_col (str): The column name in the DataFrame to be used for the y-axis.
    - title (str): The title of the plot.
    - country_name (str): The name of the selected country to include in the title.
    """
    # Create a line plot using Plotly Express
    fig = px.line(df.resample('H').mean(), x=df.index,
                  title=f'{title} in {country_name}')

    # Update layout: Remove legend and axis titles
    fig.update_layout(legend_title_text='', title_x=0.5)  # Center title (optional)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')

    # Display the plot in Streamlit
    st.plotly_chart(fig)
