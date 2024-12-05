import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load datasets
dash_1_data = pd.read_excel('Dash.xlsx', sheet_name='Dash_1')
traffic_data = pd.read_excel('Dash.xlsx', sheet_name='Traffic')
demographic_data = pd.read_excel('Dash.xlsx', sheet_name='Demographic')
exhibition_data = pd.read_excel('Dash.xlsx', sheet_name='Exhibition')

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='dash_1', children=[
        dcc.Tab(label='Dash_1', value='dash_1'),
        dcc.Tab(label='Traffic', value='traffic'),
        dcc.Tab(label='Demographic', value='demographic'),
        dcc.Tab(label='Exhibition', value='exhibition'),
    ]),
    html.Div(id='content')
])

# Callback for updating the content based on the selected tab
@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'value')]
)
def update_tab_content(tab_name):
    if tab_name == 'dash_1':
        # Dash_1 Tab
        fig1 = px.bar(
            dash_1_data,
            x='Date',
            y=['New User', 'Returning User'],
            title="Users Breakdown (New vs Returning)",
            barmode='stack'
        )
        fig2 = px.line(
            dash_1_data,
            x='Date',
            y=['Ad Spend', 'Paid Sales'],
            title="Ad Spend vs Paid Sales"
        )
        fig3 = px.line(
            dash_1_data,
            x='Date',
            y='ROAS',
            title="ROAS Over Time"
        )
        fig4 = px.line(
            dash_1_data,
            x='Date',
            y='AOV',
            title="Average Order Value (AOV)"
        )
        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ])

    elif tab_name == 'traffic':
        # Traffic Tab
        top_cities = traffic_data.groupby('City')['Total Revenue'].sum().nlargest(10).reset_index()
        fig1 = px.bar(
            top_cities,
            x='City',
            y='Total Revenue',
            title="Top 10 Cities by Total Revenue"
        )
        fig2 = px.bar(
            traffic_data,
            x='Type',
            y='Total Revenue',
            title="Revenue by Type"
        )
        fig3 = px.pie(
            traffic_data,
            names='Source',
            values='Total Revenue',
            title="Revenue by Source"
        )
        payment_counts = traffic_data['Payment method'].value_counts()
        fig4 = px.pie(
            payment_counts,
            names=payment_counts.index,
            values=payment_counts.values,
            title="Orders by Payment Method"
        )
        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ])

    elif tab_name == 'demographic':
        # Demographic Tab
        top_cities = demographic_data.nlargest(10, 'Total Users')
        fig1 = px.bar(
            top_cities,
            x='City',
            y=['Total Users', 'Total revenue'],
            title="Top 10 Cities by Users and Revenue",
            barmode='stack'
        )
        return html.Div([
            dcc.Graph(figure=fig1)
        ])

    elif tab_name == 'exhibition':
        # Exhibition Tab
        fig1 = px.bar(
            exhibition_data,
            x='Exhibition Name',
            y='Revenue',
            title="Revenue by Exhibition Name"
        )
        fig2 = px.bar(
            exhibition_data,
            x='Location',
            y='AOV',
            title="AOV by Location"
        )
        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ])

    return html.Div([html.H2("Tab not found")])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
