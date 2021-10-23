import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Read in the data
df2 = pd.read_excel("sed17-sr-tab002.xlsx", header = [4])
df2.columns = ['Year',"Doctorate_granting_institutions",'Doctorate recipients','Mean (per institution)','Median (per institution)']    

df12 = pd.read_excel("sed17-sr-tab012.xlsx", header = [3,4], index_col=[0])
df12_new = df12.loc[["Life sciences", "Physical sciences and earth sciences", 
                "Mathematics and computer sciences",
               "Psychology and social sciences",
               "Engineering","Education", "Humanities and arts", "Other"], :]

df19 = pd.read_excel("sed17-sr-tab019.xlsx", header = [3], index_col=[0])
df19_new = df19.drop(labels=["U.S. citizen or permanent resident", 
                             "Temporary visa holder",
                            "Temporary visa holdera",
                            "Unknown citizenship",
                            "Not Hispanic or Latino",
                            "All doctorate recipients"], axis=0)

nav = st.sidebar.radio("Navigation", ["Introduction",
                                  "Doctorate Recipients and Institution Number through Years",
                                  "Doctorate Recipients Distribution by Major Field of Study",
                                  "Doctorate Recipients Distribution by Ethinicity/Race"])

#navigation choice 1
if nav == "Introduction":
    st.header('Exploration of Doctorate Information in the U.S.')

    col1, col2, col3 = st.columns([1,8,1])
    img = Image.open('phd_image.jpg')
    col2.image(img, use_column_width=True)

    st.markdown('Hi there, this simple applicaiton aims to provide some direct illustrations based on [Science and Engineering PhDs awarded in the US](https://ncses.nsf.gov/pubs/nsf19301/data) datasets, please check the website if you are interested, the datasets had been used are table 2, 12, 19. The code to generate this application had been uploaded to [Blog of Gaojia](https://gaojiaxu.github.io)')

#navigation choice 2
if nav == "Doctorate Recipients and Institution Number through Years":
    st.subheader('General Doctorate Recipients and Granting Institution Number through Years')
    
    #first plot
    fig1 = px.line(df2, x = "Year", y = "Doctorate recipients",
                  title = "Number of Doctorate recipients in 1973~2017")
    st.plotly_chart(fig1)
    
    #second plot
    fig2 = px.histogram(df2, x = "Year", y = "Doctorate_granting_institutions",
                   title = "Number of Doctorate granting institutions in 1973~2017", 
                   nbins=50, opacity=0.75)
    fig2.update_layout(bargap=0.2, yaxis_title_text='Doctorate grating institutions number',
                  yaxis_range=[250,450])
    st.plotly_chart(fig2)

    st.write("From the above plot, there are general increasing trends of both number of doctorate recipients and number of doctorate granting institutions from 1973 to 2017. You may explore deeper about related information from the left sidebar.")

#navigation choice 3
if nav == "Doctorate Recipients Distribution by Major Field of Study":
    st.subheader('Doctorate Recipients Distribution by Major Field of Study')
    year = st.sidebar.slider('You may specify a year', min_value = 1987, max_value = 2017, step = 5, key = int)
    st.write('The year you have chosen is ', year)

    if year:
        df12_new_graph = df12_new.loc[:, df12_new.columns.get_level_values(0) == year].copy()
        df12_new_graph.columns = df12_new_graph.columns.droplevel()
        
        #third plot    
        fig3 = px.pie(df12_new_graph, values = "Number", names = df12_new_graph.index, 
              title = 'Proportion of Doctorate Recipients by Major Field of Study in ' + str(year))
        st.plotly_chart(fig3)
        st.write("If we output as a dataframe, 8 categories have number and percentage of total doctorate recipients in ", year, " as below: ")
        
        #related dataframe
        col1, col2, col3 = st.columns([1,8,1])
        col2.dataframe(df12_new_graph)
        
#navigation choice 4
if nav == "Doctorate Recipients Distribution by Ethinicity/Race":
    st.subheader("Doctorate Recipients Distribution by Ethinicity/Race")
    
    options = st.multiselect('For the below line charts, please choose 3 Ethnicity/Race group:',
     ['Hispanic or Latino', 'American Indian or Alaska Native', 'Asian',
       'Black or African American', 'White', 'More than one race',
       'Other race or race not reported', 'Ethnicity not reported'],
     ['Hispanic or Latino', 'American Indian or Alaska Native', 'Asian'])
    
    #raise error if length of option is not equal to 3
    if len(options) != 3:
        st.error('Please choose exactly 3 options.')
    
    curr_df1 = df19_new[(df19_new.index == options[0])]
    curr_df2 = df19_new[(df19_new.index== options[1])]
    curr_df3 = df19_new[(df19_new.index== options[2])]
    
    #fourth plot
    trace1 = go.Scatter(x = curr_df1.columns, 
                    y = curr_df1.iloc[0,:],
                    mode = "lines+markers+text",                   
                    textposition = "bottom right",
                    name = options[0])

    trace2 = go.Scatter(x = curr_df2.columns, 
                        y = curr_df2.iloc[0,:],
                        mode = "lines+markers+text",
                        textposition = "bottom right",
                        name = options[1])

    trace3 = go.Scatter(x = curr_df3.columns, 
                        y = curr_df3.iloc[0,:],
                        mode = "lines+markers+text",
                        textposition = "bottom right",
                        name = options[2])

    g = go.FigureWidget(data = [trace1,trace2,trace3],
                        layout = go.Layout(autosize=False, width=800,height=600, title = dict(text = 'Comparison of 3 Ethnicities/Races in Doctorate Recipients through Years')))
    
    col1, col2, col3 = st.columns([1,8,1])
    col2.plotly_chart(g)
    
    #fifth plot
    year2 = st.slider('For the below pie chart, please specify a year:', 
                     min_value = 2008, max_value = 2017, step = 1, key = int)
    fig19 = px.pie(df19_new, values = year2, names = df19_new.index, 
                  title='Proportion of Doctorate recipients by Ethnicity/Race in ' + str(year2))
    st.plotly_chart(fig19)



