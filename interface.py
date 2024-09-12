import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots
from functions import create_combined_time_series
from functions import (create_area_chart, create_combined_time_series, create_area_mixte, aggregation_menu,
                       create_column_mapping, group_by_src, sum_columns_with_suffix, aggregate_by_country,
                       process_data_by_month, create_pivot_table, create_heatmap, bar_group_consumption,

                       bar_group_ghg,process_ghg_data_by_month, bar_consumption, bar_ghg,download_data_as_csv)


# Configuration de la page Streamlit
st.set_page_config(page_title="Ecodynelec", page_icon=":bar_chart:", layout="wide")

# Create three columns, and place the logo in the rightmost column
logocol1, logocol2, logocol3 = st.columns([1, 8, 1])  # You can adjust these ratios to fit your needs

# Place the logo in the right column (col3)
with logocol1:
    st.image('data/Logo_colored_variant.png', use_column_width=False,width=300)  # Set the logo to fit the column width
with logocol3:
    st.image('data/IE_HEIG-VD_logotype_rouge_rvb.svg', use_column_width=True)




# Sidebar Menu with Main Options
with st.sidebar:
    main_option = option_menu(
        menu_title="Main Menu",  # Main menu title
        options=["Mix data", "Applications", "Methodology"],  # Main menu options
        icons=["database", "layers", "gear", "info-circle"],  # Optional icons
        menu_icon="cast",  # Main menu icon
        default_index=0,  # Default active index
    )

    if main_option == "Applications":
        applications_option = option_menu(
            menu_title="Applications",  # Applications submenu
            options=["Bâtiment", "PAC"],  # Submenu options
            icons=["building", "plug"],  # Submenu icons
            menu_icon="apps",  # Submenu icon
            default_index=0,
            orientation="vertical"
        )
    else:
        applications_option = None



#Données flows
flows_FR = pd.read_csv("./data/flows/flows_FR.csv")
flows_DE = pd.read_csv("./data/flows/flows_DE.csv")
flows_AT = pd.read_csv("./data/flows/flows_AT.csv")
flows_CH = pd.read_csv("./data/flows/flows_CH.csv")
flows_IT = pd.read_csv("./data/flows/flows_IT.csv")

#Données de consommation totale
tot_consumption_FR=pd.read_csv("./data/consumptions/tot_consumption_FR.csv")
tot_consumption_DE=pd.read_csv("./data/consumptions/tot_consumption_DE.csv")
tot_consumption_AT=pd.read_csv("./data/consumptions/tot_consumption_AT.csv")
tot_consumption_CH=pd.read_csv("./data/consumptions/tot_consumption_CH.csv")
tot_consumption_IT=pd.read_csv("./data/consumptions/tot_consumption_IT.csv")
#Données de consommation by src
raw_consumption_by_src_FR=pd.read_csv("./data/consumptions/raw_consumption_by_src_FR.csv")
raw_consumption_by_src_DE=pd.read_csv("./data/consumptions/raw_consumption_by_src_DE.csv")
raw_consumption_by_src_AT=pd.read_csv("./data/consumptions/raw_consumption_by_src_AT.csv")
raw_consumption_by_src_CH=pd.read_csv("./data/consumptions/raw_consumption_by_src_CH.csv")
raw_consumption_by_src_IT=pd.read_csv("./data/consumptions/raw_consumption_by_src_IT.csv")
#electricity_mixs
tot_electricity_mix_CH=pd.read_csv("./data/electricity_mixs/electricity_mix_CH.csv")
tot_electricity_mix_AT=pd.read_csv("./data/electricity_mixs/electricity_mix_AT.csv")
tot_electricity_mix_DE=pd.read_csv("./data/electricity_mixs/electricity_mix_DE.csv")
tot_electricity_mix_FR=pd.read_csv("./data/electricity_mixs/electricity_mix_FR.csv")
tot_electricity_mix_IT=pd.read_csv("./data/electricity_mixs/electricity_mix_IT.csv")
#electricity_impacts
tot_electricity_impact_CH=pd.read_csv("./data/electricity_impacts/electricity_impact_CH.csv")
tot_electricity_impact_AT=pd.read_csv("./data/electricity_impacts/electricity_impact_AT.csv")
tot_electricity_impact_DE=pd.read_csv("./data/electricity_impacts/electricity_impact_DE.csv")
tot_electricity_impact_FR=pd.read_csv("./data/electricity_impacts/electricity_impact_FR.csv")
tot_electricity_impact_IT=pd.read_csv("./data/electricity_impacts/electricity_impact_IT.csv")

#electricity_impacts
electricity_impact_by_src_CH=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_CH.csv")
electricity_impact_by_src_AT=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_AT.csv")
electricity_impact_by_src_DE=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_DE.csv")
electricity_impact_by_src_FR=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_FR.csv")
electricity_impact_by_src_IT=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_IT.csv")
#by_techno
Techno_FR=pd.read_csv("./data/technologies/technologies_FR.csv")
Techno_AT=pd.read_csv("./data/technologies/technologies_AT.csv")
Techno_DE=pd.read_csv("./data/technologies/technologies_DE.csv")
Techno_CH=pd.read_csv("./data/technologies/technologies_CH.csv")
Techno_IT=pd.read_csv("./data/technologies/technologies_IT.csv")
#by_techno_impact
Techno_impact_FR=pd.read_csv("./data/technologies/Techno_impact_FR.csv")
Techno_impact_AT=pd.read_csv("./data/technologies/Techno_impact_AT.csv")
Techno_impact_DE=pd.read_csv("./data/technologies/Techno_impact_DE.csv")
Techno_impact_CH=pd.read_csv("./data/technologies/Techno_impact_CH.csv")
Techno_impact_IT=pd.read_csv("./data/technologies/Techno_impact_CH.csv")



