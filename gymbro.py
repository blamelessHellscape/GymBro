from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import db_helper

dbh = db_helper.Db_Helper()
OPTIONS = ['boy', 'girl']
EXERCISE_OPTS = ['curls', 'tricep extensions', 'rows',
                 'lat pulldowns', 'flys', 'assisted pullups', 'lateral raises']

app = Dash()
app.config.external_stylesheets = [dbc.themes.CYBORG]

app.layout = [
    html.H1(children='GymBro', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.RadioItems(options=OPTIONS,
                   value=OPTIONS[0], id='user_chooser', inline=True),
    html.Hr(),
    dcc.RadioItems(options=EXERCISE_OPTS,
                   value=EXERCISE_OPTS[0], id='exercise_chooser', inline=True),
    dcc.Graph(id='weight_graph', figure={}),
    html.Hr(),
    html.Div([
        dbc.Row([
            dbc.Label("Max Weight Today", html_for='max_input'),
            dbc.Col(dcc.Input(id='max_input', type='text',
                    placeholder='Max', value='')),
            dbc.Col(dbc.Button("Enter", id='max_input_btn', color='primary',
                    n_clicks=0))
        ]),
        dbc.Row([
            dbc.Button("Undo Last Entry", id='undo_btn',
                       color='secondary', n_clicks=0)
        ])
    ])
]


@callback(
    Output('weight_graph', 'figure'),
    Output('max_input', 'value'),
    Input('user_chooser', 'value'),
    Input('exercise_chooser', 'value'),
    Input('max_input_btn', 'n_clicks'),
    State('max_input', 'value'),
    Input('undo_btn', 'n_clicks')
)
def update_user(user_value, exercise_value, n, new_max, n_undo):
    print('USER:', user_value)
    print('EXERCISE', exercise_value)
    if n and new_max:
        print('entered', new_max)
        status = dbh.insert_data(user_value, exercise_value, new_max)
    if n_undo:
        dbh.remove_last_row()
    return update_graph(user_value, exercise_value), ''


def update_graph(user, exercise):
    df = dbh.get_data(user, exercise)
    return px.line(df, x='date', y='max_weight', title=f'Max Weight of {exercise.upper()} Over Time')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
