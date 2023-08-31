import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv('data/preprocessed_funding.csv')

ddf = df
ddf['Month'] = pd.to_datetime(ddf['Month'])

df_geo = gpd.read_file("data/edited_geo_df.shp")


filtered_geo = df_geo.dropna(subset = ['amount_usd'])
company_list = list(set(df['Company']))
continent_list = list(set(filtered_geo['continent']))



metric_dict = {'Count':'count', 'Amount in Millions':'amount_usd'}

#tabs general, geographic, single companies
tab1,tab2,tab3 = st.tabs(['General','Company Overview','Geographic'])

#general metrics count and total
with tab1:
    st.header('General Financial Analysis')
    selected_metric_m = st.selectbox(label = 'Select Metric',options = ['Count','Amount in Millions'])
    selected_metric = metric_dict[selected_metric_m]


    if selected_metric == 'count':
        time_investor = ddf.dropna().groupby('Month').count()['Unnamed: 0']

        by_type = df.groupby('Major Category').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector = df.groupby('Subcategory').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']


        by_type_s = df.dropna().groupby('Strategics').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']
        by_sector_s = df.dropna().groupby('Stage').count().sort_values('Unnamed: 0',ascending=False)['Unnamed: 0']



    elif selected_metric == 'amount_usd':
        time_investor = ddf.dropna().groupby('Month').sum()['amount_usd']

        by_type = df[['Major Category','amount_usd']].groupby('Major Category').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        by_sector = df[['Subcategory','amount_usd']].groupby('Subcategory').sum().sort_values('amount_usd',ascending=False)['amount_usd']


        by_type_s = df[['Strategics','amount_usd']].dropna().groupby('Strategics').sum().sort_values('amount_usd',ascending=False)['amount_usd']
        by_sector_s = df[['Stage','amount_usd']].dropna().groupby('Stage').sum().sort_values('amount_usd',ascending=False)['amount_usd']


    st.subheader('Monthly Analysis')
    figt, mnxt = plt.subplots(1, 1)
    time_investor.plot(kind = 'line', figsize = (20,10), title = 'Investments Made Over Time', ylabel = f'{selected_metric_m}')
    st.pyplot()


    st.subheader('Investor Categories')
    col1,col2 = st.columns(2)
    with col1:
        figmx, mnx = plt.subplots(1, 1)
        by_type.plot(ax = mnx, kind = 'bar',title = 'Investments by Category', ylabel = f'{selected_metric_m}')
        st.pyplot()

    with col2:
        figmxv, mnxv = plt.subplots(1, 1)
        by_sector.plot(ax = mnxv, kind = 'bar',title = 'Investments by Subcategory', ylabel = f'{selected_metric_m}')
        st.pyplot()

    st.subheader('Additional Investment Information')
    col1,col2 = st.columns(2)
    with col1:
        by_sector_s.plot(kind = 'bar',title = 'Investments by Stage', ylabel = f'{selected_metric_m}')
        st.pyplot()
    with col2:
        by_type_s.plot(kind = 'bar',title = 'If Investment is Strategic', ylabel = f'{selected_metric_m}')
        st.pyplot()




#geographic, count and total toggle

#selected_metric = st.dropdown()

with tab2:
    st.header('Company Overview')
    selected_companies = st.multiselect('Select Companies to Analyze', company_list,[company_list[0]])
    filtered_df = df[df['Company'].isin(selected_companies)]
    if filtered_df.empty == False:
        st.subheader('Company Investors')
        lgdf = filtered_df.groupby('Company').agg({'Lead Investor': lambda x: list(x)[0],'Other Investor': lambda x: list(set(x))[0], 'Notes': lambda x: list(set(x))[0]})
        st.table(lgdf)

        st.subheader('Investment Amount in Millions')
        fgdf = filtered_df[['Company','amount_usd','Country']].groupby(['Company']).sum()
        if sum(fgdf['amount_usd']) > 0:
            fgdf['amount_usd'].plot(kind = 'bar', ylabel = 'Amount in Millions')
            st.pyplot()
        else:
            st.write('There is no investment amount found for the selected company')
    else:
        st.write('Please Select a Company')

with tab3:
    st.header('Geography Dashboard')
    selected_metric_m = st.selectbox(label = 'Select Geographic Metric',options = ['Count','Amount in Millions'])
    selected_metrics = metric_dict[selected_metric_m]

    st.subheader('Global Analysis')
    fig, world_ax = plt.subplots(1, 1)
    df_geo.plot(column = selected_metrics, ax = world_ax, legend=True ,legend_kwds={'label': f"{selected_metric_m} of Investments by Country",'orientation': "horizontal"})
    df_geo.boundary.plot(ax=world_ax)
    fig.set_size_inches(18.5, 10.5)
    st.pyplot()

    df_geo[['name',selected_metrics]].dropna().sort_values(selected_metrics, ascending = False).plot(kind = 'bar', x = 'name', title = 'Investment by Country',figsize = (20,10), ylabel = f'{selected_metric_m}')
    st.pyplot()

    st.subheader('Continental Analysis')
    selected_continent =  st.selectbox('Select Continent to Analyze', options = continent_list)
    col1,col2 = st.columns(2)
    fcdf = df_geo[df_geo['continent'] == selected_continent]
    with col1:
        fig2, cont_ax = plt.subplots(1, 1)
        if selected_continent == 'Europe':
            cont_ax.set_xlim(-20, 50)
            cont_ax.set_ylim(30, 70)

        if selected_continent == 'Oceania':
            cont_ax.set_xlim(100, 200)
            cont_ax.set_ylim(-50, -0)

        fcdf.plot(column = selected_metrics, ax = cont_ax, legend=True ,legend_kwds={'label': f"{selected_metric_m} of Investments by Country",'orientation': "horizontal"})
        fcdf.boundary.plot(ax=cont_ax)
        st.pyplot()

    with col2:
        fcdf[['name',selected_metrics]].dropna().sort_values(selected_metrics, ascending = False).plot(kind = 'bar', x = 'name', title = 'Investment by Country within Continent', ylabel = f'{selected_metric_m}')
        st.pyplot()



#single company all info written
#selected_companies = st.multiselect()


# Using object notation
