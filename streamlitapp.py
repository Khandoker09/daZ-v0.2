'''
Author:Khandoker Tanjim Ahammad
Date:12.11.23
Purpose: check the technical status of line maintainace unit status
'''
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("Hvv Line Maintanence Unit Status")
    df=pd.read_excel('audit_lat_12_11_23_map.xlsx',index_col=False)
    # User input for search
    fig=px.scatter_mapbox(
    df,
    hover_name='state',
    lon=df['Long'],
    lat=df['Lat'],
    zoom=12,
    color=df['HstName'],
    size=df['state_number']*40,
    #size=df['Name_of_Transport'],
    width=1200,
    height=900,
    title='HVV LMU Service'
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={'r':0,'t':50,'l':50,'b':50})
    #fig.show()
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()