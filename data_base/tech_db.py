import sqlite3 as sq



def sql_start():
    global base, cur
    base = sq.connect('reklama.db')
    cur = base.cursor()
    if base:
        print("Data base connect")
    # base.execute('DROP TABLE tech')
    base.execute('CREATE TABLE IF NOT EXISTS tech(id INTEGER PRIMARY KEY AUTOINCREMENT, id_tech INT,text_tech TEXT, answer TEXT, date_tech TEXT)')
    base.commit()


async def sql_add_tech(id, text, date):
    cur.execute('INSERT INTO tech(id_tech,text_tech, date_tech) VALUES(?,?,?)', (id, text,date,))
    base.commit()


async def sql_add_answer(id, answer):
    cur.execute('UPDATE tech SET answer = ? WHERE id = ?', (answer, id))
    base.commit()


async def sql_all():
    result1 = cur.execute("SELECT COUNT(*) FROM tech").fetchall()
    return result1


async def sql_read(score):
    ret = cur.execute(('SELECT * FROM tech ORDER BY id DESC LIMIT ? '),(score, )).fetchall()
    return ret


async def sql_old(id):
    ret = cur.execute(('SELECT text_tech,answer,date_tech FROM tech where id_tech = ?'),(id, )).fetchall()
    return ret