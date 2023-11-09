import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('reklama.db')
    cur = base.cursor()
    if base:
        print("Data base connect")
    # base.execute('DROP TABLE date_check')
    base.execute('CREATE TABLE IF NOT EXISTS date_check(id INTEGER PRIMARY KEY AUTOINCREMENT, channal TEXT, date TEXT)')
    base.commit()


async def sql_add_command(chanall, date):
    cur.execute('INSERT INTO date_check(channal, date) VALUES(?,?)', (chanall, date, ))
    base.commit()


async def sql_date(chanall, message_text):
    cur.execute('SELECT COUNT(*) FROM date_check WHERE channal = ? AND date = ?', (chanall, message_text,))
    result = cur.fetchone()[0]
    if result == 0:
        return 1
    else:
        return 0
