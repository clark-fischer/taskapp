import eel
import os
import sys
import sqlite3
from uuid import getnode as get_mac

cwd = os.getcwd()
rel_prefix = os.path.dirname(cwd)
init = rel_prefix + r"\eel\web"
index_page = init + r"\html\tab_demo.html"

con = sqlite3.connect("app.db")
cur = con.cursor()

# cur.execute('DROP TABLE tasks')
# cur.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, mac_address VARCHAR(255), status_id INT, task VARCHAR(255), address VARCHAR(255), town VARCHAR(255), field_manager VARCHAR(255), date_called_in DATETIME, date_sent_to_cc DATETIME, notes VARCHAR(255), resolution VARCHAR(255), date_resolved DATETIME);")
# cur.execute("INSERT INTO tasks (task, address, town, field_manager, date_called_in, date_sent_to_cc, notes, resolution, date_resolved) values ('Create App3', 'James', '2021-07-31 12:00:00', 'Creating this very app!', '1', 'Clark'); ")

for i in cur.execute("select * from tasks"):
    print(i)


@eel.expose
def hello():
    print("hello")


@eel.expose
def println(stuff):
    print(stuff)


@eel.expose
def get_task_length(num):
    # 1 = uncomplete
    # 2 = complete
    n = cur.execute(f"SELECT id FROM tasks WHERE status_id = {num}")
    return len(list(n))


@eel.expose
def get_incomplete_rows(num):
    command = """SELECT task, address, town, field_manager, date_called_in, date_sent_to_cc, notes, id  
                 from tasks 
                 where status_id = 1;"""
    return list(cur.execute(command))[num]


@eel.expose
def get_complete_rows(num):
    command = "SELECT task, address, town, field_manager, date_called_in, date_sent_to_cc, notes, resolution, date_resolved, id from tasks where status_id = 2;"
    return list(cur.execute(command))[num]


@eel.expose
def set_complete(num):
    command = "UPDATE tasks SET status_id = 2 WHERE id = "
    cur.execute(command + str(num) + ";")
    con.commit()


@eel.expose
def set_incomplete(num):
    command = "UPDATE tasks SET status_id = 1 WHERE id = "
    cur.execute(command + str(num) + ";")
    con.commit()


@eel.expose
def form_insert(
    mac_address,
    task,
    address,
    town,
    field_manager,
    date_called_in,
    date_sent_to_cc,
    notes,
):
    command = f"INSERT INTO tasks (mac_address, status_id, task, address, town, field_manager, date_called_in, date_sent_to_cc, notes, resolution, date_resolved) values ('{mac_address}', '1', '{task}', '{address}', '{town}', '{field_manager}', '{date_called_in}', '{date_sent_to_cc}',  '{notes}', null, null); "
    print(command)
    cur.execute(command)
    con.commit()


@eel.expose
def final_insert():
    pass


@eel.expose
def get_mac_address():
    return get_mac()


@eel.expose
def search(num, field):
    command = f'SELECT task, address, town, field_manager, date_called_in, date_sent_to_cc, notes, resolution, date_resolved, id from tasks where task LIKE "%{field}%" OR address LIKE "%{field}%" OR town LIKE "%{field}%" OR field_manager LIKE "%{field}%" OR date_called_in LIKE "%{field}%" OR date_sent_to_cc LIKE "%{field}%" OR notes LIKE "%{field}%" OR resolution LIKE "%{field}%" OR date_resolved LIKE "%{field}%";'
    return list(cur.execute(command))[num]


eel.init(init)
eel.start(index_page, size=(720, 720))

con.commit()
con.close()
