import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('reklama.db')
    cur = base.cursor()
    if base:
        print("Data base connect")
    # base.execute('DROP TABLE chanall')
    base.execute('CREATE TABLE IF NOT EXISTS chanall(id INTEGER PRIMARY KEY AUTOINCREMENT, id_chanal,name_ch TEXT, tarif TEXT, price float)')
    base.commit()


async def add_ch(id_chanal, name, tarif, price):
    cur.execute('INSERT INTO chanall(id_chanal,name_ch,tarif,price) VALUES(?,?,?,?)', (id_chanal, name, tarif, price, ))
    base.commit()


def all_ch():
    all_ch = cur.execute("SELECT id,name_ch FROM chanall").fetchall()
    return all_ch


def delete_ch(channel_id):
    cur.execute('DELETE FROM chanall where id =?', (channel_id,))
    base.commit()


def chanall_slc():
    base = sq.connect('reklama.db')
    cur = base.cursor()
    slc = cur.execute("SELECT name_ch FROM chanall").fetchall()
    return slc


def tarif_slc(chanal):
    base = sq.connect('reklama.db')
    cur = base.cursor()
    slc = cur.execute("SELECT tarif FROM chanall where name_ch = ?", (chanal, )).fetchall()
    return slc


def price_slc(chanal, tarif):
    base = sq.connect('reklama.db')
    cur = base.cursor()
    cur.execute("SELECT price FROM chanall WHERE name_ch=?", (chanal,))
    row = cur.fetchone()
    price_info = row[0]  # Получаем строку с тарифами и ценами
    tariff_price_pairs = price_info.split('/')  # Разделяем на пары тариф-цена
    # Ищем цену для заданного тарифа
    for pair in tariff_price_pairs:
        tariff, price = pair.split('=')
        if tariff.strip() == tarif:
            return price.strip()


def id_ch(name_ch):
    channel_id = cur.execute("SELECT id_chanal FROM chanall where name_ch = ?", (name_ch,)).fetchone()
    return channel_id