from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import db_helper

#TODO: save data in dict and majke button to finalize changes

dbh = db_helper.Db_Helper()
INITIAL_DATA = []
TIMESTAMP = 0
OPTIONS = ['boy', 'girl']
USER = OPTIONS[0]
EXERCISE_OPTS = ['curls', 'tricep extensions', 'rows',
                 'lat pulldowns', 'flys', 'assisted pullups', 'lateral raises']
EXERCISE = EXERCISE_OPTS[0]

app = Dash()
app.config.external_stylesheets = [dbc.themes.CYBORG]

app.layout = [
    html.H1(children='GymBro', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.RadioItems(options=OPTIONS,
                   value=USER, id='user_chooser', inline=True),
    html.Hr(),
    dcc.RadioItems(options=EXERCISE_OPTS,
                   value=EXERCISE, id='exercise_chooser', inline=True),
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
    ]),
    html.Div([
        dash_table.DataTable(
             id='workout_table',
             columns=[
                {'name': 'Reps', 'id': 'reps_col'},
                {'name': 'Weight', 'id': 'weight_col'}
             ],
             data=INITIAL_DATA,
             editable=True,
             row_deletable=True
             ),

        html.Button('Add Row', id='editing-rows-button', n_clicks=0)
    ])
]


@callback(
    Output('workout_table', 'data', allow_duplicate=True),
    Input('editing-rows-button', 'n_clicks'),
    State('workout_table', 'data'),
    State('workout_table', 'columns'), prevent_initial_call=True)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@callback(
    Output('workout_table', 'data', allow_duplicate=True),
    Input('workout_table', 'data_timestamp'),
    State('workout_table', 'data'),
    State('workout_table', 'columns'), prevent_initial_call=True)
def edit_table(timestamp, rows, columns):
    print(rows)
    if timestamp > TIMESTAMP:
        for i in range(0,len(rows)):
            reps = rows[i]['reps_col']
            weight = rows[i]['weight_col']
            row_id = i
            if not reps:
                reps = 0
            if not weight:
                weight = 0
            dbh.insert_exercise_data(reps, weight, row_id, USER, EXERCISE)

    # print('im crying', something)
    return rows


@callback(
    Output('weight_graph', 'figure'),
    Output('max_input', 'value'),
    Output('workout_table', 'data'),
    Input('user_chooser', 'value'),
    Input('exercise_chooser', 'value'),
    Input('max_input_btn', 'n_clicks'),
    State('max_input', 'value'),
    Input('undo_btn', 'n_clicks')
)
def update_user(user_value, exercise_value, n, new_max, n_undo):
    print('USER:', user_value)
    USER = user_value
    print('EXERCISE', exercise_value)
    EXERCISE = exercise_value
    INITIAL_DATA = dbh.get_exercise_data(USER, EXERCISE)
    
    if n and new_max:
        print('entered', new_max)
        status = dbh.insert_data(user_value, exercise_value, new_max)
    if n_undo:
        dbh.remove_last_row()
    return update_graph(user_value, exercise_value), '', INITIAL_DATA


def update_graph(user, exercise):
    df = dbh.get_pr_data(user, exercise)
    return px.line(df, x='date', y='max_weight', title=f'Max Weight of {exercise.upper()} Over Time')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
