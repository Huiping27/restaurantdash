#import the necessary libraries
import dash
from dash import Dash, html, dcc # we are adding one more component to be able to add the graphs/tables
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table


deliverando=pd.read_csv('SalesAnalyst_deliverando.csv',sep=';')
compe_1=pd.read_excel('SalesAnalyst_Competition.xlsx',sheet_name= 'Month 1')
compe_2=pd.read_excel('SalesAnalyst_Competition.xlsx',sheet_name= 'Month 2')
compe_merge = pd.concat([compe_1, compe_2], ignore_index=True)



# Calculate total amounts
active_restaurants_month1 = deliverando[deliverando['Month 1'] > 0]['name'].nunique()
active_restaurants_month2 = deliverando[deliverando['Month 2'] > 0]['name'].nunique()

# Calculate difference
difference = active_restaurants_month2 - active_restaurants_month1

# Calculate percentage change
percentage = (difference / active_restaurants_month1) * 100

# Create a bar plot for total amounts and difference
fig1 = go.Figure()

# Add bars for total amounts
fig1.add_trace(go.Bar(x=['Month 1', 'Month 2'], y=[active_restaurants_month1, active_restaurants_month2], name='Total', width=0.4))  # Adjust width parameter

# Add annotation for the difference
fig1.add_annotation(x='Month 2', y=active_restaurants_month2, text=f'Difference: +{difference} ({percentage:.2f}%)', showarrow=True, arrowhead=1, ax=0, ay=-40)

# Update layout
fig1.update_layout(title='Comparison of Month 1 and Month 2 on Deliverando',
                  xaxis_title='Month',
                  yaxis_title='Total Active Restaurants',
                  barmode='group',
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                  yaxis=dict(range=[0, max(active_restaurants_month1, active_restaurants_month2) * 1.1])  # Adjust y-axis range
                  )

# Show plot
fig1.show()
graph1 = dcc.Graph(figure=fig1)

# Calculate total amounts for Month 1 and Month 2
competition_restaurants_m1 = compe_merge[compe_merge['month'] == 1]['name'].nunique()
competition_restaurants_m2 = compe_merge[compe_merge['month'] == 2]['name'].nunique()

# Calculate the difference between Month 1 and Month 2
compe_difference = competition_restaurants_m2 - competition_restaurants_m1

# Calculate the percentage change
percentage = (compe_difference / competition_restaurants_m1) * 100

# Create a bar plot
fig2 = go.Figure()

# Add bars for total amounts
fig2.add_trace(go.Bar(x=['Month 1', 'Month 2'], y=[competition_restaurants_m1, competition_restaurants_m2], name='Total', width=0.4))

# Add annotation for the difference
fig2.add_annotation(x='Month 2', y=competition_restaurants_m2, text=f'Difference: +{compe_difference} ({percentage:.2f}%)', showarrow=True, arrowhead=1, ax=0, ay=-40)

# Update layout
fig2.update_layout(
    title='Comparison of Month 1 and Month 2 on Competitors',
    xaxis_title='Month',
    yaxis_title='Total Active Restaurants',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(competition_restaurants_m1, competition_restaurants_m2) * 1.1])  # Adjust y-axis range
)

# Show the plot
fig2.show()
graph2 = dcc.Graph(figure=fig2)

# Calculate the number of restaurants exclusive to Deliverando
deliverando_restaurants = deliverando['name'].nunique()

# Calculate the total number of restaurants (including both Deliverando and competitors)
total_restaurants = compe_merge['name'].nunique()

# Calculate the market share of Deliverando
deliverando_market_share = deliverando_restaurants / total_restaurants

# Calculate the market share of competitors
competitors_market_share = 1 - deliverando_market_share

# Create a pie plot
fig3 = go.Figure(data=[go.Pie(labels=['Deliverando', 'Competitors'],
                             values=[deliverando_market_share, competitors_market_share])])

