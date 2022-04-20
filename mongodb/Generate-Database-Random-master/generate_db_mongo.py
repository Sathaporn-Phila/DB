import pandas as pd
import os
import pymongo
import math
from random import randrange
name = pd.read_csv("name.csv")
grade_arr = ["A","B+","B","C+","C","D+","D","F"] # init variable

class creator:
	def __init__(self):
		myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = myclient["mydatabase"]
		self.my_Student = self.mydb["Student"]
		self.my_Subject = self.mydb["Subject"]
		self.my_Grade = self.mydb["Grade"]
	
	def create_student(self, N, limit_size):
		size = 0
		count = 0
		name = pd.read_csv("name.csv")["FirstForename"].tolist()
		
		print("first....",)
		print( int(self.mydb.command("dbstats")["storageSize"]) )
		######################################################################
		while(size < limit_size):
			stu_id = []
			stu_name = []
			for i in range(N):
				sid = "6201"+ str(randrange(100000000,999999999))
				stu_id.append(sid)
				stu_name.append(  name[randrange(0,len(name))]  )
			df = pd.DataFrame({'StudentID': stu_id,
									 'StudentName': stu_name})
			os.makedirs('creation', exist_ok=True)
			self.my_Student.insert_many(df.to_dict('records'))
			
			size = int(self.mydb.command("dbstats")["storageSize"])
			print(size)
		######################################################################
		print(int(self.mydb.command("dbstats")["storageSize"]))
	
	def create_subject(self):
		df = pd.read_csv("Subject.csv")
		self.my_Subject.insert_many(  df.to_dict('records')  )
	
	def create_grade(self, N, limit_size):
		size = 0
		count = 0
		
		stu = list(  self.my_Student.find({},{ "_id":0})  )
		sub = list(  self.my_Subject.find({},{ "_id":0, "Credit": 0})  )
		
		print("Creating grade....")
		print( int(self.mydb.command("dbstats")["storageSize"]) )
		
		######################################################################
		while(size < limit_size):
			arr_myquery = []
			sqrt_N = int(math.sqrt(N))
			for i in range(sqrt_N):
				semester = []
				for i in range(sqrt_N):
					sub_t = sub[randrange(0,len(sub))]
					semester_query = {"Term":randrange(1,6),  "SubjectName":sub_t["SubjectName"], "SubjectID":sub_t["SubjectID"], "Grade":grade_arr[randrange(0,len(grade_arr))]}
					semester.append(semester_query)
				myquery = {"StudentID":[{"ID": stu[randrange(0,len(stu))]["StudentID"] ,"Grade":[{"Semester":semester}]}]}
				arr_myquery.append(myquery)
			os.makedirs('creation', exist_ok=True) 
			self.my_Grade.insert_many(arr_myquery)
			
			size = int(self.mydb.command("dbstats")["storageSize"])
			print(size)
		print("Size of Mongodb database is",size,"bytes")
		######################################################################
		
if __name__ == '__main__':
	obj = creator()
	obj.create_subject()
	obj.create_student(  1000000, 100*10**(6)  )
	obj.create_grade(  1000000, 200*10**(6)  )
