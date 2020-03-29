import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from data_preparation import get_cumul_plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = get_cumul_plot()


app.layout = html.Div([
    html.H1(
        'Covid-19 cases worldwide trend',
        style={
            'textAlign': 'center',
            # 'color': colors['text']
        }
    ),

    dcc.Graph(
        id='cumul-trends',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)