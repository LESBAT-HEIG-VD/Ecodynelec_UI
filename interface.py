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







# Sidebar Menu with Main Options
with st.sidebar:
    main_option = option_menu(
        menu_title="Main Menu",  # Main menu title
        options=["Données de mix", "Applications", "Mode expert", "Méthodologie"],  # Main menu options
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

#Données de consommation totale
tot_consumption_FR=pd.read_csv("./data/consumptions/tot_consumption_FR.csv")
tot_consumption_DE=pd.read_csv("./data/consumptions/tot_consumption_DE.csv")
tot_consumption_AT=pd.read_csv("./data/consumptions/tot_consumption_AT.csv")
tot_consumption_CH=pd.read_csv("./data/consumptions/tot_consumption_CH.csv")

#Données de consommation by src
raw_consumption_by_src_FR=pd.read_csv("./data/consumptions/raw_consumption_by_src_FR.csv")
raw_consumption_by_src_DE=pd.read_csv("./data/consumptions/raw_consumption_by_src_DE.csv")
raw_consumption_by_src_AT=pd.read_csv("./data/consumptions/raw_consumption_by_src_AT.csv")
raw_consumption_by_src_CH=pd.read_csv("./data/consumptions/raw_consumption_by_src_CH.csv")

#electricity_mixs
tot_electricity_mix_CH=pd.read_csv("./data/electricity_mixs/electricity_mix_CH.csv")
tot_electricity_mix_AT=pd.read_csv("./data/electricity_mixs/electricity_mix_AT.csv")
tot_electricity_mix_DE=pd.read_csv("./data/electricity_mixs/electricity_mix_DE.csv")
tot_electricity_mix_FR=pd.read_csv("./data/electricity_mixs/electricity_mix_FR.csv")

#electricity_impacts
tot_electricity_impact_CH=pd.read_csv("./data/electricity_impacts/electricity_impact_CH.csv")
tot_electricity_impact_AT=pd.read_csv("./data/electricity_impacts/electricity_impact_AT.csv")
tot_electricity_impact_DE=pd.read_csv("./data/electricity_impacts/electricity_impact_DE.csv")
tot_electricity_impact_FR=pd.read_csv("./data/electricity_impacts/electricity_impact_FR.csv")


#electricity_impacts
electricity_impact_by_src_CH=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_CH.csv")
electricity_impact_by_src_AT=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_AT.csv")
electricity_impact_by_src_DE=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_DE.csv")
electricity_impact_by_src_FR=pd.read_csv("./data/electricity_impacts/electricity_impact_by_src_FR.csv")

#by_techno
Techno_FR=pd.read_csv("./data/technologies/technologies_FR.csv")
Techno_AT=pd.read_csv("./data/technologies/technologies_AT.csv")
Techno_DE=pd.read_csv("./data/technologies/technologies_DE.csv")
Techno_CH=pd.read_csv("./data/technologies/technologies_CH.csv")

#by_techno_impact
Techno_impact_FR=pd.read_csv("./data/technologies/Techno_impact_FR.csv")
Techno_impact_AT=pd.read_csv("./data/technologies/Techno_impact_AT.csv")
Techno_impact_DE=pd.read_csv("./data/technologies/Techno_impact_DE.csv")
Techno_impact_CH=pd.read_csv("./data/technologies/Techno_impact_CH.csv")



for df in [flows_FR, flows_DE, flows_AT, flows_CH, tot_consumption_FR, tot_consumption_DE, tot_consumption_AT, tot_consumption_CH,
           tot_electricity_mix_CH,tot_electricity_mix_AT,tot_electricity_mix_DE,tot_electricity_mix_FR,tot_electricity_impact_CH,
           tot_electricity_impact_AT,tot_electricity_impact_DE,tot_electricity_impact_FR,raw_consumption_by_src_FR,raw_consumption_by_src_CH,
           raw_consumption_by_src_DE,raw_consumption_by_src_AT,electricity_impact_by_src_CH,electricity_impact_by_src_AT,
           electricity_impact_by_src_DE,electricity_impact_by_src_FR,Techno_FR,Techno_AT,Techno_DE,Techno_CH,Techno_impact_FR,Techno_impact_AT,
            Techno_impact_DE,Techno_impact_CH]:

        df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

for df in [flows_FR, flows_DE, flows_AT, flows_CH]:
    df['total_consumption']=df['production']+df['imports']-df['exports']

# Utilisation de colonnes pour une mise en page personnalisée
col1, col2, col3, col4, col5 = st.columns(5)  # Créer 5 colonnes
years = list(range(2016, 2023))
months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
          "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
Countries= {'Suisse' : 'CH', 'France' : 'FR', 'Allemagne' : 'DE', 'Autriche' : 'AT'}
ordered_countries = ['CH', 'DE', 'FR', 'AT', 'IT', 'Other']
ordered_colors = ['blue','green', 'red', 'purple',  'orange',  'yellow' ]
month_dict = {1: "January", 2: "February", 3: "March", 4: "April",5: "May", 6: "June", 7: "July", 8: "August",9: "September", 10: "October", 11: "November", 12: "December"}


#Dictionnaires des dataframes
dataframes_flows = {'Suisse': flows_CH,'France': flows_FR,'Allemagne': flows_DE,'Autriche': flows_AT}
dataframes_tot_consumption = {'Suisse': tot_consumption_CH,'France':tot_consumption_FR,
                              'Allemagne': tot_consumption_DE,'Autriche': tot_consumption_AT}
dataframes_raw_consumption_by_src = {'Suisse': raw_consumption_by_src_CH,'France':raw_consumption_by_src_FR,
                              'Allemagne': raw_consumption_by_src_DE,'Autriche': raw_consumption_by_src_AT}
dataframes_tot_electricity_mix = {'Suisse': tot_electricity_mix_CH,'France':tot_electricity_mix_FR,
                              'Allemagne': tot_electricity_mix_DE,'Autriche': tot_electricity_mix_AT}
dataframes_tot_electricity_impact = {'Suisse': tot_electricity_impact_CH,'France':tot_electricity_impact_FR,
                              'Allemagne': tot_electricity_impact_DE,'Autriche': tot_electricity_impact_AT}
dataframes_electricity_impact_by_src = {'Suisse': electricity_impact_by_src_CH,'France':electricity_impact_by_src_FR,
                              'Allemagne': electricity_impact_by_src_DE,'Autriche': electricity_impact_by_src_AT}
dataframes_techno = {'Suisse': Techno_CH,'France':Techno_FR,'Allemagne': Techno_DE,'Autriche': Techno_AT}
dataframes_techno_impact = {'Suisse': Techno_impact_CH,'France':Techno_impact_FR,'Allemagne': Techno_impact_DE,'Autriche': Techno_impact_AT}

with col1:
    selected_country_name = st.selectbox('Choisissez un pays:', list(Countries.keys()))

with col2:
    resolution = st.selectbox('Résolution:', ['Annuel', 'Mensuel','Quotidien','Horaire'])


# Récupération du DataFrame basé sur le pays sélectionné
tot_consumption_selected_df = dataframes_tot_consumption [selected_country_name]
raw_consumption_by_src_selected_df = dataframes_raw_consumption_by_src [selected_country_name]
flows_selected_df =dataframes_flows[selected_country_name]
tot_electricity_mix_selected_df = dataframes_tot_electricity_mix [selected_country_name]
tot_electricity_impact_selected_df = dataframes_tot_electricity_impact [selected_country_name]
electricity_impact_by_src_selected_df = dataframes_electricity_impact_by_src [selected_country_name]
techno_selected_df=dataframes_techno [selected_country_name]
techno_impact_selected_df=dataframes_techno_impact [selected_country_name]




if main_option == "Données de mix":
    if resolution == 'Annuel':
        flows_selected_df['exports'] = -flows_selected_df['exports']
        flows_annual_df = flows_selected_df.resample('Y').sum() / 1000
        flows_annual_df.index = flows_annual_df.index.year
        tot_consumption_annual_df = tot_consumption_selected_df['sum'].resample('Y').sum() / 1000

        col1, col2 = st.columns(2)
        with col1:

            bar_group_consumption(flows_annual_df, title=f'Yearly Time Series of Production, Imports, and Exports ', text="GWh",
                                  y_cols=['total_consumption', 'production', 'imports', 'exports'], barmode='group')
            download_data_as_csv(flows_annual_df, "flows_annual_df.csv")
        # pour les impacts
        consumer_impact_annual = tot_electricity_impact_selected_df['sum'].resample('Y').mean()
        consumer_impact_annual.index = consumer_impact_annual.index.year
        with col2:
            bar_group_ghg(consumer_impact_annual, f'Yearly average of GHG emissions  in {selected_country_name}')
            download_data_as_csv(consumer_impact_annual, "consumer_impact_annual.csv")



        selection = aggregation_menu()
        if selection == "Mixte":
            raw_consumption_by_src_annual_df = raw_consumption_by_src_selected_df.resample('Y').sum() / 1000
            raw_consumption_by_src_annual_df = aggregate_by_country(selected_country_name,raw_consumption_by_src_annual_df)
            raw_consumption_by_src_annual_df.index = raw_consumption_by_src_annual_df.index.year
            col1, col2 = st.columns(2)
            with col1:

                bar_consumption(raw_consumption_by_src_annual_df,title=f'Yearly consumption by source in {selected_country_name}')
                download_data_as_csv(raw_consumption_by_src_annual_df, "raw_consumption_by_src_annual_df.csv")

            electricity_impact_by_src_annual_df = electricity_impact_by_src_selected_df.resample('Y').mean()
            electricity_impact_by_src_annual_df = aggregate_by_country(selected_country_name,electricity_impact_by_src_annual_df)
            electricity_impact_by_src_annual_df.index = electricity_impact_by_src_annual_df.index.year

            with col2:

                bar_ghg(electricity_impact_by_src_annual_df, f'Yearly average of GHG emissions  in {selected_country_name} by source')
                download_data_as_csv(electricity_impact_by_src_annual_df, "electricity_impact_by_src_annual_df.csv")
        if selection == "Technologie":
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
                download_data_as_csv(techno_annual_df, "techno_annual_df.csv")


            techno_impact_annual_df=techno_impact_selected_df.resample('Y').mean()
            techno_impact_annual_df.index = techno_impact_annual_df.index.year

            with col2:

                bar_group_consumption(techno_impact_annual_df,
                                      title=f'Yearly average of GHG emissions by technology in {selected_country_name}',
                                      text="gCO2eq/kWh",
                                      y_cols=techno_impact_annual_df.columns, barmode='stack')
                download_data_as_csv(techno_impact_annual_df, "techno_impact_annual_df.csv")


        if selection == "Pays d'origine":
            mix_import_annual = tot_electricity_mix_selected_df.drop(['sum'], axis=1)
            mix_import_annual = mix_import_annual.multiply(tot_consumption_selected_df['sum'], axis='index').resample('Y').sum() / 1000
            mix_import_annual.index = mix_import_annual.index.year



            col1, col2 = st.columns(2)
            with col1:

                bar_group_consumption(mix_import_annual, title=f"Origins of yearly Swiss consumer mix in {selected_country_name}",
                                      text="GWh",
                                      y_cols=ordered_countries, barmode='stack')
                download_data_as_csv(mix_import_annual, "mix_import_annual.csv")


            mix_impact_annual = tot_electricity_impact_selected_df.drop(['sum'], axis=1).resample('Y').mean()
            mix_impact_annual.index=mix_impact_annual.index.year
            with col2:

                bar_group_consumption(mix_impact_annual,title=f'Yearly average of GHG emissions  in {selected_country_name} by country',
                                      text="gCO2eq/kWh",y_cols=ordered_countries, barmode='stack')
                download_data_as_csv(mix_impact_annual, "mix_impact_annual.csv")



    elif resolution == 'Mensuel':

        with col3:
            # Utilisation d'un slider pour choisir une année
            selected_year = st.slider('Choisissez une année:', min_value=min(years), max_value=max(years), value=min(years))

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

            bar_group_consumption(flows_monthly_df, title=f'Monthly Time Series of Production, Imports, and Exports ',
                                  text="GWh",
                                  y_cols=['total_consumption', 'production', 'imports', 'exports'], barmode='group')
            download_data_as_csv(flows_monthly_df, "flows_monthly_df.csv")


            # pour les impacts
        tot_electricity_impact_monthly_df=tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index.year == selected_year)]
        monthly_consumer_impact = tot_electricity_impact_monthly_df['sum'].resample('M').mean()
        monthly_consumer_impact.index = monthly_consumer_impact.index.month.map(lambda x: month_dict[x])
        with col2:

            bar_group_ghg(monthly_consumer_impact, f'Monthly average of GHG emissions  in {selected_country_name}')
            download_data_as_csv(monthly_consumer_impact, "monthly_consumer_impact.csv")

        selection = aggregation_menu()
        if selection == "Mixte":

            raw_consumption_by_src_monthly_df = process_data_by_month(raw_consumption_by_src_selected_df, selected_year, selected_country_name, month_dict,
                aggregate_by_country)

            electricity_impact_by_src_monthly_df = process_ghg_data_by_month(electricity_impact_by_src_selected_df, selected_year, selected_country_name, month_dict,
                aggregate_by_country)

            col1, col2 = st.columns(2)
            with col1:
                bar_consumption(raw_consumption_by_src_monthly_df,title=f'Monthly consumption by source in {selected_country_name}')
                download_data_as_csv(raw_consumption_by_src_monthly_df, "raw_consumption_by_src_monthly_df.csv")
            with col2:
                bar_ghg(electricity_impact_by_src_monthly_df,f'Monthly average of GHG emissions  in {selected_country_name} by source')
                download_data_as_csv(electricity_impact_by_src_monthly_df, "electricity_impact_by_src_monthly_df.csv")
        if selection == "Technologie":

            techno_monthly_df = techno_selected_df.loc[techno_selected_df.index.year == selected_year]
            techno_monthly_df = techno_monthly_df.resample('M').sum() / 1000
            techno_monthly_df.index = techno_monthly_df.index.month.map(lambda x: month_dict[x])
            col1, col2 = st.columns(2)
            with col1:
                bar_consumption(techno_monthly_df,title=f'Monthly consumption by technology in {selected_country_name}')
                download_data_as_csv(techno_monthly_df, "techno_monthly_df.csv")
            techno_impact_monthly_df = techno_impact_selected_df.loc[techno_impact_selected_df.index.year == selected_year]
            techno_impact_monthly_df = techno_impact_monthly_df.resample('M').mean()
            techno_impact_monthly_df.index = techno_impact_monthly_df.index.month.map(lambda x: month_dict[x])

            with col2:
                bar_ghg(techno_impact_monthly_df,f'Monthly average  of GHG emissions by technology in {selected_country_name}')
                download_data_as_csv(techno_impact_monthly_df, "techno_impact_monthly_df.csv")



        if selection == "Pays d'origine":
            tot_electricity_mix_monthly_df = tot_electricity_mix_selected_df[(tot_electricity_mix_selected_df.index.year == selected_year)]
            monthly_mix_import = tot_electricity_mix_monthly_df.drop(['sum'], axis=1)
            monthly_mix_import = monthly_mix_import.multiply(tot_consumption_monthly_df, axis='index').resample('M').sum() / 1000
            monthly_mix_import.index = monthly_mix_import.index.month.map(lambda x: month_dict[x])


            col1, col2 = st.columns(2)
            with col1:
                bar_group_consumption(monthly_mix_import,
                                      title=f"Origins of monthly consumer mix in {selected_country_name}",
                                      text="GWh",
                                      y_cols=ordered_countries, barmode='stack')
                download_data_as_csv(monthly_mix_import, "monthly_mix_import.csv")

            tot_electricity_impact_monthly_df = tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index.year == selected_year)]
            monthly_mix_impact = tot_electricity_impact_monthly_df.drop(['sum'], axis=1).resample('M').mean()
            monthly_mix_impact.index = monthly_mix_impact.index.month.map(lambda x: month_dict[x])
            with col2:

                bar_group_consumption(monthly_mix_impact,
                                      title=f'Monthly average of GHG emissions  in {selected_country_name}',
                                      text="gCO2eq/kWh",
                                      y_cols=ordered_countries, barmode='stack')
                download_data_as_csv(monthly_mix_impact, "monthly_mix_impact.csv")


    elif resolution == 'Quotidien':

        # Supposons que flows_selected_df est déjà défini et correctement configuré
        min_date = flows_selected_df.index.min()
        max_date = flows_selected_df.index.max()

        # Positionnement des widgets dans les colonnes si déjà définies
        with col3:  # Exemple de placement dans la colonne
            start_date, end_date = st.date_input(
                "Sélectionnez une plage de dates:",
                [min_date, max_date],  # Utilisez les extrêmes de l'index comme valeur par défaut
                min_value=min_date,  # Date minimale extraite de l'index
                max_value=max_date,  # Date maximale extraite de l'index
                help="Vous pouvez choisir une plage dans les limites des dates disponibles dans les données."
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
            create_combined_time_series(flows_daily, tot_consumption_daily, title=f'Daily Time Series of Production, Imports, and Exports ')
            download_data_as_csv(flows_daily, "flows_daily.csv")


        # pour les impacts
        tot_electricity_impact_daily_df = tot_electricity_impact_selected_df.loc[(tot_electricity_impact_selected_df.index >= start_date) & (
                        tot_electricity_impact_selected_df.index <= end_date)]

        pivot_table=create_pivot_table(tot_electricity_impact_daily_df['sum'].resample('H').mean())
        with col2:
            create_heatmap(pivot_table, f' Heatmap of the average of GHG emissions  in {selected_country_name}')
            download_data_as_csv(pivot_table, "tot_electricity_impact_daily_df.csv")

        selection = aggregation_menu()
        if selection == "Mixte":
            raw_consumption_by_src_daily_df = raw_consumption_by_src_selected_df.loc[(raw_consumption_by_src_selected_df.index >= start_date) & (
                            raw_consumption_by_src_selected_df.index <= end_date)].resample('D').sum()
            raw_consumption_by_src_daily_df = raw_consumption_by_src_daily_df.resample('D').sum() / 1000
            raw_consumption_by_src_daily_df = aggregate_by_country(selected_country_name,
                                                                     raw_consumption_by_src_daily_df)
            col1, col2 = st.columns(2)
            with col1:
                create_area_mixte(raw_consumption_by_src_daily_df,
                                  title=f'Daily consumption by source in {selected_country_name}',text='GWh')
                download_data_as_csv(raw_consumption_by_src_daily_df, "raw_consumption_by_src_daily_df.csv")

            electricity_impact_by_src_daily_df = electricity_impact_by_src_selected_df.loc[(electricity_impact_by_src_selected_df.index >= start_date) & (
                        electricity_impact_by_src_selected_df.index <= end_date)]
            electricity_impact_by_src_daily_df = electricity_impact_by_src_daily_df.resample('D').mean()
            electricity_impact_by_src_daily_df = aggregate_by_country(selected_country_name,
                                                                     electricity_impact_by_src_daily_df)
            with col2:
                create_area_mixte(electricity_impact_by_src_daily_df,title=f'Daily average of GHG emissions by source in {selected_country_name}',text='gCO2/KWh')
                download_data_as_csv(electricity_impact_by_src_daily_df, "electricity_impact_by_src_daily_df.csv")
        if selection == "Technologie":

            col1, col2 = st.columns(2)  # Crée deux colonnes pour les graphiques
            with col1:
                techno_daily_df=(techno_selected_df.loc[(techno_selected_df.index >= start_date) & (techno_selected_df.index <= end_date)]
                             .resample('D').sum()) / 1000
                #create_time_series(techno_daily_df,title=f'Daily average of GHG emissions by source in {selected_country_name}')
                create_area_mixte(techno_daily_df,
                                              title=f'Daily consumption by technology in {selected_country_name}',text='GWh')
                download_data_as_csv(techno_daily_df, "techno_daily_df.csv")

            techno_impact_daily_df = techno_impact_selected_df.loc[(techno_impact_selected_df.index >= start_date) &
                                                                                           (techno_impact_selected_df.index <= end_date)].resample('D').mean()



            with col2:
                create_area_mixte(techno_impact_daily_df,
                                              title=f'Daily average of GHG emissions by technology in {selected_country_name}', text='gCO2/KWh')
                download_data_as_csv(techno_impact_daily_df, "techno_impact_daily_df.csv")



        if selection == "Pays d'origine":
            tot_electricity_mix_daily_df = tot_electricity_mix_selected_df.loc[
                (tot_electricity_mix_selected_df.index >= start_date) & (tot_electricity_mix_selected_df.index <= end_date)].resample('D').sum()
            daily_mix_import = tot_electricity_mix_daily_df.drop(['sum'], axis=1)
            daily_mix_import = daily_mix_import.multiply(tot_consumption_daily, axis='index').resample('D').sum() / 1000


            col1, col2 = st.columns(2)
            with col1:
                create_area_chart(daily_mix_import,title=f"Origins of daily consumer mix by country in {selected_country_name}")
                download_data_as_csv(daily_mix_import, "daily_mix_import.csv")

            tot_electricity_impact_daily_df = tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index >= start_date) &
                                                                                 (tot_electricity_impact_selected_df.index <= end_date)]

            daily_mix_impact = tot_electricity_impact_daily_df.drop(['sum'], axis=1).resample('D').mean()
            with col2:
                create_area_chart(daily_mix_impact, title=f'Daily average of GHG emissions by country (gCO2eq/kWh) in {selected_country_name}')
                download_data_as_csv(daily_mix_impact, "daily_mix_impact.csv")


    elif resolution == 'Horaire':

        # Supposons que flows_selected_df est déjà défini et correctement configuré
        min_date = flows_selected_df.index.min()
        max_date = flows_selected_df.index.max()

        # Positionnement des widgets dans les colonnes si déjà définies
        with col3:  # Exemple de placement dans la colonne
            start_date, end_date = st.date_input(
                "Sélectionnez une plage de dates:",
                [min_date, max_date],  # Utilisez les extrêmes de l'index comme valeur par défaut
                min_value=min_date,  # Date minimale extraite de l'index
                max_value=max_date,  # Date maximale extraite de l'index
                help="Vous pouvez choisir une plage dans les limites des dates disponibles dans les données."
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
            create_combined_time_series(flows_hourly, tot_consumption_hourly, title=f'Hourly Time Series of Production, Imports, and Exports ')
            download_data_as_csv(flows_hourly, "flows_hourly.csv")


        # pour les impacts
        tot_electricity_impact_hourly_df = tot_electricity_impact_selected_df.loc[(tot_electricity_impact_selected_df.index >= start_date) & (
                    tot_electricity_impact_selected_df.index <= end_date)]


        pivot_table = create_pivot_table(tot_electricity_impact_hourly_df['sum'].resample('H').mean())
        with col2:
            create_heatmap(pivot_table, f' Heatmap of the average of GHG emissions  in {selected_country_name}')
            download_data_as_csv(pivot_table, "tot_electricity_impact_hourly_df.csv")
        selection = aggregation_menu()
        if selection == "Mixte":
            raw_consumption_by_src_hourly_df = raw_consumption_by_src_selected_df.loc[(raw_consumption_by_src_selected_df.index >= start_date) & (
                        raw_consumption_by_src_selected_df.index <= end_date)].resample('H').sum()
            raw_consumption_by_src_hourly_df = raw_consumption_by_src_hourly_df.resample('H').sum() / 1000
            raw_consumption_by_src_hourly_df = aggregate_by_country(selected_country_name,raw_consumption_by_src_hourly_df)
            col1, col2 = st.columns(2)
            with col1:
                create_area_mixte(raw_consumption_by_src_hourly_df,
                                              title=f'Hourly consumption by source in {selected_country_name}',text='GWh')
                download_data_as_csv(raw_consumption_by_src_hourly_df, "raw_consumption_by_src_hourly_df.csv")

            electricity_impact_by_src_hourly_df = electricity_impact_by_src_selected_df.loc[(electricity_impact_by_src_selected_df.index >= start_date) & (
                        electricity_impact_by_src_selected_df.index <= end_date)].resample('H').sum()
            electricity_impact_by_src_hourly_df = electricity_impact_by_src_hourly_df.resample('H').mean()
            electricity_impact_by_src_hourly_df = aggregate_by_country(selected_country_name,
                                                                      electricity_impact_by_src_hourly_df)
            with col2:
                create_area_mixte(electricity_impact_by_src_hourly_df,
                                      title=f'Hourly average of GHG emissions by source in {selected_country_name}',text='gCO2/KWh')
                download_data_as_csv(electricity_impact_by_src_hourly_df, "electricity_impact_by_src_hourly_df.csv")


        if selection == "Technologie":

            col1, col2 = st.columns(2)  # Crée deux colonnes pour les graphiques
            with col1:
                techno_hourly_df = (techno_selected_df.loc[
                                    (techno_selected_df.index >= start_date) &
                                    (techno_selected_df.index <= end_date)]
                                .resample('H').sum()) / 1000

                create_area_mixte(techno_hourly_df,
                               title=f'Daily average of GHG emissions by technology in {selected_country_name}',text='GWh')
                download_data_as_csv(techno_hourly_df, "techno_hourly_df.csv")

            with col2:
                techno_impact_hourly_df = techno_impact_selected_df.loc[
                                              (techno_impact_selected_df.index >= start_date) &
                                              (techno_impact_selected_df.index <= end_date)].resample('D').mean()

                create_area_mixte(techno_impact_hourly_df,
                                   title=f'Hourly average of GHG emissions by technology in {selected_country_name}',text='gCO2/KWh')
                download_data_as_csv(techno_impact_hourly_df, "techno_impact_hourly_df.csv")

        if selection == "Pays d'origine":
            tot_electricity_mix_hourly_df = tot_electricity_mix_selected_df.loc[
                (tot_electricity_mix_selected_df.index >= start_date) & (tot_electricity_mix_selected_df.index <= end_date)].resample('H').sum()
            hourly_mix_import = tot_electricity_mix_hourly_df.drop(['sum'], axis=1)
            hourly_mix_import = hourly_mix_import.multiply(tot_consumption_hourly, axis='index').resample('H').sum() / 1000


            col1, col2 = st.columns(2)
            with col1:
                create_area_chart(hourly_mix_import,title=f"Origins of hourly consumer mix by country in {selected_country_name}")
                download_data_as_csv(hourly_mix_import, "hourly_mix_import.csv")

            tot_electricity_impact_hourly_df = tot_electricity_impact_selected_df[(tot_electricity_impact_selected_df.index >= start_date) &
                                                                                 (tot_electricity_impact_selected_df.index <= end_date)]

            hourly_mix_impact = tot_electricity_impact_hourly_df.drop(['sum'], axis=1).resample('H').mean()
            with col2:
                create_area_chart(hourly_mix_impact, title=f'Hourly average of GHG emissions by country in {selected_country_name}')
                download_data_as_csv(hourly_mix_impact, "hourly_mix_impact.csv")

















