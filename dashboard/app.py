import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data_etl import prepare_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


min_cases = 60
cumul = prepare_data()
available_vars = cumul['show'].unique()

app.layout = html.Div([
    html.H1(
        'The numbers of Covid-19',
        style={
            'textAlign': 'center',
            # 'color': colors['text']
        }
    ),

    dcc.Dropdown(
        id='show-variable',
        options=[{'label': i, 'value': i} for i in available_vars],
        value='cases'
    ),

    dcc.Graph(
        id='cumul-trends'
    ),

    dcc.Input(id='input-min_cases', value=min_cases, type='number')
])


@app.callback(
    Output('cumul-trends', 'figure'),
    [Input('input-min_cases', 'value'),
     Input('show-variable', 'value')])
def update_alignment(min_cases, chosen_var):
    cumul_aligned = cumul[cumul['value'] > min_cases]
    fig = px.line(cumul_aligned[cumul_aligned['show'] == chosen_var], y='value', color='countriesAndTerritories', log_y=False)
    fig.update_layout(title='Cases', xaxis_title='Days from ' + str(min_cases) + 'th case')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)