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
        print(query_string)
        results = self.run_query(query_string)
        print(type(results),results)
        df = pd.DataFrame(results, columns=['id','date','max_weight','user','exercise'])
        print(df.head())
        return df

    def insert_data(self,user, exercise, max_weight):
        self.run_query(f'''insert into exercises(date, max_weight,user,exercise) values ("{datetime.datetime.now().date()}",{max_weight}, "{user}", "{exercise}")''')
        print(f'inserted values {user} {exercise} {max_weight}' )