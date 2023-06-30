import sqlite3 as sq

def add_sport(arr):
        with sq.connect('protocolbd.bd') as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS sport_protocol (
                нагрудный_номер INTEGER PRIMARY KEY UNIQUE NOT NULL,
                ФИО TEXT NOT NULL,
                пол TEXT NOT NULL,
                возраст INTEGER NOT NULL,
                вид TEXT NOT NULL,
                результат REAL NOT NULL
                )""")
            
            try:
                cur.execute("""INSERT INTO sport_protocol VALUES(?, ?, ?, ?, ?, ?)""",  
                        (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]))
                cur.close()
                return '✅ Участник добавлен!'
            except:
                 cur.close()
                 return '🚫 Участник с таким номером уже существует!'
            
def del_sport(number):
    with sq.connect('protocolbd.bd') as con:        
        cur = con.cursor()

        cur.execute("SELECT * FROM sport_protocol WHERE нагрудный_номер = ?", (number,))        
        res = cur.fetchone()

        if res:
            cur.execute("""DELETE FROM sport_protocol WHERE нагрудный_номер = ?""", (number,))
            return f'✅ Спортсмен с номером {number} успешно удалён!'
        else:
             cur.close()
             return f'🚫 Что-то пошло не так! Возможно введён неверный номер!'
        
def del_all():
    with sq.connect('protocolbd.bd') as con:        
        cur = con.cursor()
        
        cur.execute("""DELETE FROM sport_protocol""")

def send():
    with sq.connect('protocolbd.bd') as con:        
        cur = con.cursor()

    cur.execute("SELECT * FROM sport_protocol")
    f = cur.fetchall()
    return f