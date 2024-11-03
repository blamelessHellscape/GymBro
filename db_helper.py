import sqlite3
import datetime
import pandas as pd

class Db_Helper:
    db = None
    def __init__(self):
        print('db init')
        self.db = sqlite3.connect('gains.db',  check_same_thread=False)
        self.run_query('''create table if not exists exercise_table(id INTEGER PRIMARY KEY, row_id INTEGER, weight INTEGER, user TEXT, exercise TEXT)''')
        self.run_query('''create table if not exists pr_table(id INTEGER PRIMARY KEY, date TEXT, max_weight INTEGER, user TEXT, exercise TEXT)''')
        self.db.commit()
    
    def run_query(self, query): 
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_pr_data(self,user, exercise):
        query_string = f'''select * from pr_table where user="{user}" and exercise="{exercise}"'''
        results = self.run_query(query_string)
        print('DB: retrived:',results)
        df = pd.DataFrame(results, columns=['id','date','max_weight','user','exercise'])
        return df

    def insert_pr_data(self,user, exercise, max_weight):
        res = self.run_query(f'''insert into pr_table(date, max_weight,user,exercise) values ("{datetime.datetime.now().date()}",{max_weight}, "{user}", "{exercise}")''')
        self.db.commit()
        print(f'DB: inserted values {user} {exercise} {max_weight}' )
        return res
    
    def remove_last_pr_row(self):
        query = '''delete from pr_table where id= (select max(id) from exercises)'''
        res = self.run_query(query)
        self.db.commit()
        return res
    
    def get_exercise_data(self, user, exercise):
        query_string = f'''select * from exercise_table where user="{user}" and exercise="{exercise} order by row_id asc"'''
    
#https://dash.plotly.com/datatable/editable#adding-or-removing-rows
#Table: exercise:: row-id, reps, weight, user, exercise
#Table: pr:: date, max_weight, exercise, user

#select * from exercise where user = USER and exercise = EXERCISE order by row-id asc
#on row update: compare if highest value in data is higher than updated value and if so insert into pr... (literally the insert data function we already have.)