for df in [flows_FR, flows_DE, flows_AT, flows_CH, tot_consumption_FR, tot_consumption_DE, tot_consumption_AT, tot_consumption_CH,
           tot_electricity_mix_CH,tot_electricity_mix_AT,tot_electricity_mix_DE,tot_electricity_mix_FR,tot_electricity_impact_CH,
           tot_electricity_impact_AT,tot_electricity_impact_DE,tot_electricity_impact_FR,raw_consumption_by_src_FR,raw_consumption_by_src_CH,
           raw_consumption_by_src_DE,raw_consumption_by_src_AT,electricity_impact_by_src_CH,electricity_impact_by_src_AT,
           electricity_impact_by_src_DE,electricity_impact_by_src_FR,Techno_FR,Techno_AT,Techno_DE,Techno_CH,Techno_impact_FR,Techno_impact_AT,
            Techno_impact_DE,Techno_impact_CH,flows_IT,tot_consumption_IT,raw_consumption_by_src_IT,tot_electricity_mix_IT,
           tot_electricity_impact_IT,electricity_impact_by_src_IT,Techno_IT,Techno_impact_IT]:

        df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

for df in [flows_FR, flows_DE, flows_AT, flows_CH,flows_IT]:
    df['total_consumption']=df['production']+df['imports']-df['exports']

# Utilisation de colonnes pour une mise en page personnalisée
col1, col2, col3, col4, col5 = st.columns(5)  # Créer 5 colonnes
years = list(range(2016, 2023))
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

Countries = {'Switzerland': 'CH', 'France': 'FR', 'Germany': 'DE', 'Austria': 'AT','Italy':'IT'}

ordered_countries = ['CH', 'DE', 'FR', 'AT', 'IT', 'Other']
ordered_colors = ['blue','green', 'red', 'purple',  'orange',  'yellow' ]
month_dict = {1: "January", 2: "February", 3: "March", 4: "April",5: "May", 6: "June", 7: "July", 8: "August",9: "September", 10: "October", 11: "November", 12: "December"}



# Dictionary of dataframes with Italy added
dataframes_flows = {'Switzerland': flows_CH,
    'France': flows_FR,
    'Germany': flows_DE,
    'Austria': flows_AT,
    'Italy': flows_IT
}

dataframes_tot_consumption = {
    'Switzerland': tot_consumption_CH,
    'France': tot_consumption_FR,
    'Germany': tot_consumption_DE,
    'Austria': tot_consumption_AT,
    'Italy': tot_consumption_IT
}

dataframes_raw_consumption_by_src = {
    'Switzerland': raw_consumption_by_src_CH,
    'France': raw_consumption_by_src_FR,
    'Germany': raw_consumption_by_src_DE,
    'Austria': raw_consumption_by_src_AT,
    'Italy': raw_consumption_by_src_IT
}

dataframes_tot_electricity_mix = {
    'Switzerland': tot_electricity_mix_CH,
    'France': tot_electricity_mix_FR,
    'Germany': tot_electricity_mix_DE,
    'Austria': tot_electricity_mix_AT,
    'Italy': tot_electricity_mix_IT
}

dataframes_tot_electricity_impact = {
    'Switzerland': tot_electricity_impact_CH,
    'France': tot_electricity_impact_FR,
    'Germany': tot_electricity_impact_DE,
    'Austria': tot_electricity_impact_AT,
    'Italy': tot_electricity_impact_IT
}

dataframes_electricity_impact_by_src = {
    'Switzerland': electricity_impact_by_src_CH,
    'France': electricity_impact_by_src_FR,
    'Germany': electricity_impact_by_src_DE,
    'Austria': electricity_impact_by_src_AT,
    'Italy': electricity_impact_by_src_IT
}

dataframes_techno = {
    'Switzerland': Techno_CH,
    'France': Techno_FR,
    'Germany': Techno_DE,
    'Austria': Techno_AT,
    'Italy': Techno_IT
}

dataframes_techno_impact = {
    'Switzerland': Techno_impact_CH,
    'France': Techno_impact_FR,
    'Germany': Techno_impact_DE,
    'Austria': Techno_impact_AT,
    'Italy': Techno_impact_IT
}







with col1:
    selected_country_name = st.selectbox('Choose a country:', list(Countries.keys()))

with col2:
    resolution = st.selectbox('Resolution:', ['Annual', 'Monthly','Daily','Hourly'])


# Récupération du DataFrame basé sur le pays sélectionné
tot_consumption_selected_df = dataframes_tot_consumption [selected_country_name]
raw_consumption_by_src_selected_df = dataframes_raw_consumption_by_src [selected_country_name]
flows_selected_df =dataframes_flows[selected_country_name]
tot_electricity_mix_selected_df = dataframes_tot_electricity_mix [selected_country_name]
tot_electricity_impact_selected_df = dataframes_tot_electricity_impact [selected_country_name]
electricity_impact_by_src_selected_df = dataframes_electricity_impact_by_src [selected_country_name]
techno_selected_df=dataframes_techno [selected_country_name]
techno_impact_selected_df=dataframes_techno_impact [selected_country_name]




