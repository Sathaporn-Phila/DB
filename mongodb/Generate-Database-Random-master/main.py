import pandas as pd
import os
import sqlite3
import pymongo
from random import randrange

from generate_db_sql import creator as creator_sql
from generate_db_mongo import creator as creator_mongo
from generate_db_mysql import creator as creator_mysql
class creator:
	#def __init__(self):
		#creator_sql.__init__(creator_sql)
		#creator_mongo.__init__(creator_mongo)
	
	def create_student(self, N, limit_size):
		print("********sql********")
		creator_sql.create_student(creator_sql, N, limit_size)
		
		print("********mongo********")
		creator_mongo.create_student(creator_mongo, N, limit_size)
	
	def create_subject(self):
		creator_sql.create_subject(creator_sql)
		creator_mongo.create_subject(creator_mongo)
	
	def create_grade(self, N, limit_size):
		print("********sql********")
		#creator_sql.create_grade(creator_sql, N, limit_size)
		
		print("********mongo********")
		#creator_mongo.create_grade(creator_mongo, N, limit_size)
		print("********mysql********")
		creator_grade = creator_mysql()
		creator_grade.create_grade(N, limit_size)
if __name__ == '__main__':
	obj = creator()
	#obj.create_subject()
	#obj.create_student(  1000000, 500*10**(6)  )
	obj.create_grade(  1000000, 8*10**(9)  )
	
