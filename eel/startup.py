"""Created by Clark Fischer in mid 2021
   taskapp is the temporary name for a task scheduling service.
   The program is designed to run on the H: drive,
   and let any user add tasks and watch them be completed.
"""

import os
import sqlite3
from uuid import getnode as get_mac
import eel


cwd = os.getcwd()
rel_prefix = os.path.dirname(cwd)
init = rel_prefix + r"\eel\web"
index_page = init + r"\html\tab_demo_i.html"

con = sqlite3.connect("app.db")
cur = con.cursor()


for i in cur.execute("select * from tasks"):
    print(i)

def reset_table():
    """drops then recreates table"""

    cur.execute('DROP TABLE tasks')

    cur.execute("""CREATE TABLE tasks
                (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                mac_address VARCHAR(255), status_id INT, task VARCHAR(255),
                address VARCHAR(255), town VARCHAR(255), field_manager VARCHAR(255), 
                date_called_in DATETIME, date_sent_to_cc DATETIME, notes VARCHAR(255),
                resolution VARCHAR(255), date_resolved DATETIME);""")


@eel.expose
def hello():
    """only used as a test from js --> python"""
    print("hello")


@eel.expose
def println(stuff):
    """similarly used as a test from js --> python,
    but now also allows for input to be tested as well
    """
    print(stuff)

@eel.expose
def get_status_rows(num, status_id, complete=False):
    """takes a status_id and finds all rows with that status.
        those rows are then returned to the python function
    """
    if not complete:
        command = f"""SELECT task, address, town, field_manager,
                     date_called_in, date_sent_to_cc, notes, id  
                     from tasks
                     where status_id = {status_id};"""
                     

    return list(cur.execute(command))[num]

# @eel.expose
# def get_status_rows(num):
#     """takes a status_id and finds all rows with that status.
#         those rows are then returned to the python function
#     """
#     command = f"""SELECT resolution, date
#                  from tasks
#                  where status_id = 2;"""

#     return list(cur.execute(command))[num]

@eel.expose
def get_task_length(status_id):
    """takes a status_id and finds all rows with that status.
    those rows are then returned to the python function,
    made into a list, and counted, finding the length
    """
    # 1 = uncomplete
    # 2 = complete
    return len(list(cur.execute(f"SELECT id FROM tasks WHERE status_id = {status_id}")))


@eel.expose
def set_status(num, status_id):
    """Takes a status_id and an id, and sets the status at the id"""
    command = f"UPDATE tasks SET status_id = {status_id} WHERE id = {num};"
    print(command)
    cur.execute(command)
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
    """Used on the newtask.html form.
    Should be noted that the `resolution` and `date_resolved` columns are left null,
    so they can filled later when the problem is actually resolved
    """
    command = f"""INSERT INTO tasks
                (mac_address, status_id, task, address, town, field_manager, date_called_in,
                date_sent_to_cc, notes, resolution, date_resolved)
                values ('{mac_address}', '1', '{task}',
                '{address}', '{town}', '{field_manager}', '{date_called_in}',
                '{date_sent_to_cc}',  '{notes}', null, null); """
    print(command)
    cur.execute(command)
    con.commit()


@eel.expose
def final_insert(resolution, date_resolved, idd):
    """will be used to complete a task, insert `resolution` & `date_resolved`"""
    command = f"""UPDATE tasks SET resolution = "{resolution}", date_resolved = "{date_resolved}" where id = {idd};"""
    print(command)
    cur.execute(command)
    con.commit()
    

@eel.expose
def get_mac_address():
    """used to log some sort of unqiue id; should be comvined with the ip address at some point"""
    return get_mac()


@eel.expose
def search(num, field):
    """Just searches every field for a given string, the field argument"""
    command = f"""SELECT task, address, town, field_manager, date_called_in,
                  date_sent_to_cc, notes, resolution, date_resolved, id
                  from tasks where task LIKE "%{field}%" OR address LIKE "%{field}%" OR town LIKE "%{field}%" OR
                  field_manager LIKE "%{field}%" OR date_called_in LIKE "%{field}%" OR date_sent_to_cc LIKE "%{field}%" 
                  OR notes LIKE "%{field}%" OR resolution LIKE "%{field}%"
                  OR date_resolved LIKE "%{field}%";"""
    return list(cur.execute(command))[num]


eel.init(init)
eel.start(index_page, size=(720, 720))

con.commit()
con.close()

#She sent me an email with what fields she wants added , and they have since been added