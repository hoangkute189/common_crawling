import sqlite3

conn = sqlite3.connect('common_crawl.db')

c = conn.cursor()

# c.execute("""
#         INSERT INTO common_crawl (id, url, title, content) VALUES (?, ?, ?, ?)
#         """, ('1', 'link', 'title', 'content'))

# conn.commit()

c.execute("""SELECT * FROM common_crawl""")

print(c.fetchall())

conn.commit()

conn.close()