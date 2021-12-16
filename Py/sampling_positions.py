#!/usr/bin/env python3

#sample from database


from sqlconnect import connect_sql

import pandas as pd
import sys



cnx,cursor = connect_sql()

def retrive(DB_name,WDL):
    query = ("SELECT * FROM `" + DB_name + "` WHERE `WDL`= '"+ WDL +"'")
    result = cursor.execute(query)
    rows = cursor.fetchall()
    count = cursor.rowcount
    print (count)
    df = pd.DataFrame(rows)
    sample = df.sample(frac = 1, random_state=10)

    return sample

def get_samples(positions):
    DB_name = 'positions_'+ positions
    samples_W = retrive (DB_name,'W')
    samples_D = retrive (DB_name,'D')   
    
    samples_W.columns = ['position', 'winning', 'loasing', 'drawing', 'best','WDL','WDLscore','dtz_score']
    samples_D.columns = ['position', 'winning', 'loasing', 'drawing', 'best','WDL','WDLscore','dtz_score']
    filename_w= '/samples/'+ positions+'_win.csv'
    filename_d= '/samples/'+ positions+'_draw.csv'
    
    samples_W.to_csv(filename_w,index=False)
    samples_D.to_csv(filename_d,index=False)

    
def start():
    filename = sys.argv[1]
    get_samples(filename)

start()
