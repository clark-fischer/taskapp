import sqlite3

con = sqlite3.connect("app.db")
cur = con.cursor()


def get_task_length(num):
    n = cur.execute(f"SELECT id FROM tasks WHERE status_id = {num}")
    return len(list(n))


print(get_task_length(1))
