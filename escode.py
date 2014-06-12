# -*- coding: utf-8 -*-  
from mysql import connector
import os

GROUP=8
ROOT=u'练习源代码'
HOST='222.204.211.2'
DB='onlinejudge'


def creatConn():
	conn=connector.connect(host=HOST,user="root",passwd="root",db=DB)
	return conn

def getUser(conn):
	cur = conn.cursor()
	sql="select * from t_user,t_group_user where t_user.id = t_group_user.user_id and t_group_user.group_id=%d;" % GROUP 
	cur.execute(sql)
	result=cur.fetchall()
	return result

def closeConn(conn):
	conn.close()

def extract(users,conn):
	cur = conn.cursor()
	try:
		os.mkdir(ROOT)
	except OSError:
		print "file exists!"
	for user in users:
		folderName=user[3]+user[4]
		print folderName
		try:
			os.mkdir(os.path.join(ROOT,folderName))
		except OSError:
			print "file exists!"

		sql="select problem_id,id,code from t_contest_group,t_solution where  t_contest_group.group_id=%d and t_contest_group.contest_id=t_solution.contest_id and t_solution.user_id=%d;" % (GROUP,user[0])
		cur.execute(sql)
		codes=cur.fetchall()
		for code in codes:
			fileName=os.path.join(ROOT,folderName,str(code[0])+'_'+str(code[1])+'.txt')
			f=file(fileName,'w')
			try:
				f.write(code[2].encode('gbk'))
			except UnicodeEncodeError:
				print type(code[2])
				print "encode error",fileName
			f.close()
	
	


if __name__=='__main__':
	conn=creatConn()
	users=getUser(conn)
	print len(users)
	extract(users,conn)
	closeConn(conn)
	
