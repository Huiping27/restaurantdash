# Import the necessary libraries
import dash
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import openpyxl as xl
# Read data from CSV and Excel files
deliverando = pd.read_csv('SalesAnalyst_deliverando.csv', sep=';')
compe_1 = pd.read_excel('SalesAnalyst_Competition.xlsx', sheet_name='Month 1')
compe_2 = pd.read_excel('SalesAnalyst_Competition.xlsx', sheet_name='Month 2')
compe_merge = pd.concat([compe_1, compe_2], ignore_index=True)

# Calculate total active restaurants for Deliverando
active_restaurants_month1 = deliverando[deliverando['Month 1'] > 0]['name'].nunique()
active_restaurants_month2 = deliverando[deliverando['Month 2'] > 0]['name'].nunique()

# Calculate difference and percentage change
difference_deliverando = active_restaurants_month2 - active_restaurants_month1
percentage_deliverando = (difference_deliverando / active_restaurants_month1) * 100

# Create a bar plot for Deliverando
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=['Month 1', 'Month 2'], y=[active_restaurants_month1, active_restaurants_month2], name='Total'))
fig1.update_layout(title='Comparison of Month 1 and Month 2 on Deliverando',
                   xaxis_title='Month',
                   yaxis_title='Total Active Restaurants')

# Calculate total active restaurants for competitors
competition_restaurants_month1 = compe_merge[compe_merge['month'] == 1]['name'].nunique()
competition_restaurants_month2 = compe_merge[compe_merge['month'] == 2]['name'].nunique()

# Calculate difference and percentage change for competitors
difference_competitors = competition_restaurants_month2 - competition_restaurants_month1
percentage_competitors = (difference_competitors / competition_restaurants_month1) * 100

# Create a bar plot for competitors
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=['Month 1', 'Month 2'], y=[competition_restaurants_month1, competition_restaurants_month2], name='Total'))
fig2.update_layout(title='Comparison of Month 1 and Month 2 on Competitors',
                   xaxis_title='Month',
                   yaxis_title='Total Active Restaurants')

# Calculate market share of Deliverando and competitors
deliverando_market_share = deliverando['name'].nunique() / compe_merge['name'].nunique()
competitors_market_share = 1 - deliverando_market_share

# Create a pie plot for market share
fig3 = go.Figure(data=[go.Pie(labels=['Deliverando', 'Competitors'], values=[deliverando_market_share, competitors_market_share])])
fig3.update_layout(title='Compare Market Share Deliverando VS Competitors')

# Calculate exclusive restaurants on competitors
exclusive_to_competitors = compe_merge[compe_merge['month'] == 1]['name'].nunique()
total_competitors = compe_merge['name'].nunique()

# Calculate exclusive ratio
exclusive_ratio = exclusive_to_competitors / total_competitors
rest_market_ratio = 1 - exclusive_ratio

# Create a pie plot for exclusivity
fig4 = go.Figure(data=[go.Pie(labels=['Exclusive', 'Rest'], values=[exclusive_ratio, rest_market_ratio])])
fig4.update_layout(title='Exclusive only VS No Exclusive Competitors')

# Get top 10 active restaurants
restaurant_activity = compe_merge.groupby('name')['orders'].sum().nlargest(10)

# Create a bar plot for top 10 restaurants
fig5 = go.Figure()
fig5.add_trace(go.Bar(x=restaurant_activity.index, y=restaurant_activity.values))
fig5.update_layout(title='Top 10 Restaurants On Competitors',
                   xaxis_title='Category',
                   yaxis_title='Total Orders')

# Initialize the app
app =dash.Dash()
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1('Deliverando and Competitor in Graz'),

    # First graph
    dcc.Graph(id='graph1', figure=fig1),

    # Second graph
    dcc.Graph(id='graph2', figure=fig2),

    # Third graph
    dcc.Graph(id='graph3', figure=fig3),

    # Fourth graph
    dcc.Graph(id='graph4', figure=fig4),

    # Fifth graph
    dcc.Graph(id='graph5', figure=fig5)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