# Update layout
fig3.update_layout(title='Compare Market Share Deliverando VS Competitors',
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Show plot
fig3.show()

graph3 = dcc.Graph(figure=fig3)


# Calculate total amounts for Month 1 and Month 2
competition_restaurants = 2932

# Identify restaurants exclusive to competitors
exclusive_to_competitors = 2726

# Create a bar plot
fig4 = go.Figure()

# Add bars for total amounts
fig4.add_trace(go.Bar(x=['Exclusive to Competitors','Total'], y=[ exclusive_to_competitors,competition_restaurants], name='Total', width=0.4))

# Update layout
fig4.update_layout(
    title='Exclusive Restaurants Only On Competitors',
    xaxis_title='Category',
    yaxis_title='Total Active Restaurants',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(exclusive_to_competitors, competition_restaurants) * 1.1])  # Adjust y-axis range
)

# Show the plot
fig4.show()
graph4 = dcc.Graph(figure=fig4)

#Entry the data
competition_restaurants = 2932  

exclusive_to_competitors = 2726  

# Calculate the exclusive ratio
exclusive_ratio = exclusive_to_competitors / competition_restaurants

# Calculate the market share of competitors
rest_market_ratio = 1 - exclusive_ratio

# Create a pie plot
fig5 = go.Figure(data=[go.Pie(labels=['Exclusive', 'Rest'],
                             values=[exclusive_ratio, rest_market_ratio])])

# Update layout
fig5.update_layout(title='Exclusive only VS No Exclusive Competitors',
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Show plot
fig5.show()
graph5 = dcc.Graph(figure=fig5)

restaurant_activity = compe_merge.groupby('name')['orders'].sum()

# Sort the restaurants based on the total orders in descending order
sorted_restaurants = restaurant_activity.sort_values(ascending=False)

# Get the top 10 active restaurants
top_10_active_restaurants = sorted_restaurants.head(10)

# Create a bar plot
fig6 = go.Figure()

# Add bars for total amounts
fig6.add_trace(go.Bar(x=top_10_active_restaurants.index, y=top_10_active_restaurants.values))

# Update layout
fig6.update_layout(
    title='Top 10 Restaurants On Competitors',
    xaxis_title='Category',
    yaxis_title='Total Orders',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(top_10_active_restaurants.values) * 1.5]),  # Adjust y-axis range
    height=600,  # Set the height of the figure
    width=1100    # Set the width of the figure
)

# Show the plot
fig6.show()

graph6 = dcc.Graph(figure=fig6)

restaurant_activity = compe_merge.groupby('name')['orders'].sum()

# Sort the restaurants based on the total orders in descending order
sorted_restaurants = restaurant_activity.sort_values(ascending=False)

# Get the top 10 active restaurants
top_10_active_restaurants = sorted_restaurants.head(10)

# Create a bar plot
fig6 = go.Figure()

# Add bars for total amounts
fig6.add_trace(go.Bar(x=top_10_active_restaurants.index, y=top_10_active_restaurants.values))

# Update layout
fig6.update_layout(
    title='Top 10 Restaurants On Competitors',
    xaxis_title='Category',
    yaxis_title='Total Orders',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(top_10_active_restaurants.values) * 1.5]),  # Adjust y-axis range
    height=600,  # Set the height of the figure
    width=1100    # Set the width of the figure
)

# Show the plot
fig6.show()

graph6 = dcc.Graph(figure=fig6)

# initializing the app
app = dash.Dash()

server = app.server
# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Deliverando and Competitor in Graz'),

    # First graph
    dcc.Graph(
        id='graph1',
        figure=fig1 
    ),

    # Second graph
    dcc.Graph(
        id='graph2',
        figure=fig2  
    ),

    # Third graph
    dcc.Graph(
        id='graph3',
        figure=fig3  
    ),

    # Fourth graph
    dcc.Graph(
        id='graph4',
        figure=fig4  
    ),
      # Fifthth graph
    dcc.Graph(
        id='graph5',
        figure=fig5  
    ),  
    # Sixth graph
    dcc.Graph(
        id='graph6',
        figure=fig6  
    ),  
    # Seven graph
    dcc.Graph(
        id='graph7',
        figure=fig7  
    ),
    
])

# Run the app
if __name__ == '__main__':
    app.run_server(port=8059)