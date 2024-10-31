from dash import Dash, html, dcc, callback, Output, Input,State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# from db_helper import *
import db_helper

dbh = db_helper.Db_Helper()
USER = 'boy'
OPTIONS = ['boy', 'girl']
EXERCISE_OPTS = ['curls', 'tricep extensions', 'rows',
                 'lat pulldowns', 'flys', 'assisted pullups', 'lateral raises']
CURRENT_EXERCISE = EXERCISE_OPTS[0]
# data = [{'date': 1, 'max_weight': 20},
        # {'date': 2, 'max_weight': 30},
        # {'date': 3, 'max_weight': 20},
        # {'date': 4, 'max_weight': 30},
        # {'date': 5, 'max_weight': 40}
        # ]
# df = pd.DataFrame.from_records(data)
app = Dash()
app.config. external_stylesheets = [dbc.themes.BOOTSTRAP]

app.layout = [
    html.H1(children='GymBro', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.RadioItems(options=OPTIONS, value=USER, id='user_chooser', inline=True),
    html.Hr(),
    dcc.RadioItems(options=EXERCISE_OPTS,
                   value=CURRENT_EXERCISE, id='exercise_chooser',inline=True),
    dcc.Graph(id='weight_graph',figure={}),
    html.Hr(),
    html.Div([
        dbc.Row([
    dbc.Col(dcc.Input(id='max_input', type='text', placeholder='flex emoji', value='')),
    dbc.Col(dbc.Button("Enter", id='max_input_btn', color='primary', n_clicks=0), width=2, className="d-grid col-2 gap-2")
        ])
    ], className="mb-3",)
    ]

@callback(
    Output('weight_graph', 'figure'),
    Output('max_input', 'value'),
    Input('user_chooser', 'value'),
    Input('exercise_chooser', 'value'),
    Input('max_input_btn', 'n_clicks'),
    State('max_input', 'value'),
)
def update_user(user_value, exercise_value, n, new_max):
    print(user_value)
    print(exercise_value)
    USER=user_value
    CURRENT_EXERCISE=exercise_value
    if n and new_max:
        #TODO: insert into DB
        print('entered',new_max)
        dbh.insert_data(USER,CURRENT_EXERCISE,new_max)
        # data.append({'date': 6, 'max_weight': new_max}) #datetime.datetime.now().date()
        # df = pd.DataFrame.from_records(data)
    return update_graph(), ''


def update_graph():
    # fetch from db here
    df = dbh.get_data(USER,CURRENT_EXERCISE)
    return px.line(df, x='date', y='max_weight')


if __name__ == '__main__':
    app.run(debug=True)
