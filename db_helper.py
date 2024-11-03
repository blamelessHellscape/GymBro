import sqlite3
import datetime
import pandas as pd

class Db_Helper:
    db = None
    def __init__(self):
        print('db init')
        self.db = sqlite3.connect('gains.db',  check_same_thread=False)
        self.run_query('''create table if not exists exercises(id INTEGER PRIMARY KEY, date TEXT, max_weight INTEGER, user TEXT, exercise TEXT)''')
        self.db.commit()
    
    def run_query(self, query): 
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_data(self,user, exercise):
        query_string = f'''select * from exercises where user="{user}" and exercise="{exercise}"'''
        results = self.run_query(query_string)
        print('DB: retrived:',results)
        df = pd.DataFrame(results, columns=['id','date','max_weight','user','exercise'])
        return df

    def insert_data(self,user, exercise, max_weight):
        res = self.run_query(f'''insert into exercises(date, max_weight,user,exercise) values ("{datetime.datetime.now().date()}",{max_weight}, "{user}", "{exercise}")''')
        self.db.commit()
        print(f'DB: inserted values {user} {exercise} {max_weight}' )
        return res
    
    def remove_last_row(self):
        query = '''delete from exercises where id= (select max(id) from exercises)'''
        res = self.run_query(query)
        self.db.commit()
        return res
    
#https://dash.plotly.com/datatable/editable#adding-or-removing-rows
#Table: exercise:: row-id, reps, weight, user, exercise
#Table: pr:: date, max_weight, exercise, user