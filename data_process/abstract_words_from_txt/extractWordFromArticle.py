import string
import sqlite3

filename = r"E:\work\pycode\util\text\data\Application_of_Artificial_Intelligence_Technology_.txt"
fout = open(r"out.txt", 'w')
conn = sqlite3.connect("mydict.db")
c = conn.cursor()

def extract_word_from_article(filename):
	fin = open(filename)
	words = []
	count = 0
	for line in fin:
		line = line.replace('-',' ')
		for word in line.split():
			word = word.strip(string.punctuation + string.whitespace)
			word = word.lower()
			if word not in words:
				words.append(word)
				sql = "select chinese from DICT WHERE english = \"{0}\"".format(word)
				cursor = c.execute(sql)
				ret = c.fetchone()
				if ret:
					ret=ret[0]
					count = count + 1
					print("%s : %s"%(word, ret))
					fout.write(word)
					# ret = ret.replace("\"", "\\*")
					fout.write("\n")
					fout.write("\t")
					fout.write(ret)
					fout.write("\n")
	fout.close()
	conn.close()
	print("total number: ", count)


extract_word_from_article(filename)
