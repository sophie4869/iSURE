import os
import mysql.connector
import sys

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': '8889',
  'database': 'sensorData'
}
cnx = mysql.connector.connect(**config)#???

class ReadFile:
    def readLines(self):
        f = open("/Users/sophie/_current/0811_sitting_gyroscope.csv", "r", 1) # data file path
        i=0
        for line in f:
            list=[]
            strs = line.split(",")
            if len(strs) != 8:
                continue
            data=(strs[1], strs[2], strs[3], strs[4], strs[5].replace("\n",""))
            list.append(data)
            print list
            cursor=cnx.cursor()
            sql = "insert into sensor0(type,x,y,z,time)values(%s,%s,%s,%s,%s)" # insert into database
            cursor.executemany(sql,list)
            cnx.commit()
            i=i+1
            print("inserted")
        cnx.close()
        f.close()
        print("done")
        
             
if __name__ == "__main__":
    readFile = ReadFile()  
    readFile.readLines()

