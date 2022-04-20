import time
import sqlite3
import pymongo
conn = sqlite3.connect('creation/test_database')
cursor = conn.cursor()
start1 = time.time()

cursor.execute("SELECT * FROM Enrolls WHERE SubjectID = 80203901")
rows = cursor.fetchall()
end1 = time.time()


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
grade = mydb["Grade"]

start = time.time()
query = grade.find({})
for i in query:
	print(query)
end = time.time()


print("Sqlite use time {}".format(end1-start1))
print("MongoDB use time {}".format(end-start))