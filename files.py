import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from fileUpload.db import get_db
from fileUpload.auth import login_required

bp = Blueprint("files", __name__, url_prefix = "/files")

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    g.catalog = catalog()
    if request.method == 'POST':
        name = request.form["fname"]
        f = request.files["file"]
        id = register_name(name)
        tot, valid = process_file(f, id)
        g.catalog = catalog()
        return render_template('files/upload.html', catalog = g.catalog)
    return render_template('files/upload.html', catalog = g.catalog)


def register_name(name):
    user_id = g.user_id
    if "db" not in g:
        g.db = get_db
    g.db.execute("insert into files (user_id, filename) values (?,?)",(user_id, name))
    id = g.db.execute("SELECT last_insert_rowid() ").fetchone()[0]
    print(id)
    g.db.commit()
    return id


def is_valid_query(qry):
    reg = r"select\s[^\;]+"
    m = re.findall(reg, qry)
    print(qry,reg,m)
    if m:
        return True
    return False

def is_empty(qry):
    reg = r"^\s*$"
    m = re.findall(reg, qry)
    print(qry,reg,m)
    if m:
        return True
    return False

def process_file(file, id):
    data = file.read().decode("utf-8")
    l = len(data)
    lines = data.split(";")
    tot = 0
    valid = 0
    for l in lines:
        if is_valid_query(l):
            valid += 1
            g.db.execute("insert into lines (file_id, line_nr, body) values (?,?,?)",(id, valid, l))
            g.db.commit()
            print("inserted")
        if not is_empty(l):
            tot += 1
    return tot, valid



def catalog():
    if "db" not in g:
        g.db = get_db()
    data = g.db.execute(QRY).fetchall()
    return data


@bp.route("/preview/<int:id>", methods = ["GET"])
def preview(id):
    print(type(id))
    data = g.db.execute("select line_nr, body from lines where file_id = ? limit 10",(id,)).fetchall()
    print(data)
    return render_template('files/preview.html',data = data)


QRY = """
select f.id, f.filename, f.time_uploaded, u.username, max(l.line_nr) as lines
from FILES f
join user u
on f.USER_ID = u.id
join lines l
on f.id = l.file_id
group by f.id, f.filename, f.time_uploaded, u.username
"""
