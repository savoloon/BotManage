import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('reklama.db')
    cur = base.cursor()
    if base:
        print("Data base connect")
    # base.execute('DROP TABLE menu ')
    base.execute('CREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY AUTOINCREMENT, id_tg INT, channal TEXT, tarif TEXT, date TEXT, text TEXT, photo TEXT)')
    base.commit()


async def sql_add_command(id, chanall, tarif, date, text, photo):
    cur.execute('INSERT INTO menu(id_tg, channal, tarif,date,text, photo) VALUES(?,?,?,?,?,?)', (id, chanall, tarif, date, text, photo,))
    base.commit()


async def sql_date(chanall, message_text):
    cur.execute('SELECT COUNT(*) FROM menu WHERE channal = ? AND date = ?', (chanall, message_text,))
    result = cur.fetchone()[0]
    if result == 0:
        return 1
    else:
        return 0


async def sql_all():
    result1 = cur.execute("SELECT COUNT(*) FROM menu").fetchall()
    return result1


async def sql_read(score):
    ret = cur.execute(('SELECT * FROM menu ORDER BY id DESC LIMIT ? '),(score, )).fetchall()
    return ret


async def all_post(id_tg):
    cur.execute('SELECT channal, tarif, text, date, photo FROM oplach WHERE id_tg = ?', (id_tg, ))
    posts = cur.fetchall()
    return posts

async def count_user_post(id_tg):
    cur.execute('SELECT COUNT(*) FROM oplach WHERE id_tg = ?', (id_tg, ))
    count = cur.fetchall()
    return count

async def countotpr_user_post(id_tg):
    cur.execute('SELECT COUNT(*) FROM menu WHERE id_tg = ?', (id_tg, ))
    countotpr = cur.fetchall()
    return countotpr