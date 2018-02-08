import pymysql
conn = pymysql.connect(host="localhost",port=3306,user='root',password='huang1989',db='xiaoshuo',charset='utf8')
print(conn)