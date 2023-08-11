import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv('data/preprocessed_funding.csv')

company_list = list(set(df['Company']))

st.header('Private Financial Dash')



#tabs general, geographic, single companies
tab1,tab2,tab3 = st.tabs(['General','Geographic','Single Companies'])

#general metrics count and total
with tab1:
    st.write(df.head())
    col1,col2 = st.columns(2)
    by_type = df.groupby('Type of transaction').count().sort_values('pkey',ascending=False)['pkey']
    by_sector = df.groupby('Sector').count().sort_values('pkey',ascending=False)['pkey']


    by_type_s = df.dropna().groupby('Type of transaction').sum().sort_values('amount_preprocessed',ascending=False)['amount_preprocessed']
    by_sector_s = df.dropna().groupby('Sector').sum().sort_values('amount_preprocessed',ascending=False)['amount_preprocessed']
    with col1:
        by_type.plot(kind = 'bar')
        st.pyplot()

        by_type_s.plot(kind = 'bar')
        st.pyplot()

    with col2:
        by_sector.plot(kind = 'bar')
        st.pyplot()

        by_sector_s.plot(kind = 'bar')
        st.pyplot()



#geographic, count and total toggle

#selected_metric = st.dropdown()

with tab2:
    selected_metrics = st.selectbox(label = 'Select Geographic Metric',options = ['Count','Amount'])
    if selected_metrics == 'Count':
        gdf = df.groupby('Country').count().sort_values('pkey',ascending=False)['pkey']
        gdf.plot(kind = 'bar')
        st.pyplot()
    elif selected_metrics == 'Amount':
        gdf = df.groupby('Country').sum().sort_values('amount_preprocessed',ascending=False)['amount_preprocessed']
        gdf.plot(kind = 'bar')
        st.pyplot()

#single company all info written
#selected_companies = st.multiselect()

with tab3:
    selected_companies = st.multiselect('Select Companies to Analyze', company_list,[company_list[0]])
    filtered_df = df[df['Company'].isin(selected_companies)]
    str_j_comp = ' ,'.join(filtered_df['Company'])

    lgdf = filtered_df.groupby('Company').agg({'Sector': lambda x: set(x),'Type of transaction': lambda x: list(x)})
    st.write(lgdf)

    fgdf = filtered_df.groupby(['Company']).sum()
    fgdff = fgdf[fgdf['amount_preprocessed']>0]
    fgdff['amount_preprocessed'].plot(kind = 'bar')
    st.pyplot()
# Using object notation
