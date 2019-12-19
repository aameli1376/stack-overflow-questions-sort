from flask import Flask, render_template
from datetime import datetime, timedelta
import json
import re
import webbrowser
from stackapi import StackAPI
N = 7
date_N_days_ago = datetime.now() - timedelta(days=N)
print(datetime.now().hour)



app = Flask(__name__)

#---------online----------
SITE = StackAPI('stackoverflow')
most_voted = SITE.fetch('questions', fromdate=date_N_days_ago, todate=datetime.now(), pagesize=2, order='desc', tagged='android',sort='votes',filter='withbody')
most_voted_items =most_voted['items']
newest = SITE.fetch('questions', fromdate=date_N_days_ago, todate=datetime.now(), pagesize=2, order='desc', tagged='android',sort='creation',filter='withbody')
newest_items = newest['items']
#..........................

#--------------saved---------
with open('voted.json','w') as json_file:
    json.dump(most_voted, json_file)
    #most_voted = json.load(json_file)
    most_voted_items = most_voted['items']

with open('newest.json','w') as json_file:
    json.dump(newest, json_file)
    #newest = json.load(json_file)
    newest_items = newest['items']
#--------------------


for quest in most_voted_items:
    quest['creation_date'] = datetime.fromtimestamp(quest['creation_date']).strftime('%c')
for quest in newest_items:
    quest['creation_date'] = datetime.fromtimestamp(quest['creation_date']).strftime('%c')
@app.route('/')
def hello_world():
    return render_template('home.html',voted_items=most_voted_items,newst_items=newest_items)


if __name__ == '__main__':
    app.run()
