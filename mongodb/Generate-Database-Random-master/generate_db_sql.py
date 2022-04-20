import pandas as pd
import os
import sqlite3
from random import randrange
name = pd.read_csv("name.csv")
grade_arr = ["A","B+","B","C+","C","D+","D","F"] # init variable

class creator:
	def __init__(self):
		self.conn = sqlite3.connect('creation/test_database')
		self.sql= self.conn.cursor()
	
	def create_student(self, N, limit_size):
		size = 0
		count = 0
		name = pd.read_csv("name.csv")["FirstForename"].tolist()
		
		self.sql.execute('CREATE TABLE IF NOT EXISTS Student (StudentID text, StudentName text)')
		self.conn.commit()
		
		print("first....",)
		print(os.path.getsize('creation/test_database'))
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
			
			if(count == 0):
				df.to_sql('Student', self.conn, index=False, if_exists='replace')
				count = 1
			else:
				df.to_sql('Student', self.conn, index=False, if_exists='append')
			size = os.path.getsize('creation/test_database')
			print(size)
		######################################################################
		print(os.path.getsize('creation/test_database'))
	
	def create_subject(self):
		pd.read_csv("Subject.csv").to_sql('Subject', self.conn, index=False, if_exists='replace')
	
	def create_grade(self, N, limit_size):
		size = 0
		count = 0
		stu_id = pd.read_sql('SELECT Student.StudentID FROM Student', self.conn)["StudentID"].values.tolist()
		sub_id = pd.read_sql('SELECT Subject.SubjectID FROM Subject', self.conn)["SubjectID"].values.tolist()
		
		self.sql.execute('CREATE TABLE IF NOT EXISTS Grade (StudentID text, SubjectID text, Grade text, Semester number)')
		self.conn.commit()
		
		print("second....")
		print(os.path.getsize('creation/test_database'))
		######################################################################
		while(size < limit_size):
			student = []
			subject = []
			grade = []
			semester = []
			for i in range(N):
				student.append(  stu_id[randrange(0,len(stu_id))]  )
				subject.append(  sub_id[randrange(0,len(sub_id))]  )
				grade.append(  grade_arr[randrange(0,len(grade_arr))]  )
				semester.append(  randrange(1,6)  )
			df = pd.DataFrame({'StudentID': student,
									 'SubjectID': subject,
									 'Grade ': grade,
									 'Semester': semester})
			os.makedirs('creation', exist_ok=True) 
			
			if(count == 0):
				df.to_sql('Enrolls', self.conn, index=False, if_exists='replace')
				count = 1
			else:
				df.to_sql('Enrolls', self.conn, index=False, if_exists='append')
			size = os.path.getsize('creation/test_database')
			print(size)
		print("Size of Sqlite3 database is",size,"bytes")
		######################################################################
		
if __name__ == '__main__':
	obj = creator()
	obj.create_subject()
	obj.create_student(  1000000, 100*10**(6)  )
	obj.create_grade(  1000000, 200*10**(6)  )
