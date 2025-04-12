import sqlite3


db = sqlite3.connect("databases/db.sqlite")


def sql_request(request):
    cur = db.cursor()
    result = cur.execute(request).fetchall()
    return result


def sql_changes(request):
    cur = db.cursor()
    cur.execute(request)
    db.commit()


def get_clients():
    cur = db.cursor()
    result = cur.execute(
        """SELECT group_id, channel_id
            FROM Clients"""
    ).fetchall()
    return result


def add_client(group_id: int, channel_id: int):
    cur = db.cursor()
    cur.execute(
        f"""INSERT INTO Clients(group_id, channel_id)
                VALUES({group_id}, {channel_id})""",
    )
    db.commit()
