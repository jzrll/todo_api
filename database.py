import sqlite3


def setup_db():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    count = cur.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    if count == 0:
        cur.execute("""
            INSERT INTO tasks VALUES
                (1, 'task 1', FALSE),
                (2, 'task 2', FALSE),
                (3, 'task 3', FALSE)
        """)

    con.commit()
    con.close()
    