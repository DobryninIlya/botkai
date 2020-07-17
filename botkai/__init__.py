import .classes

cursorR = classes.cursorR
conn = classes.conn

cursorR.execute("""CREATE TABLE chatListen (id INT NOT NULL PRIMARY KEY, chatId INT NOT NULL); """)
cursorR.execute("""CREATE TABLE storage (id INT NOT NULL PRIMARY KEY, media_id INT NOT NULL); """)
cursorR.execute("""CREATE TABLE answers (id INT NOT NULL PRIMARY KEY, userId INT NOT NULL); """)
conn.commit()