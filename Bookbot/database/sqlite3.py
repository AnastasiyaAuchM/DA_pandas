import sqlite3 as sq
from json import dumps

'''Create connect to SQLite for store users id, 
   current reading page and list with pages of bookmarks'''

global db, cur
db = sq.connect('bookbot_bd.db')
cur = db.cursor()

async def db_start():
	cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, page TEXT, bookmarks ARRAY)")
	db.commit()
	
async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?)", (user_id, '', ''))
        db.commit()

async def edit_page(page, user_id):
	cur.execute("UPDATE profile SET page = ? WHERE user_id = ?", (page, user_id, ))
	db.commit()
	
async def edit_bookmarks(bookmark, user_id):
	marks_jsonarray = dumps(list(bookmark))
	cur.execute("UPDATE profile SET bookmarks = ? WHERE user_id = ?", (marks_jsonarray, user_id, ))
	db.commit()
