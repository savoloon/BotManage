import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('reklama.db')
    cur = base.cursor()
    if base:
        print("Data base connect")
    # base.execute('DROP TABLE oplach')
    base.execute('CREATE TABLE IF NOT EXISTS oplach(id INTEGER PRIMARY KEY AUTOINCREMENT, id_tg INT, channal TEXT, tarif TEXT, date TEXT, text TEXT, photo TEXT)')
    base.commit()


async def sql_add_command(id, chanall, tarif, date, text, photo):
    cur.execute('INSERT INTO oplach(id_tg, channal, tarif,date,text, photo) VALUES(?,?,?,?,?,?)', (id, chanall, tarif, date, text, photo))
    base.commit()


def all_opl():
    records = cur.execute("SELECT id, channal, date, text, photo, tarif FROM oplach").fetchall()
    return records

