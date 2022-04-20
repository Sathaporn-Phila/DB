import mysql.connector
import random
import time

class creator:
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nuinee",
            auth_plugin='mysql_native_password'
        )
        self.cur = self.mydb.cursor()
        self.cur.execute(self.cur.execute("CREATE DATABASE IF NOT EXISTS grade"))
    def create_grade(self, N, limit_size):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nuinee",
            database="grade",
            auth_plugin='mysql_native_password'
        )

        i = 0
        self.cur = self.mydb.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Student (StudentID VARCHAR(255), SubjectID VARCHAR(255), Grade VARCHAR(255))")
        #self.cur.execute("CREATE INDEX id ON Student (StudentID)")
        self.mydb.commit()
        self.cur.execute("START TRANSACTION")
        size = self.getSize(self.cur)
        val_insert = []

        while(size<limit_size):
            StuID = "620" + str(random.randrange(1000000000,9999999999))
            SubID = random.choice(["010123102","010123103","010123105","010113010","010113011","040313005","040313007","040313008","040313006","080103001"])
            G = random.choice(["A","B+","B","C+","C","D+","D","F"])
            val_insert.append((StuID,SubID,G))
            if(len(val_insert)>=N):
                self.cur.executemany("INSERT INTO Student (StudentID, SubjectID, Grade) VALUES (%s,%s,%s)",val_insert)
                self.cur.execute("ANALYZE TABLE grade.student")
                val_insert = []
            i+=1
            all_table = self.cur.fetchall()
            if((i%N)==0):
                self.mydb.commit()
                size = self.getSize(self.cur)
                self.cur.execute("START TRANSACTION")
    def getSize(self,cursor):
        query = "SELECT  table_name AS `Table`, \
            round((data_length + index_length) \
            , 1) `Size in Byte` \
            FROM information_schema.TABLES \
            WHERE table_schema = 'grade' AND \
            table_name = 'Student';"
        cursor.execute(query)
        all_table = cursor.fetchall()
        for table in all_table:
            name_table = table[0]
            if(name_table == "student"):
                size = table[-1]
        print("Mysql size is {}".format(size))
        return size

obj = creator()
start = time.time()
obj.create_grade(  10**5, 8*10**(9)  )
end = time.time()
print("Tine is {}".format(end-start))