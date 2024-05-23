import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots









def create_combined_time_series(flows_df, consumption_df, title):
    """
    Crée et affiche un graphique de séries temporelles  pour les flux et la consommation totale.

    Args:
    - flows_df (pd.DataFrame): DataFrame contenant les données annuelles des flux.
    - consumption_df (pd.Series): Série contenant les données annuelles de consommation totale.
    - title (str): Titre du graphique.
    """

    # Création du graphique avec Graph Objects
    fig = go.Figure()

    # Ajout des séries de données des flux
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['production'], mode='lines', name='Production'))
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['imports'], mode='lines', name='Imports'))
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['exports'], mode='lines', name='Exports'))
    fig.add_trace(go.Scatter(x=flows_df.index, y=flows_df['total_consumption'], mode='lines', name='total_consumption'))
    # Ajout de la série de données de consommation totale
    fig.add_trace(go.Scatter(x=consumption_df.index, y=consumption_df, mode='lines', name='Total Consumption'))

    # Mise à jour des axes et du layout
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Quantity',
        legend_title='Series'
    )

    fig.update_layout(legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'),
                      xaxis=dict(tickangle=30))


    fig.update_xaxes(title='',range=[flows_df.index.min(), flows_df.index.max()])
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text="GWh", xref="paper", yref="paper", x=-0.05, y=1.05, showarrow=False, font=dict(size=12))

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

def create_area_chart(dataframe,   title):
    """
    Crée et affiche un graphique en aires avec des données spécifiées.

    Args:
    - dataframe (pd.DataFrame): DataFrame contenant les données à tracer.
    - x_column (str): Nom de la colonne pour l'axe des abscisses.
    - y_columns (list): Liste des noms de colonnes pour l'axe des ordonnées.
    - colors (list): Liste des couleurs correspondant aux colonnes y.
    - title (str): Titre du graphique.
    - legend_title (str): Titre de la légende.
    - xaxis_title (str): Titre pour l'axe X.
    - yaxis_title (str): Titre pour l'axe Y.
    """
    # Supposons que flows_selected_df est déjà défini et correctement configuré
    colors = px.colors.qualitative.Alphabet
    # Création du graphique en aires
    fig = px.area(dataframe, x=dataframe.index, y=ordered_countries,
                  title=title,color_discrete_sequence=colors)


    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.update_layout(legend=dict(x=0.7, y=-0.2, xanchor='right', yanchor='top', orientation='h'))

    # Affichage du graphique dans Streamlit
    st.plotly_chart(fig)


def create_area_mixte(df,title,text=""):
    """
        Create an area chart to visualize energy consumption data over time.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the energy data, with the index typically representing time and columns representing data values.
            title (str): The title of the area chart.

        The function generates an area chart using Plotly, emphasizing changes in energy consumption over time by displaying the cumulative area under the curve for each category.
        """
    colors = px.colors.qualitative.Alphabet
    fig = px.area(df, x=df.index,y=df.columns,title=title,color_discrete_sequence=colors)
    fig.update_layout(legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'),
                      xaxis=dict(tickangle=30), coloraxis_colorbar=dict(title='gCO2eq/kWh'))
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text=text, xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False, font=dict(size=12))

    st.plotly_chart(fig)









# Fonction pour créer le menu d'agrégation
def aggregation_menu(menu_title="Type d'Agrégation:"):
    st.write(menu_title)
    selection = option_menu(
        menu_title="",  # Intitulé du menu
        options=["Mixte", "Technologie", "Pays d'origine"],
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


def Merge(dict1, dict2, dict3, dict4):
    res = {**dict1, **dict2, **dict3, **dict4}
    return res


mapping_cols = Merge(create_column_mapping('CH'),create_column_mapping('FR'),create_column_mapping('DE'),create_column_mapping('AT'))

# Fonction pour sommer les colonnes se terminant par un suffixe spécifique
def group_by_src(df):

    df = df.rename(columns=mapping_cols)
    df = df.groupby(df.columns, axis=1).sum()

    return df


def sum_columns_with_suffix(df, suffix):
    columns = [col for col in df.columns if col.endswith(f"_{suffix}")]
    return df[columns].sum(axis=1)
Country= {'Suisse' : 'CH', 'France' : 'FR', 'Allemagne' : 'DE', 'Autriche' : 'AT','Italie':'IT'}
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
    # Show the figure
    st.plotly_chart(fig)


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

    colors =[ '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
     '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    # Create the bar chart using Plotly Express
    fig = px.bar(df, x=df.index, y=y_cols,
                 barmode=barmode, title=title,
                 color_discrete_sequence=colors)


    #fig = px.bar(df, x=df.index, y=y_cols,
    #             barmode=barmode, title=title)
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text=text, xref="paper", yref="paper", x=-0.05, y=1.07, showarrow=False, font=dict(size=12))
    fig.update_layout(legend=dict(x=0.5, y=-0.2,xanchor='center',  yanchor='top',  orientation='h'  ),margin=dict(l=40, r=40, t=40, b=50) )
    st.plotly_chart(fig)

def bar_group_ghg(df, title):
    """
        Create a bar chart to visualize greenhouse gas emissions data by category.

        Parameters:
            df (pd.DataFrame): DataFrame containing the data.
            title (str): The title of the bar chart.

        This function creates a bar chart using Plotly and displays it using Streamlit.
        """
    fig = px.bar(df, x=df.index, y=df,title=title)
    fig.update_xaxes(title='')
    fig.update_yaxes(title='', rangemode='tozero')
    fig.add_annotation(text="gCO2eq/kWh", xref="paper", yref="paper", x=-0.05, y=1.05, showarrow=False,
                       font=dict(size=12))
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
    fig.update_layout(legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'))
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
    fig.update_layout(legend=dict(x=1, y=-0.2, xanchor='right', yanchor='top', orientation='h'))
    st.plotly_chart(fig)

