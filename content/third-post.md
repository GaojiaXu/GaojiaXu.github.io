title: Blog on Homework 3
date: 10/01/2021
author: Gaojia Xu

Creating effective visualizations using [best practices](https://rafalab.github.io/dsbook/data-visualization-principles.html)
starting with the [data sets](https://github.com/rfordatascience/tidytuesday/tree/master/data/2018/2018-11-13).

I chose the library plotly because it is easy to use, it is also quite similar to the R shiny application form that I was used to. This library is powerful that we can make animations based on the data, design the widgets and layout by ourselves.

Blog outline:

* [3.1 Plot1](#section1)
* [3.2 Plot2](#section2)
* [3.3 Plot3](#section3)
* [3.4 Plot4](#section4)


<a name="section1"></a>
##3.1 Plot1

From this plot, each point indicate an entity. We can see change of malaria death of entities by year. While most of the death numbers per 100,000 people of entities maintain close to 0 throughout the 26 years, there are entites with much higher death nubmers and we can see movement of these points by the animation.

The function looks like this:

```python

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import ipywidgets as widgets
import plotly.graph_objects as go

df_death = pd.read_csv("malaria_deaths.csv")
df_death = df_death.set_axis(['Entity', 'Code', 'Year', 'Death(per 100,000 people)'], axis=1)

fig = px.scatter(df_death, y="Death(per 100,000 people)", animation_frame="Year", animation_group="Entity",         
           hover_name="Entity",
           title="Malaria Death(per 100,000 people) in entities")

fig.update_xaxes(title='Entites')
fig.show()
  
```
<a name="section2"></a>
##3.2 Plot2

From another view, the graph below shows the line plots of Malaria Death of each entity, if we want to see specific trend in one entity, we can double click the name on the right to only display the line plot for that entity.

The function looks like this:

```python
fig = px.line(df_death, x = "Year", y = "Death(per 100,000 people)", color = 'Entity',
              title = "Malaria Death(per 100,000 people) in Entites")
fig.update_traces(line = dict(width = 1))

```
<a name="section3"></a>
##3.3 Plot3

Plot3 means to display the interaction of Malaria Incidence and Death. Moreover, there are two user-chosen entites that can be compared on the graph. The dot for each entity is connected by Year chronologically. 


The function looks like this:

```
df_inc = pd.read_csv("malaria_inc.csv")
df_inc = df_inc.set_axis(['Entity', 'Code', 'Year', 'Incidence(per 1000 people at risk)'], axis=1)
df2 = df_inc.merge(df_death, on=["Entity","Code","Year"])


#design and display widgets
entity1 = widgets.Dropdown(
    options = list(df2['Entity'].unique()),
    value = 'Botswana',
    description = 'Entity 1:',
    continuous_update = True
)

entity2 = widgets.Dropdown(
    options = list(df2['Entity'].unique()),
    value = 'Djibouti',
    description = 'Entity 2:',
    continuous_update = True
)

container = widgets.HBox([entity1, entity2])

#current dataframe for line charts
curr_df1 = df2[(df2['Entity'] == entity1.value)]
curr_df2 = df2[(df2['Entity'] == entity2.value)]

#specify the line charts and layout
trace1 = go.Scatter(x = curr_df1['Incidence(per 1000 people at risk)'], 
                    y = curr_df1['Death(per 100,000 people)'],
                    mode = "lines+markers+text",
                    text = curr_df1['Year'],
                    textposition = "bottom right",
                    name = entity1.value)

trace2 = go.Scatter(x = curr_df2['Incidence(per 1000 people at risk)'], 
                    y = curr_df2['Death(per 100,000 people)'],
                    mode = "lines+markers+text",
                    text = curr_df2['Year'],
                    textposition =  "bottom right",
                    name = entity2.value)

g = go.FigureWidget(data = [trace1,trace2],
                    layout = go.Layout(title = dict(
                        text = 'Malaria incidence(per 1,000 population at risk) and deaths(per 100,000 people)'),
                    template = 'seaborn'))

g.layout.xaxis.title = 'Incidence(per 1000 people at risk)'
g.layout.yaxis.title = 'Death(per 100,000 people)'

#how to update the chart
def get_data(e):
    """Update of line charts"""
    with g.batch_update():
        curr_df1 = df2[(df2['Entity'] == entity1.value)]
        curr_df2 = df2[(df2['Entity'] == entity2.value)]
        g.data[0].x = curr_df1['Incidence(per 1000 people at risk)']
        g.data[0].y = curr_df1['Death(per 100,000 people)']
        g.data[0].name = entity1.value
        
        g.data[1].x = curr_df2['Incidence(per 1000 people at risk)']
        g.data[1].y = curr_df2['Death(per 100,000 people)']
        g.data[1].name = entity2.value
        
        
entity1.observe(get_data, names = "value")
entity2.observe(get_data, names = "value")

widgets.VBox([container,g])


```

<a name="section4"></a>
##3.4 Plot4

Plot4 shows the Malaria death partitioned by 5 age groups. The user can specify widgets about the entity and year.

```python

df_death_age = pd.read_csv("malaria_deaths_age.csv").drop(columns = 'Unnamed: 0')
df_death_age = df_death_age.set_axis(['Entity', 'Code', 'Year', 'Age_group', 'Deaths'], axis=1)
df_death_age['Age_group'] = df_death_age['Age_group'].str.replace('14-May','5-14')

#design and display widgets
entity = widgets.Dropdown(
    options = list(df_death_age['Entity'].unique()),
    value = 'Afghanistan',
    description = 'Entity:',
    continuous_update = True)

year = widgets.IntSlider(
    value = 1990,
    min = 1990,
    max = 2016,
    description = 'Year',
    orientation = 'horizontal',
    continuous_update = True)

container = widgets.VBox([entity, year])

#current dataframe for pie charts
cur_df = df_death_age[(df_death_age['Entity'] == entity.value) & (df_death_age['Year'] == year.value)]

#specify the pie chart and layout
trace1 = go.Pie(labels = cur_df['Age_group'],
                values = cur_df['Deaths'])

g = go.FigureWidget(data = [trace1],
                    layout = go.Layout(title = dict(text = 'Malaria death by age group'),
                    template = 'seaborn'))

g.layout.xaxis.title = 'Year'
g.layout.yaxis.title = 'Death number'

#how to update the chart
def get_data2(e):
    """Update pie charts"""
    with g.batch_update():
        cur_df = df_death_age[(df_death_age['Entity'] == entity.value) & (df_death_age['Year'] == year.value)]
        g.data[0].labels = cur_df['Age_group']
        g.data[0].values = cur_df['Deaths']
         
entity.observe(get_data2, names = "value")
year.observe(get_data2, names = "value")

widgets.VBox([container,g])
```

