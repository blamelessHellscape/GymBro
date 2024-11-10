import sqlite3
import datetime
import pandas as pd


class Db_Helper:
    db = None

    def __init__(self):
        print('db init')
        self.db = sqlite3.connect('gains.db',  check_same_thread=False)
        self.run_query(
            '''create table if not exists exercise_table(id INTEGER PRIMARY KEY, row_id INTEGER, reps INTEGER, weight INTEGER, user TEXT, exercise TEXT)''')
        self.run_query(
            '''create table if not exists pr_table(id INTEGER PRIMARY KEY, date TEXT, max_weight INTEGER, user TEXT, exercise TEXT)''')
        self.run_query(
            '''create table if not exists exercise_names_table(exercise_name TEXT PRIMARY KEY)'''
        )
        self.db.commit()

    def run_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_pr_data(self, user, exercise):
        query_string = f'''select * from pr_table where user="{user}" and exercise="{exercise}"'''
        results = self.run_query(query_string)
        # print('DB: retrived:',results)
        df = pd.DataFrame(results, columns=[
                          'id', 'date', 'max_weight', 'user', 'exercise'])
        return df

    def insert_pr_data(self, user, exercise, max_weight):
        date = datetime.datetime.now().date()
        exists = self.run_query(f'''select * from pr_table where user="{user}" and exercise="{exercise}" and "{date}"''')
        if exists:
            # print('exists',exists)
            return
        query_string = f'''insert into pr_table(date, max_weight,user,exercise) values ("{date}",{max_weight}, "{user}", "{exercise}")'''
        res = self.run_query(query_string)
        print(query_string)
        self.db.commit()
        # print(f'DB: inserted values {user} {exercise} {max_weight}')
        return res

    def get_exercise_data(self, user, exercise):
        query_string = f'''select * from exercise_table where user="{user}" and exercise="{exercise}" order by row_id asc'''
        # print(query_string)
        res = self.run_query(query_string)
        # print('GET: exercise_table', res)
        ret = [{'reps_col': i[2], 'weight_col': i[3]} for i in res]
        return ret

    def insert_exercise_data(self, table_data, user, exercise):
        # delete all where user and exercise
        query_string = f'''delete from exercise_table where user="{user}" and exercise="{exercise}"'''
        self.run_query(query_string)
        # insert and save highest weight
        max_weight = 0
        for row in table_data:
            # print('ROW:', row)
            if int(row['weight_col']) > max_weight:
                max_weight = int(row['weight_col'])
            query_string = f'''insert into exercise_table(reps,weight,row_id,user,exercise) values(
                {row['reps_col']}, {row['weight_col']},{table_data.index(row)}, "{user}", "{exercise}")'''
            # print(query_string)
            self.run_query(query_string)
        self.db.commit()
        # insert max_weight for max graph
        if max_weight > 0:
            # print('inserting max weight', max_weight)
            self.insert_pr_data(user, exercise, max_weight)


# https://dash.plotly.com/datatable/editable#adding-or-removing-rows
# Table: exercise:: row-id, reps, weight, user, exercise
# Table: pr:: date, max_weight, exercise, user

# select * from exercise where user = USER and exercise = EXERCISE order by row-id asc
# on row update: compare if highest value in data is higher than updated value and if so insert into pr... (literally the insert data function we already have.)
