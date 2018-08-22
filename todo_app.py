import sqlite3 as sql
import random
from datetime import datetime as dt
from flask import Flask, render_template, \
    request, redirect, url_for

DATABASE_PATH = 'todo_app.db'

app = Flask(__name__)


def query_run(statement, flag=False):
    out = []
    try:
        conn = sql.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(statement)
        if flag:
            conn.commit()
        out = cursor.fetchall()
        conn.close()
    except Exception as err:
        print("Database operation failed: ", err)
    return out


@app.route("/")
def todo_read():
    read_query = "SELECT * FROM TODO_APP WHERE TYPE <> 'Done';"
    todo_list = query_run(read_query)
    print(todo_list)
    return render_template("index.html", todo_list=todo_list)


@app.route("/showall", methods=['GET'])
def todo_readall():
    read_query = "SELECT * FROM TODO_APP;"
    todo_list = query_run(read_query)
    return render_template("index_full.html", todo_list=todo_list)


@app.route("/create", methods=['POST'])
def todo_write():
    if request.method == 'POST':
        query_mod = "SELECT MAX(ID) FROM TODO_APP;"
        out = query_run(query_mod)
        if len(out) > 0:
            if type(out[0][0]) == int:
                todo_id = out[0][0] + 1
            else:
                todo_id = 1
        else:
            todo_id = random.randint(1000, 100000)
        date = dt.strftime(dt.today(), '%Y-%m-%d')
        write_query = "INSERT INTO TODO_APP " \
                      "(ID, TASK, TYPE, DATE) VALUES"
        write = "".join([write_query, "(", str(todo_id), ",'",
                         request.form['Task'], "', '",
                        'Ready', "', '", date, "' );"])
        query_run(write, True)

    return redirect(url_for("todo_read"))


@app.route("/delete/<todo_id>", methods=["POST"])
def todo_remove(todo_id):
    if request.method == "POST":
        delete = "DELETE FROM TODO_APP WHERE ID="
        delete_query = "".join([delete, str(todo_id), ";"])
        query_run(delete_query, True)

    return redirect(url_for("todo_read"))


@app.route("/update/<todo_id>", methods=["POST"])
def todo_update(todo_id):
    if request.method == "POST":
        update_query = "UPDATE TODO_APP SET "
        update = "".join([update_query, "Task='",
                          request.form['Task'], "', Type='",
                          request.form['Type'], "', Date='",
                          str(request.form['Date']), "' WHERE ID=",
                          str(todo_id), ";"])
        print(request.form['Task'], request.form['Type'], request.form['Date'],update)
        query_run(update, True)

    return redirect(url_for("todo_read"))


if __name__ == "__main__":
    app.run(debug=True, port=7000)
