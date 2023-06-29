import os
import sqlite3


raw_dict = r"raw-dict.txt"

conn = sqlite3.connect("mydict.db")
c = conn.cursor()
try:
    c.execute('''CREATE TABLE DICT
                (english TEXT PRIMARY KEY NOT NULL,
                chinese TEXT NOT NULL,
                level INT NOT NULL);''')
    conn.commit()
except:
    print("table exist")

fin = open(raw_dict,'r',encoding='utf-8')
for num, line in enumerate(fin):
    # line = line.replace("/", "//")
    # line = line.replace("'", "''")
    # line = line.replace("[", "/[")
    # line = line.replace("]", "/]")
    # line = line.replace("%", "/%")
    # line = line.replace("&","/&")
    # line = line.replace("_", "/_")
    # line = line.replace("(", "/(")
    # line = line.replace(")", "/)")
    line = line.replace("\"", "\\*")
    if num%2==0:
        english = line.replace("\n", "")
    else:
        chinese = line.replace("\n", "")
        cmd = "INSERT INTO DICT (english, chinese, level) VALUES (\"{0}\", \"{1}\", 1)".format(english, chinese)
        # print(cmd)
        c.execute(cmd)

conn.commit()
conn.close()