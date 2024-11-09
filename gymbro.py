from dash import Dash, html, dcc, callback, Output, Input, State, dash_table, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import db_helper

dbh = db_helper.Db_Helper()
INITIAL_DATA = [{'reps_col': '', 'weight_col': ''}]
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
        dbc.Row([
            html.Hr(),
            html.Button('Add Row', id='add_row_btn'),
            html.Button('Save Data', id='save_data_btn')
        ])
    ])
]


@callback(
    Output('weight_graph', 'figure'),
    Output('workout_table', 'data'),
    Input('user_chooser', 'value'),
    Input('exercise_chooser', 'value'),
    Input('save_data_btn', 'n_clicks'),
    Input('add_row_btn', 'n_clicks'),
    State('workout_table', 'data')
)
def update_user(user_value, exercise_value, save_clicks, add_row, table_data):
    # https://stackoverflow.com/questions/62119605/dash-how-to-callback-depending-on-which-button-is-being-clicked
    trigger = callback_context.triggered[0]['prop_id'].split('.')[0]
    # print('TRIGGER',trigger)
    global USER
    global EXERCISE
    
    # print('USER:', user_value)
    # print('EXERCISE', exercise_value)
    rows = get_table_data(USER, EXERCISE)

    # print('displaying rows', rows)
    # print('table_data', table_data)
    # print('interesection', [i for i in table_data if i not in rows])
    # print('-----')
    rows.extend([i for i in table_data if i not in rows])
    match trigger:
        case 'user_chooser':
            USER = user_value
            rows = get_table_data(USER, EXERCISE)
        case 'exercise_chooser':
            EXERCISE = exercise_value
            rows = get_table_data(USER, EXERCISE)
        case 'add_row_btn':
            rows.extend(INITIAL_DATA)
            return update_graph(user_value, exercise_value), rows
        case 'save_data_btn':
            # print('save:', table_data)
            if table_data[-1]['reps_col'] == '': #bad if there are 2+ empty rows, too lazy to fix
                del table_data[-1]
            dbh.insert_exercise_data(table_data, USER, EXERCISE)
            rows = get_table_data(USER, EXERCISE)
            return update_graph(user_value, exercise_value), rows
        
    return update_graph(user_value, exercise_value), rows


def get_table_data(user, exercise):
    df = dbh.get_exercise_data(user, exercise)
    return df


def update_graph(user, exercise):
    df = dbh.get_pr_data(user, exercise)
    return px.line(df, x='date', y='max_weight', title=f'Max Weight of {exercise.upper()} Over Time')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