if main_option == "Mix data":
    if resolution == 'Annual':
        flows_selected_df['exports'] = -flows_selected_df['exports']
        flows_annual_df = flows_selected_df.resample('Y').sum() / 1000
        flows_annual_df.index = flows_annual_df.index.year
        tot_consumption_annual_df = tot_consumption_selected_df['sum'].resample('Y').sum() / 1000

        col1, col2 = st.columns(2)
        with col1:

            bar_group_consumption(flows_annual_df, title=f'Yearly Time Series of Production, Imports, and Exports in {selected_country_name}   ', text="GWh",
                                  y_cols=['total_consumption', 'production', 'imports', 'exports'], barmode='group')
            download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

            # Bouton pour télécharger le CSV dans download_col (gauche)
            with download_col:
                download_data_as_csv(flows_annual_df, f"Yearly_Time_Series_of_Production_Imports_and_Exports_in_{selected_country_name.replace(' ', '_')}.csv")

                # Use an expander to display the general description in info_col (right)
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                            **Chart Description:**  
                                            This bar chart represents the yearly time series of production, imports, exports, and total electricity consumption in **{selected_country_name}**,
                                             measured in gigawatt-hours (GWh), over a period from 2016 to 2022.

                                            **Data Source:** EcoDynElec
                                        """)

        # pour les impacts
        consumer_impact_annual = tot_electricity_impact_selected_df['sum'].resample('Y').mean()
        consumer_impact_annual.index = consumer_impact_annual.index.year
        with col2:
            bar_group_ghg(consumer_impact_annual, f'Yearly average of GHG emissions  in {selected_country_name}')
            download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

            # Bouton pour télécharger le CSV dans download_col (gauche)
            with download_col:
                download_data_as_csv(consumer_impact_annual, f"Yearly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}.csv")

                # Use an expander to display the general description in info_col (right)
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                        **Chart Description:**  
                                                        This bar chart represents the yearly average of greenhouse gas (GHG) emissions in **{selected_country_name}**,
                                                         measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh), from 2016 to 2022.

                                                        **Data Source:** EcoDynElec
                                                    """)




        selection = aggregation_menu()
        if selection == "Mixed":
            raw_consumption_by_src_annual_df = raw_consumption_by_src_selected_df.resample('Y').sum() / 1000
            raw_consumption_by_src_annual_df = aggregate_by_country(selected_country_name,raw_consumption_by_src_annual_df)
            raw_consumption_by_src_annual_df.index = raw_consumption_by_src_annual_df.index.year
            col1, col2 = st.columns(2)
            with col1:

                bar_consumption(raw_consumption_by_src_annual_df,title=f'Yearly consumption by source in {selected_country_name}')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(raw_consumption_by_src_annual_df, f"Yearly_consumption_by_source_in_{selected_country_name.replace(' ', '_')}.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                    **Chart Description:**  
                                                                                                    This stacked bar chart represents the yearly electricity consumption by source in **{selected_country_name}** from 2016 to 2022, measured in gigawatt-hours (GWh).
                                                                                                     Each bar is divided into segments that correspond to different energy sources contributing to the overall electricity consumption.

                                                                                                    **Data Source:** EcoDynElec
                                                                                                """)


            electricity_impact_by_src_annual_df = electricity_impact_by_src_selected_df.resample('Y').mean()
            electricity_impact_by_src_annual_df = aggregate_by_country(selected_country_name,electricity_impact_by_src_annual_df)
            electricity_impact_by_src_annual_df.index = electricity_impact_by_src_annual_df.index.year

            with col2:

                bar_ghg(electricity_impact_by_src_annual_df, f'Yearly average of GHG emissions  in {selected_country_name} by source')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(electricity_impact_by_src_annual_df,  f"Yearly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_by_source.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                                    **Chart Description:**  
                                                                                                                    This stacked bar chart illustrates the yearly average of greenhouse gas (GHG) emissions in **{selected_country_name}** by energy source, measured in grams
                                                                                                                     of CO2 equivalent per kilowatt-hour (gCO2eq/kWh), from 2016 to 2022.
                                                                                                                     Each bar is segmented to show the GHG emissions contribution from various energy sources used in **{selected_country_name}**'s electricity consumption.

                                                                                                                    **Data Source:** EcoDynElec
                                                                                                                """)

        if selection == "By Technology":
            col1, col2 = st.columns(2)

            techno_annual_df = techno_selected_df.resample('Y').sum() / 1000
            techno_annual_df.index = techno_annual_df.index.year
            col1, col2 = st.columns(2)
            with col1:
                #bar_consumption(techno_annual_df,title=f'Yearly consumption of {selected_technologie} in {selected_country_name}')
                bar_group_consumption(techno_annual_df,
                                      title=f'Yearly consumption by technology  in {selected_country_name}',
                                      text="GWh",
                                      y_cols=techno_annual_df.columns,barmode='stack')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(techno_annual_df, f"Yearly_consumption_by_technology_in_{selected_country_name.replace(' ', '_')}.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                        **Chart Description:**  
                                                                        This stacked bar chart represents the yearly electricity consumption by technology in **{selected_country_name}** from 2016 to 2022, measured in gigawatt-hours (GWh).
                                                                         Each bar is divided into segments that correspond to the contributions of various energy technologies to the total electricity consumption.

                                                                        **Data Source:** EcoDynElec
                                                                    """)



            techno_impact_annual_df=techno_impact_selected_df.resample('Y').mean()
            techno_impact_annual_df.index = techno_impact_annual_df.index.year

            with col2:

                bar_group_consumption(techno_impact_annual_df,
                                      title=f'Yearly average of GHG emissions by technology in {selected_country_name}',
                                      text="gCO2eq/kWh",
                                      y_cols=techno_impact_annual_df.columns, barmode='stack')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(techno_impact_annual_df, f"Yearly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_by_technology.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                        **Chart Description:**  
                                                                                        This stacked bar chart represents the yearly average of greenhouse gas (GHG) emissions by technology in **{selected_country_name}** from 2016 to 2022, measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                                                         Each bar is divided into segments representing the GHG emissions contributions from various energy technologies.

                                                                                        **Data Source:** EcoDynElec
                                                                                    """)



        if selection == "Country of origin":
            mix_import_annual = tot_electricity_mix_selected_df.drop(['sum'], axis=1)
            mix_import_annual = mix_import_annual.multiply(tot_consumption_selected_df['sum'], axis='index').resample('Y').sum() / 1000
            mix_import_annual.index = mix_import_annual.index.year



            col1, col2 = st.columns(2)
            with col1:

                bar_group_consumption(mix_import_annual, title=f"Origins of yearly Swiss consumer mix in {selected_country_name}",
                                      text="GWh",
                                      y_cols=ordered_countries, barmode='stack')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(mix_import_annual, f"Origins_of_yearly_Swiss_consumer_mix_in_{selected_country_name.replace(' ', '_')}.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                        **Chart Description:**  
                                                                                                        This stacked bar chart illustrates the origins of the yearly Swiss consumer electricity mix from 2016 to 2022, measured in gigawatt-hours (GWh).
                                                                                                         Each bar is divided into segments representing the contributions of electricity sourced from **{selected_country_name}** and its neighboring countries.

                                                                                                        **Data Source:** EcoDynElec
                                                                                                    """)



            mix_impact_annual = tot_electricity_impact_selected_df.drop(['sum'], axis=1).resample('Y').mean()
            mix_impact_annual.index=mix_impact_annual.index.year
            with col2:

                bar_group_consumption(mix_impact_annual,title=f'Yearly average of GHG emissions  in {selected_country_name} by country',
                                      text="gCO2eq/kWh",y_cols=ordered_countries, barmode='stack')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(mix_impact_annual, f"Yearly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_by_country.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                                        **Chart Description:**  
                                                                                                                        This stacked bar chart represents the yearly average of greenhouse gas (GHG) emissions in **{selected_country_name}** by country from 2016 to 2022, measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                                                                                         The stacked bars show the contributions of GHG emissions from domestic electricity production and imports from neighboring countries.

                                                                                                                        **Data Source:** EcoDynElec
                                                                                                                    """)




    elif resolution == 'Monthly':

        with col3:
            # Utilisation d'un slider pour choisir une année
            selected_year = st.slider('Choose a year:', min_value=min(years), max_value=max(years), value=min(years))

        #flows
        flows_selected_df['exports'] = -flows_selected_df['exports']
        flows_monthly_df = flows_selected_df[(flows_selected_df.index.year == selected_year)]
        flows_monthly_df = flows_monthly_df.resample('M').sum() / 1000
        flows_monthly_df.index = flows_monthly_df.index.month.map(lambda x: month_dict[x])
        #tot_consumption
        tot_consumption_monthly_df = tot_consumption_selected_df[(tot_consumption_selected_df.index.year == selected_year)]
        tot_consumption_monthly_df = tot_consumption_monthly_df['sum'].resample('M').sum() / 1000

        col1, col2 = st.columns(2)
        with col1:

            bar_group_consumption(flows_monthly_df, title=f'Monthly Time Series of Production, Imports, and Exports in {selected_country_name} in {selected_year} ',
                                  text="GWh",
                                  y_cols=['total_consumption', 'production', 'imports', 'exports'], barmode='group')
            download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

            # Bouton pour télécharger le CSV dans download_col (gauche)
            with download_col:
                download_data_as_csv(flows_monthly_df, f"Monthly_Time_Series_of_Production_Imports_and_Exports_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}.csv")

                # Use an expander to display the general description in info_col (right)
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                        **Chart Description:**  
                                                        This bar chart represents the monthly time series of production, imports, exports, and total electricity consumption in **{selected_country_name}**,
                                                         measured in gigawatt-hours (GWh), over a period from 2016 to 2022.

                                                        **Data Source:** EcoDynElec
                                                    """)




            # pour les impacts
        tot_electricity_impact_monthly_df=tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index.year == selected_year)]
        monthly_consumer_impact = tot_electricity_impact_monthly_df['sum'].resample('M').mean()
        monthly_consumer_impact.index = monthly_consumer_impact.index.month.map(lambda x: month_dict[x])
        with col2:

            bar_group_ghg(monthly_consumer_impact, f'Monthly average of GHG emissions  in {selected_country_name} in {selected_year} ')
            download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

            # Bouton pour télécharger le CSV dans download_col (gauche)
            with download_col:
                download_data_as_csv(monthly_consumer_impact, f"Monthly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}.csv")

                # Use an expander to display the general description in info_col (right)
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                    **Chart Description:**  
                                                                    This bar chart represents the monthly average of greenhouse gas (GHG) emissions in **{selected_country_name}**,
                                                                     measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh), from 2016 to 2022.

                                                                    **Data Source:** EcoDynElec
                                                                """)


        selection = aggregation_menu()
        if selection == "Mixed":

            raw_consumption_by_src_monthly_df = process_data_by_month(raw_consumption_by_src_selected_df, selected_year, selected_country_name, month_dict,
                aggregate_by_country)

            electricity_impact_by_src_monthly_df = process_ghg_data_by_month(electricity_impact_by_src_selected_df, selected_year, selected_country_name, month_dict,
                aggregate_by_country)

            col1, col2 = st.columns(2)
            with col1:
                bar_consumption(raw_consumption_by_src_monthly_df,title=f'Monthly consumption by source in {selected_country_name} in {selected_year}')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(raw_consumption_by_src_monthly_df, f"Monthly_consumption_by_source_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                    **Chart Description:**  
                                                                                    This stacked bar chart represents the monthly electricity consumption by source in **{selected_country_name}** from 2016 to 2022, measured in gigawatt-hours (GWh).
                                                                                     Each bar is divided into segments that correspond to different energy sources contributing to the overall electricity consumption.

                                                                                    **Data Source:** EcoDynElec
                                                                                """)

            with col2:
                bar_ghg(electricity_impact_by_src_monthly_df,f'Monthly average of GHG emissions  in {selected_country_name} in {selected_year} by source')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(electricity_impact_by_src_monthly_df, f"Monthly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}_by_source.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                                                    **Chart Description:**  
                                                                                                                                    This stacked bar chart illustrates the monthly average of greenhouse gas (GHG) emissions in **{selected_country_name}** by energy source, measured in grams
                                                                                                                                     of CO2 equivalent per kilowatt-hour (gCO2eq/kWh), from 2016 to 2022.
                                                                                                                                     Each bar is segmented to show the GHG emissions contribution from various energy sources used in **{selected_country_name}**'s electricity consumption.

                                                                                                                                    **Data Source:** EcoDynElec
                                                                                                                                """)

        if selection == "By Technology":

            techno_monthly_df = techno_selected_df.loc[techno_selected_df.index.year == selected_year]
            techno_monthly_df = techno_monthly_df.resample('M').sum() / 1000
            techno_monthly_df.index = techno_monthly_df.index.month.map(lambda x: month_dict[x])
            col1, col2 = st.columns(2)
            with col1:
                bar_consumption(techno_monthly_df,title=f'Monthly consumption by technology in {selected_country_name} in {selected_year}')

                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(techno_monthly_df, f"Monthly_consumption_by_technology_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                        **Chart Description:**  
                                                                                        This stacked bar chart represents the monthly electricity consumption by technology in **{selected_country_name}** from 2016 to 2022, measured in gigawatt-hours (GWh).
                                                                                         Each bar is divided into segments that correspond to the contributions of various energy technologies to the total electricity consumption.

                                                                                        **Data Source:** EcoDynElec
                                                                                    """)

            techno_impact_monthly_df = techno_impact_selected_df.loc[techno_impact_selected_df.index.year == selected_year]
            techno_impact_monthly_df = techno_impact_monthly_df.resample('M').mean()
            techno_impact_monthly_df.index = techno_impact_monthly_df.index.month.map(lambda x: month_dict[x])

            with col2:
                bar_ghg(techno_impact_monthly_df,f'Monthly average  of GHG emissions by technology in {selected_country_name} in {selected_year}')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(techno_impact_monthly_df, f"Monthly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}_by_technology.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                        **Chart Description:**  
                                                                                                        This stacked bar chart represents the monthly average of greenhouse gas (GHG) emissions by technology in **{selected_country_name}** from 2016 to 2022, measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                                                                         Each bar is divided into segments representing the GHG emissions contributions from various energy technologies.

                                                                                                        **Data Source:** EcoDynElec
                                                                                                    """)




        if selection == "Country of origin":
            tot_electricity_mix_monthly_df = tot_electricity_mix_selected_df[(tot_electricity_mix_selected_df.index.year == selected_year)]
            monthly_mix_import = tot_electricity_mix_monthly_df.drop(['sum'], axis=1)
            monthly_mix_import = monthly_mix_import.multiply(tot_consumption_monthly_df, axis='index').resample('M').sum() / 1000
            monthly_mix_import.index = monthly_mix_import.index.month.map(lambda x: month_dict[x])


            col1, col2 = st.columns(2)
            with col1:
                bar_group_consumption(monthly_mix_import,
                                      title=f"Origins of monthly consumer mix by country in {selected_country_name} in {selected_year}",
                                      text="GWh",
                                      y_cols=ordered_countries, barmode='stack')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(monthly_mix_import, f"Monthly_consumption_by_country_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                                        **Chart Description:**  
                                                                                                                        This stacked bar chart illustrates the origins of the monthly Swiss consumer electricity mix from 2016 to 2022, measured in gigawatt-hours (GWh).
                                                                                                                         Each bar is divided into segments representing the contributions of electricity sourced from **{selected_country_name}** and its neighboring countries.

                                                                                                                        **Data Source:** EcoDynElec
                                                                                                                    """)


            tot_electricity_impact_monthly_df = tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index.year == selected_year)]
            monthly_mix_impact = tot_electricity_impact_monthly_df.drop(['sum'], axis=1).resample('M').mean()
            monthly_mix_impact.index = monthly_mix_impact.index.month.map(lambda x: month_dict[x])
            with col2:

                bar_group_consumption(monthly_mix_impact,
                                      title=f'Monthly average of GHG emissions by country  in {selected_country_name} in {selected_year}',
                                      text="gCO2eq/kWh",
                                      y_cols=ordered_countries, barmode='stack')
                download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

                # Bouton pour télécharger le CSV dans download_col (gauche)
                with download_col:
                    download_data_as_csv(monthly_mix_impact, f"Monthly_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}_in_{selected_year}_by_country.csv")

                    # Use an expander to display the general description in info_col (right)
                    with info_col:
                        with st.expander("ℹ️ Chart's Information"):
                            st.write(f"""
                                                                                                                                        **Chart Description:**  
                                                                                                                                        This stacked bar chart represents the monthly average of greenhouse gas (GHG) emissions in **{selected_country_name}** by country from 2016 to 2022, measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                                                                                                         The stacked bars show the contributions of GHG emissions from domestic electricity production and imports from neighboring countries.

                                                                                                                                        **Data Source:** EcoDynElec
                                                                                                                                    """)



    elif resolution == 'Daily':

        # Supposons que flows_selected_df est déjà défini et correctement configuré
        min_date = flows_selected_df.index.min()
        max_date = flows_selected_df.index.max()

        # Positionnement des widgets dans les colonnes si déjà définies
        with col3:  # Exemple de placement dans la colonne
            start_date, end_date = st.date_input(
                "Select a date range:",
                [min_date, max_date],  # Utilisez les extrêmes de l'index comme valeur par défaut
                min_value=min_date,  # Date minimale extraite de l'index
                max_value=max_date,  # Date maximale extraite de l'index
                help="You can select a range within the available dates in the data."
            )
            # Ajustez end_date pour inclure toute la journée
            start_date = pd.Timestamp(start_date)
            end_date = pd.Timestamp(end_date) + pd.Timedelta(days=1, seconds=-1)





        # Filtrer le DataFrame selon la plage sélectionnée
        flows_daily= flows_selected_df.loc[(flows_selected_df.index >= start_date) & (flows_selected_df.index <= end_date)].resample('D').sum() / 1000
        tot_consumption_daily= tot_consumption_selected_df.loc[(tot_consumption_selected_df.index >= start_date) & (tot_consumption_selected_df.index <= end_date)].resample('D').sum()
        tot_consumption_daily=tot_consumption_daily['sum'].resample('D').sum() / 1000
        col1, col2 = st.columns(2)
        with col1:
            create_combined_time_series(flows_daily, tot_consumption_daily, title=f'Daily Time Series of Production, Imports, and Exports in {selected_country_name} ')
            # Ajouter des colonnes pour les boutons à l'intérieur de col1
            download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

            # Bouton pour télécharger le CSV dans download_col (gauche)
            with download_col:
                download_data_as_csv(flows_daily,
                                     f"Daily_Time_Series_of_Production_Imports_and_Exports_in_{selected_country_name.replace(' ', '_')}.csv")

                # Use an expander to display the general description in info_col (right)
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                **Chart Description:**  
                                This chart presents the daily evolution of energy flows in **{selected_country_name}**, 
                                including production, imports, exports, and total electricity consumption.

                                **Data Source:** EcoDynElec
                            """)





        # for impacts
        tot_electricity_impact_daily_df = tot_electricity_impact_selected_df.loc[
            (tot_electricity_impact_selected_df.index >= start_date) &
            (tot_electricity_impact_selected_df.index <= end_date)
            ]





        # Display the chart based on user's choice
        with col2:

                # Create a line plot (assuming you want to use Plotly)
                fig = px.line(tot_electricity_impact_daily_df.resample('D').mean(),
                              x=tot_electricity_impact_daily_df.resample('D').mean().index, y='sum',
                              title=f'Line Plot of GHG Emissions in {selected_country_name}')
                fig.update_layout(legend_title_text='')

                fig.update_traces(hovertemplate='%{y:.0f} gCO2eq/KWh<br>Date: %{x|%a %d %b %Y}<extra></extra>')
                fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.2,
                                   showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
                # Add annotation for unit
                fig.add_annotation(text="gCO2eq/KWh", xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False,
                                   font=dict(size=12))
                fig.update_xaxes(title_text='', tickformat='%a %d %b %y')
                fig.update_yaxes(title_text='')
                st.plotly_chart(fig)

                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(tot_electricity_impact_daily_df, f"Daily_Line_Plot_of_GHG_Emissions_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                **Chart's Description:** 
                                This line plot visualizes the temporal evolution of greenhouse gas (GHG) emissions in **{selected_country_name}**,
                                 measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                 The x-axis represents the time series data over several days, while the y-axis indicates the magnitude of GHG emissions

                                **Data Source:** EcoDynElec
                            """)






        selection = aggregation_menu()
        if selection == "Mixed":
            raw_consumption_by_src_daily_df = raw_consumption_by_src_selected_df.loc[(raw_consumption_by_src_selected_df.index >= start_date) & (
                            raw_consumption_by_src_selected_df.index <= end_date)].resample('D').sum()
            raw_consumption_by_src_daily_df = raw_consumption_by_src_daily_df.resample('D').sum() / 1000
            raw_consumption_by_src_daily_df = aggregate_by_country(selected_country_name,
                                                                     raw_consumption_by_src_daily_df)
            col1, col2 = st.columns(2)
            with col1:
                create_area_mixte(raw_consumption_by_src_daily_df,
                                  title=f'Daily consumption by source in {selected_country_name}',text='GWh')

                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(raw_consumption_by_src_daily_df, f"Daily_consumption_by_source_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                **Chart Description:**  
                                
                                This stacked area chart illustrates the daily electricity consumption by energy source in **{selected_country_name}** over the selected time period.
                                 Each area in the plot corresponds to a different energy source contributing to the total electricity consumption.

                                **Data Source:** EcoDynElec
                            """)


            electricity_impact_by_src_daily_df = electricity_impact_by_src_selected_df.loc[(electricity_impact_by_src_selected_df.index >= start_date) & (
                        electricity_impact_by_src_selected_df.index <= end_date)]
            electricity_impact_by_src_daily_df = electricity_impact_by_src_daily_df.resample('D').mean()
            electricity_impact_by_src_daily_df = aggregate_by_country(selected_country_name,
                                                                     electricity_impact_by_src_daily_df)
            with col2:
                create_area_mixte(electricity_impact_by_src_daily_df,title=f'Daily average of GHG emissions by source in {selected_country_name}',text='gCO2/KWh')
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(electricity_impact_by_src_daily_df,  f"Daily_average_of_GHG_emissions_by_source_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                **Chart Description:**  
                                                This stacked area chart visualizes the daily average of greenhouse gas (GHG) emissions by energy source in **{selected_country_name}** over the selected period.
                                                 Each color band represents the contribution of a different energy source to the total GHG emissions,
                                                 measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh)

                                                **Data Source:** EcoDynElec
                                            """)

        if selection == "By Technology":

            col1, col2 = st.columns(2)  # Crée deux colonnes pour les graphiques
            with col1:
                techno_daily_df=(techno_selected_df.loc[(techno_selected_df.index >= start_date) & (techno_selected_df.index <= end_date)]
                             .resample('D').sum()) / 1000
                #create_time_series(techno_daily_df,title=f'Daily average of GHG emissions by source in {selected_country_name}')
                create_area_mixte(techno_daily_df,
                                              title=f'Daily consumption by technology in {selected_country_name}',text='GWh')
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(techno_daily_df, f"Daily_consumption_by_technology_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                **Chart Description:**  

                                                This stacked area chart illustrates the daily electricity consumption by technology in **{selected_country_name}** over the selected time period.
                                                 Each area in the plot corresponds to a different energy source contributing to the total electricity consumption.

                                                **Data Source:** EcoDynElec
                                            """)


            techno_impact_daily_df = techno_impact_selected_df.loc[(techno_impact_selected_df.index >= start_date) &
                                                                                           (techno_impact_selected_df.index <= end_date)].resample('D').mean()



            with col2:
                create_area_mixte(techno_impact_daily_df,
                                              title=f'Daily average of GHG emissions by technology in {selected_country_name}', text='gCO2eq/KWh')

                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(techno_impact_daily_df,  f"Daily_average_of_GHG_emissions_by_technology_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                **Chart Description:**  
                                This stacked area chart visualizes the daily average of greenhouse gas (GHG) emissions by technology in **{selected_country_name}** over the selected period.
                                                 Each color band represents the contribution of a different energy source to the total GHG emissions,
                                                 measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh)

                                                                

                                **Data Source:** EcoDynElec
                                                            """)




        if selection == "Country of origin":
            tot_electricity_mix_daily_df = tot_electricity_mix_selected_df.loc[
                (tot_electricity_mix_selected_df.index >= start_date) & (tot_electricity_mix_selected_df.index <= end_date)].resample('D').sum()
            daily_mix_import = tot_electricity_mix_daily_df.drop(['sum'], axis=1)
            daily_mix_import = daily_mix_import.multiply(tot_consumption_daily, axis='index').resample('D').sum() / 1000


            col1, col2 = st.columns(2)
            with col1:
                create_area_chart(daily_mix_import,title=f"Origins of daily consumer mix by country in {selected_country_name}")
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(daily_mix_import, f"Daily_consumption_by_country_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                **Chart Description:**  

                                                                This stacked area chart displays the origins of the daily consumer electricity mix by country in Switzerland over the selected time period.
                                                                 Each color band represents the contribution of electricity imports from different countries to the total electricity mix consumed in **{selected_country_name}**.

                                                                **Data Source:** EcoDynElec
                                                            """)


            tot_electricity_impact_daily_df = tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index >= start_date) &
                                                                                 (tot_electricity_impact_selected_df.index <= end_date)]

            daily_mix_impact = tot_electricity_impact_daily_df.drop(['sum'], axis=1).resample('D').mean()
            with col2:
                create_area_chart(daily_mix_impact, title=f'Daily average of GHG emissions by country (gCO2eq/kWh) in {selected_country_name}', unit="gCO2eq/kWh")
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:

                    download_data_as_csv(daily_mix_impact,  f"Daily_average_of_GHG_emissions_by_country_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                                                                        **Chart Description:**  

                                                                                                                        This stacked area chart shows the daily average of greenhouse gas (GHG) emissions by country in **{selected_country_name}**, measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                                                                                         Each color band represents the GHG emissions associated with electricity produced or imported from different countries.

                                                                                                                        **Data Source:** EcoDynElec
                                                                                                                    """)

    elif resolution == 'Hourly':

        # Supposons que flows_selected_df est déjà défini et correctement configuré
        min_date = flows_selected_df.index.min()
        max_date = flows_selected_df.index.max()

        # Positionnement des widgets dans les colonnes si déjà définies
        with col3:  # Exemple de placement dans la colonne
            start_date, end_date = st.date_input(
                "Select a date range:",
                [min_date, max_date],  # Utilisez les extrêmes de l'index comme valeur par défaut
                min_value=min_date,  # Date minimale extraite de l'index
                max_value=max_date,  # Date maximale extraite de l'index
                help="You can select a range within the available dates in the data."
            )
            # Ajustez end_date pour inclure toute la journée
            start_date = pd.Timestamp(start_date)
            end_date = pd.Timestamp(end_date) + pd.Timedelta(days=1, seconds=-1)



        # Filtrer le DataFrame selon la plage sélectionnée
        flows_hourly = flows_selected_df.loc[(flows_selected_df.index >= start_date) & (flows_selected_df.index <= end_date)]/ 1000
        tot_consumption_hourly = tot_consumption_selected_df.loc[
            (tot_consumption_selected_df.index >= start_date) & (tot_consumption_selected_df.index <= end_date)]
        tot_consumption_hourly=tot_consumption_hourly['sum'] / 1000
        col1,col2= st.columns(2)
        with col1:
            create_combined_time_series(flows_hourly, tot_consumption_hourly, title=f'Hourly Time Series of Production, Imports, and Exports in {selected_country_name}',resolution='hourly')
            download_col, info_col = st.columns([0.7, 0.3])  # Adjust the ratios as needed

            # Bouton pour télécharger le CSV dans download_col (gauche)
            with download_col:
                download_data_as_csv(flows_hourly, f"Hourly_Time_Series_of_Production_Imports_and_Exports_in_{selected_country_name.replace(' ', '_')}.csv")

                # Use an expander to display the general description in info_col (right)
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                            **Chart Description:**  
                                            This chart presents the hourly evolution of energy flows in **{selected_country_name}**, 
                                            including production, imports, exports, and total electricity consumption.

                                            **Data Source:** EcoDynElec
                                        """)



        # pour les impacts
        tot_electricity_impact_hourly_df = tot_electricity_impact_selected_df.loc[(tot_electricity_impact_selected_df.index >= start_date) & (
                    tot_electricity_impact_selected_df.index <= end_date)]


        pivot_table = create_pivot_table(tot_electricity_impact_hourly_df['sum'].resample('H').mean())


        # Display the chart based on user's choice
        with col4:
            # Add a selectbox to allow the user to choose between heatmap and line plot
            chart_type = st.selectbox("Choose chart type:", ["Heatmap", "Line Plot"])
        with col2:
            if chart_type == "Line Plot":
                # Create a line plot (assuming you want to use Plotly)
                fig = px.line(tot_electricity_impact_hourly_df.resample('H').mean(),
                              x=tot_electricity_impact_hourly_df.index, y='sum',
                              title=f'Line Plot of GHG Emissions in {selected_country_name}')
                fig.update_layout(legend_title_text='')
                fig.update_traces(hovertemplate='%{y:.0f} gCO2eq/KWh<br>Date: %{x| %a %d %b %Y %H %M}<extra></extra>')
                fig.update_xaxes(title_text='', tickformat=' %a %d %b %y %H %M')
                fig.update_yaxes(title_text='')
                fig.add_annotation(text="© Ecodynelec-HEIG-VD", xref="paper", yref="paper", x=0, y=-0.5,
                                   showarrow=False, font=dict(size=12, color="gray"), xanchor='left', yanchor='bottom')
                fig.add_annotation(text="gCO2eq/KWh", xref="paper", yref="paper", x=-0.05, y=1.1, showarrow=False,
                                   font=dict(size=12))
                st.plotly_chart(fig)
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(tot_electricity_impact_hourly_df, f"Hourly_Line_Plot_of_GHG_Emissions_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                **Chart's Description:** 
                                                This line plot visualizes the temporal evolution of greenhouse gas (GHG) emissions in **{selected_country_name}**,
                                                 measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                 The x-axis represents the time series data over time (hourly), while the y-axis indicates the magnitude of GHG emissions
    
                                                **Data Source:** EcoDynElec
                                            """)

            elif chart_type == "Heatmap":
                create_heatmap(pivot_table, f'Heatmap of the average of GHG emissions in {selected_country_name}')
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(pivot_table, f"Heatmap_of_the_average_of_GHG_emissions_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                **Chart Description:**  
                                                This heatmap displays the average greenhouse gas (GHG) emissions in **{selected_country_name}** over time.
                                                 The horizontal axis represents the dates, while the vertical axis represents the hours of the day.
                                                  Each colored cell in the heatmap corresponds to the intensity of GHG emissions, measured in grams of
                                                   CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
    
                                                **Data Source:** EcoDynElec
                                            """)

        selection = aggregation_menu()
        if selection == "Mixed":
            raw_consumption_by_src_hourly_df = raw_consumption_by_src_selected_df.loc[(raw_consumption_by_src_selected_df.index >= start_date) & (
                        raw_consumption_by_src_selected_df.index <= end_date)].resample('H').sum()
            raw_consumption_by_src_hourly_df = raw_consumption_by_src_hourly_df.resample('H').sum() / 1000
            raw_consumption_by_src_hourly_df = aggregate_by_country(selected_country_name,raw_consumption_by_src_hourly_df)
            col1, col2 = st.columns(2)
            with col1:
                create_area_mixte(raw_consumption_by_src_hourly_df,
                                              title=f'Hourly consumption by source in {selected_country_name}',text='GWh',resolution='hourly')
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(raw_consumption_by_src_hourly_df, f"Hourly_consumption_by_source_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                **Chart Description:**  

                                                This stacked area chart illustrates the hourly electricity consumption by energy source in **{selected_country_name}** over the selected time period.
                                                 Each area in the plot corresponds to a different energy source contributing to the total electricity consumption.

                                                **Data Source:** EcoDynElec
                                            """)


            electricity_impact_by_src_hourly_df = electricity_impact_by_src_selected_df.loc[(electricity_impact_by_src_selected_df.index >= start_date) & (
                        electricity_impact_by_src_selected_df.index <= end_date)].resample('H').sum()
            electricity_impact_by_src_hourly_df = electricity_impact_by_src_hourly_df.resample('H').mean()
            electricity_impact_by_src_hourly_df = aggregate_by_country(selected_country_name,
                                                                      electricity_impact_by_src_hourly_df)
            with col2:
                create_area_mixte(electricity_impact_by_src_hourly_df,
                                      title=f'Hourly average of GHG emissions by source in {selected_country_name}',text='gCO2/KWh',resolution='hourly')

                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(electricity_impact_by_src_hourly_df,  f"Hourly_average_of_GHG_emissions_by_source_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                **Chart Description:**  
                                                                This stacked area chart visualizes the hourly average of greenhouse gas (GHG) emissions by energy source in **{selected_country_name}** over the selected period.
                                                                 Each color band represents the contribution of a different energy source to the total GHG emissions,
                                                                 measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh)

                                                                **Data Source:** EcoDynElec
                                                            """)



        if selection == "By Technology":

            col1, col2 = st.columns(2)  # Crée deux colonnes pour les graphiques
            with col1:
                techno_hourly_df = (techno_selected_df.loc[
                                    (techno_selected_df.index >= start_date) &
                                    (techno_selected_df.index <= end_date)]
                                .resample('H').sum()) / 1000

                create_area_mixte(techno_hourly_df,
                               title=f'Daily average of GHG emissions by technology in {selected_country_name}',text='GWh',resolution='hourly')
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(techno_hourly_df,  f"Hourly_average_of_GHG_emissions_by_technology_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                **Chart Description:**  

                                                                This stacked area chart illustrates the hourly electricity consumption by technology in **{selected_country_name}** over the selected time period.
                                                                 Each area in the plot corresponds to a different energy source contributing to the total electricity consumption.

                                                                **Data Source:** EcoDynElec
                                                            """)


            with col2:
                techno_impact_hourly_df = techno_impact_selected_df.loc[
                                              (techno_impact_selected_df.index >= start_date) &
                                              (techno_impact_selected_df.index <= end_date)].resample('D').mean()

                create_area_mixte(techno_impact_hourly_df,
                                   title=f'Hourly average of GHG emissions by technology in {selected_country_name}',text='gCO2/KWh',resolution="hourly")

                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(techno_impact_hourly_df, f"Hourly_consumption_by_technology_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                **Chart Description:**  
                                                This stacked area chart visualizes the hourly average of greenhouse gas (GHG) emissions by technology in **{selected_country_name}** over the selected period.
                                                                 Each color band represents the contribution of a different energy source to the total GHG emissions,
                                                                 measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh)



                                                **Data Source:** EcoDynElec
                                                                            """)


        if selection == "Country of origin":
            tot_electricity_mix_hourly_df = tot_electricity_mix_selected_df.loc[
                (tot_electricity_mix_selected_df.index >= start_date) & (tot_electricity_mix_selected_df.index <= end_date)].resample('H').sum()
            hourly_mix_import = tot_electricity_mix_hourly_df.drop(['sum'], axis=1)
            hourly_mix_import = hourly_mix_import.multiply(tot_consumption_hourly, axis='index').resample('H').sum() / 1000


            col1, col2 = st.columns(2)
            with col1:
                create_area_chart(hourly_mix_import,title=f"Origins of hourly consumer mix by country in {selected_country_name}",resolution="hourly")
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(hourly_mix_import, f"Hourly_consumption_by_country_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                                **Chart Description:**  

                                                                                This stacked area chart displays the origins of the hourly consumer electricity mix by country in Switzerland over the selected time period.
                                                                                 Each color band represents the contribution of electricity imports from different countries to the total electricity mix consumed in **{selected_country_name}**.

                                                                                **Data Source:** EcoDynElec
                                                                            """)


            tot_electricity_impact_hourly_df = tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index >= start_date) &
                                                                                 (tot_electricity_impact_selected_df.index <= end_date)]

            hourly_mix_impact = tot_electricity_impact_hourly_df.drop(['sum'], axis=1).resample('H').mean()
            with col2:
                create_area_chart(hourly_mix_impact, title=f'Hourly average of GHG emissions by country in {selected_country_name}',resolution="hourly",unit="gCO2eq/KWh")
                download_col, info_col = st.columns([0.7, 0.3])
                with download_col:
                    download_data_as_csv(hourly_mix_impact,  f"Hourly_average_of_GHG_emissions_by_country_in_{selected_country_name.replace(' ', '_')}.csv")
                with info_col:
                    with st.expander("ℹ️ Chart's Information"):
                        st.write(f"""
                                                                                                **Chart Description:**  

                                                                                                This stacked area chart shows the hourly average of greenhouse gas (GHG) emissions by country in **{selected_country_name}**, measured in grams of CO2 equivalent per kilowatt-hour (gCO2eq/kWh).
                                                                                                 Each color band represents the GHG emissions associated with electricity produced or imported from different countries.

                                                                                                **Data Source:** EcoDynElec
                                                                                            """)



















