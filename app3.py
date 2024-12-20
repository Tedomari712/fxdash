# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import os

# Initialize the app with custom styling
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
    ]
)

# This is important for Render deployment
server = app.server

# Custom CSS for consistent font styling and enhanced visuals
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Treasury Department 2024</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: 'Bebas Neue', sans-serif;
            }
            .regular-text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .card-body p, .card-body text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .card {
                margin-bottom: 1rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .partner-logo {
                width: 100px;
                height: 100px;
                object-fit: contain;
                margin: 10px;
            }
            .market-share-card {
                background: linear-gradient(135deg, #f6f9fc 0%, #f1f4f8 100%);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''

# Create DataFrames with the data
monthly_data = pd.DataFrame({
    'Month': ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'],
    'FX_Volume': [10695001.00, 6050000.00, 12668000.00, 9250000.00, 8050000.00, 7900000.00, 6250000.00, 12204100.00, 8112800.00, 23360000.00, 16290055.00, 7830000.00],
    'FX_Income': [8381251.00, 4884250.00, 3301000.00, 5382500.00, 2225000.00, -30500.00, 925000.00, 779850.00, 536840.00, -319150.00, -675202.25, -861182.00]
})

partner_data = pd.DataFrame({
    'Month': ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'],
    'LEMFI': [8500000.00, 4750000.00, 10100000.00, 7150000.00, 6250000.00, 7500000.00, 6250000.00, 10149900.00, 6950000.00, 15250000.00, 14950000.00, 6950000.00],
    'NALA': [1995000.00, 500000.00, 2568000.00, 18000000.00, 1300000.00, 400000.00, 0.00, 1995000.00, 100000.00, 3260000.00, 710000.00, 0.00],
    'DLOCAL': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1000000.00, 1150000.00, 470000.00, 0.00],
    'STARKS': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 300000.00]
})

# Calculate market share
total_volume = partner_data[['LEMFI', 'NALA', 'DLOCAL', 'STARKS']].sum().sum()
market_shares = {
    'LEMFI': partner_data['LEMFI'].sum() / total_volume * 100,
    'NALA': partner_data['NALA'].sum() / total_volume * 100,
    'DLOCAL': partner_data['DLOCAL'].sum() / total_volume * 100,
    'STARKS': partner_data['STARKS'].sum() / total_volume * 100
}

# App Layout
app.layout = dbc.Container([
    # Header with logo and title
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='/assets/vngrd.PNG',
                     className='logo', 
                     style={'height': '150px', 'object-fit': 'contain'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '40px', 'marginBottom': '30px', 'width': '100%'}),
            html.H1("Treasury Department Analysis 2024", 
                   className="text-primary text-center mb-4",
                   style={'letterSpacing': '2px'})
        ])
    ]),

    # Key Metrics Cards with Enhanced Design
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-primary mb-3"),
                        html.H5("Cumulative Volume", className="card-title text-center"),
                        html.H2(f"USD {104539901:,.2f}", 
                               className="text-primary text-center"),
                        dcc.Graph(
                            figure=go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=20.91,
                                title={'text': "Target Progress"},
                                gauge={'axis': {'range': [0, 100]},
                                       'bar': {'color': "#1a76ff"},
                                       'threshold': {
                                           'line': {'color': "red", 'width': 4},
                                           'thickness': 0.75,
                                           'value': 20.91
                                       }},
                                number={'suffix': "%"}
                            )).update_layout(height=150, margin=dict(l=20, r=20, t=30, b=20))
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-money-bill-wave fa-2x text-success mb-3"),
                        html.H5("Total FX Income", className="card-title text-center"),
                        html.H2(f"KES {26066041:,.2f}", 
                               className="text-primary text-center"),
                        dcc.Graph(
                            figure=go.Figure(go.Indicator(
                                mode="delta",
                                value=26066041,
                                delta={'reference': 30000000,
                                      'relative': True,
                                      'position': "bottom"},
                            )).update_layout(height=150, margin=dict(l=20, r=20, t=30, b=20))
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-bullseye fa-2x text-danger mb-3"),
                        html.H5("Annual Target Gap", className="card-title text-center"),
                        html.H2(f"USD {395460099:,.2f}", 
                               className="text-primary text-center"),
                        html.Div([
                            dcc.Graph(
                                figure=go.Figure(go.Indicator(
                                    mode="number+delta",
                                    value=79.09,
                                    delta={'reference': 100,
                                          'relative': True,
                                          'position': "bottom"},
                                    number={'suffix': "%"}
                                )).update_layout(height=150, margin=dict(l=20, r=20, t=30, b=20))
                            )
                        ])
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

    # Enhanced Visualizations
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Performance Overview"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=make_subplots(
                            rows=2, cols=1,
                            subplot_titles=("FX Volume Trend", "FX Income Distribution"),
                            specs=[[{"type": "scatter"}],
                                  [{"type": "bar"}]],
                            vertical_spacing=0.12
                        ).add_trace(
                            go.Scatter(
                                x=monthly_data['Month'],
                                y=monthly_data['FX_Volume'],
                                mode='lines+markers',
                                name='FX Volume',
                                line=dict(width=3, color='#1a76ff'),
                                marker=dict(size=8)
                            ),
                            row=1, col=1
                        ).add_trace(
                            go.Bar(
                                x=monthly_data['Month'],
                                y=monthly_data['FX_Income'],
                                name='FX Income',
                                marker_color=['#28a745' if x >= 0 else '#dc3545' 
                                            for x in monthly_data['FX_Income']]
                            ),
                            row=2, col=1
                        ).update_layout(
                            height=700,
                            showlegend=True,
                            template='plotly_white',
                            margin=dict(l=60, r=30, t=100, b=60)
                        )
                    )
                ])
            ], className="shadow-sm mb-4")
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Partner Market Share"),
                dbc.CardBody([
                    html.Div([
                        html.Img(src='/assets/LEMFI.png', className='partner-logo'),
                        html.Img(src='/assets/Nala.png', className='partner-logo'),
                        html.Img(src='/assets/Dlocal.png', className='partner-logo'),
                        html.Img(src='/assets/Starks.JPG', className='partner-logo'),
                    ], className="d-flex justify-content-around mb-4"),
                    dcc.Graph(
                        figure=go.Figure(data=[go.Pie(
                            labels=list(market_shares.keys()),
                            values=list(market_shares.values()),
                            hole=.3,
                            marker=dict(colors=['#1a76ff', '#28a745', '#ffc107', '#dc3545']),
                            textinfo='percent+label',
                            textposition='outside',
                            pull=[0.1 if x == max(market_shares.values()) else 0 
                                  for x in market_shares.values()]
                        )]).update_layout(
                            height=400,
                            margin=dict(l=20, r=20, t=30, b=20)
                        )
                    )
                ])
            ], className="shadow-sm mb-4"),
            
            dbc.Card([
                dbc.CardHeader("Partner Volume Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.area(
                            partner_data,
                            x='Month',
                            y=['LEMFI', 'NALA', 'DLOCAL', 'STARKS'],
                            title='Monthly Volume by Partner',
                            labels={'value': 'Volume (USD)', 'variable': 'Partner'},
                        ).update_layout(
                            height=300,
                            showlegend=True,
                            margin=dict(l=40, r=20, t=60, b=40)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=4)
    ]),

    # Additional Insights
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Performance Matrix"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.scatter(
                            monthly_data,
                            x='FX_Volume',
                            y='FX_Income',
                            size=[1000000] * len(monthly_data),
                            text='Month',
                            title='Volume vs Income Correlation'
                        ).update_traces(
                            textposition='top center'
                        ).update_layout(
                            height=400,
                            showlegend=False,
                            margin=dict(l=40, r=20, t=60, b=40)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4")

], fluid=True, className="p-4")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)
