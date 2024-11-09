from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import db_helper

#TODO: save data in dict and majke button to finalize changes

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
    # html.Div([
    #     dbc.Row([
    #         dbc.Label("Max Weight Today", html_for='max_input'),
    #         dbc.Col(dcc.Input(id='max_input', type='text',
    #                 placeholder='Max', value='')),
    #         dbc.Col(dbc.Button("Enter", id='max_input_btn', color='primary',
    #                 n_clicks=0))
    #     ]),
    #     dbc.Row([
    #         dbc.Button("Undo Last Entry", id='undo_btn',
    #                    color='secondary', n_clicks=0)
    #     ])
    # ]),
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
        html.Button('Add Row', id='add_row_btn', n_clicks=0),
        html.Button('Save Data', id='save_data_btn', n_clicks=0)
    ])
    ])
]



# @callback(
#     Output('workout_table', 'data', allow_duplicate=True),
#     Input('workout_table', 'data_timestamp'),
#     State('workout_table', 'data'),
#     State('workout_table', 'columns'), prevent_initial_call=True)
# def edit_table(timestamp, rows, columns):
#     print(rows)
#     if timestamp > TIMESTAMP:
#         for i in range(0,len(rows)):
#             reps = rows[i]['reps_col']
#             weight = rows[i]['weight_col']
#             row_id = i
#             if not reps:
#                 reps = 0
#             if not weight:
#                 weight = 0

#     # print('im crying', something)
#     return rows


# def save_table_data(save_clicks, table_data):
    
    # return

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
    print('USER:', user_value)
    USER = user_value
    print('EXERCISE', exercise_value)
    EXERCISE = exercise_value

    rows = get_table_data(USER, EXERCISE)
    print('displaying rows', rows)
    if add_row > 0:
        rows.extend(INITIAL_DATA)
        return update_graph(user_value, exercise_value), rows
    
    if save_clicks > 0:
        print('save:', table_data)
        dbh.insert_exercise_data(table_data,USER, EXERCISE)
        return update_graph(user_value, exercise_value), table_data
        # for row in table_data:
        #     print('ROW:', row) 
        #     dbh.insert_exercise_data(row['reps_col'], row['weight_col'], table_data.index(row), USER, EXERCISE)

    return update_graph(user_value, exercise_value), rows


def get_table_data(user, exercise):
    df = dbh.get_exercise_data(user, exercise)
    return df

def update_graph(user, exercise):
    df = dbh.get_pr_data(user, exercise)
    return px.line(df, x='date', y='max_weight', title=f'Max Weight of {exercise.upper()} Over Time')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
