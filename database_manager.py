import sqlite3 as sql


def listNotes():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM notes").fetchall()
    con.close()
    return data


def insertContact(email, password):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO contact_list (email,password) VALUES (?,?)", (email, password)
        )
        val = 0
    except sql.IntegrityError:
        print("Email already added")
        val = 1
    con.commit()
    con.close()
    return val


def checkContact(email, password):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        if (
            len(
                cur.execute(
                    "SELECT email, password FROM contact_list WHERE email = ? AND password = ?",
                    (email, password),
                ).fetchall()
            )
            == 1
        ):
            return True
        else:
            return False
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    con.commit()
    con.close()
    return False


def addnote(user, text, title):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO notes (user, text, title) VALUES (?,?,?)", (user, text, title)
        )
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return 1
    con.commit()
    con.close()
    return 0


def search(search, tag):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        if tag != "":
            if (
                len(
                    cur.execute(
                        "SELECT title, text FROM notes WHERE (title LIKE ? OR text LIKE ?) AND tag = ?",
                        ("%" + search + "%", "%" + search + "%", tag),
                    ).fetchall()
                )
                > 0
            ):
                results = cur.execute(
                    "SELECT * FROM notes WHERE (title LIKE ? OR text LIKE ?) AND tag = ?",
                    ("%" + search + "%", "%" + search + "%", tag),
                ).fetchall()
            else:
                results = []
        else:
            if (
                len(
                    cur.execute(
                        "SELECT title, text FROM notes WHERE (title LIKE ? OR text LIKE ?) OR tag = ?",
                        ("%" + search + "%", "%" + search + "%", tag),
                    ).fetchall()
                )
                > 0
            ):
                results = cur.execute(
                    "SELECT * FROM notes WHERE (title LIKE ? OR text LIKE ?) OR tag = ?",
                    ("%" + search + "%", "%" + search + "%", tag),
                ).fetchall()
            else:
                results = []
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    con.commit()
    con.close()
    return results


def updatetag(id, tag):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    print("updating " + str(id))
    cur.execute("UPDATE notes SET tag = ? WHERE rowid = ?", (tag, id))
    con.commit()
    con.close()
