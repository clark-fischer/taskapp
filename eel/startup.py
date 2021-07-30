import eel
import os
import sys
import sqlite3

cwd = os.getcwd()
rel_prefix = os.path.dirname(cwd)
init = rel_prefix + r'\eel\web'
index_page = init + r'\html\index.html'

con = sqlite3.connect('app.db')
cur = con.cursor()
# cur.execute('DROP TABLE tasks')
# cur.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR(255), creator VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, due_at DATETIME, description VARCHAR(255), status_id INT, users_assigned1 VARCHAR(255), users_assigned2 VARCHAR(255), users_assigned3 VARCHAR(255));")
# cur.execute("INSERT INTO tasks (task, creator, due_at, description, status_id, users_assigned1) values ('Create App', 'Clark', '2021-07-31 12:00:00', 'Creating this very app!', '1', 'Clark'); ")

@eel.expose 
def get_rows(command='SELECT * from tasks;'):
	for row in cur.execute(command):
		return(row)

get_rows()
con.commit()
con.close()


# eel.init(init)
# eel.start(index_page, size=(720, 720))