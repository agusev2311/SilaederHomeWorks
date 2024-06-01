import sqlite3


a = input('all / число последних логов\n')

if a == 'all':
    conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
    cur = conn.cursor()

    cur.execute("SELECT * FROM logs")
    logs = cur.fetchall()

    counter = 1

    for i in logs:
        print(f'{counter}) {i[0]}\n')
        counter += 1

    cur.close()
    conn.close()
else:
    a = int(a)
    conn = sqlite3.connect('data.shw') # shw - SilHomeWorks
    cur = conn.cursor()

    cur.execute("SELECT * FROM logs")
    logs = cur.fetchall()

    counter = 1

    for i in logs:
        if counter >= len(logs) - a + 1:
            print(f'{counter}) {i[0]}\n')
        counter += 1

    cur.close()
    conn.close()
