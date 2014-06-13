# -*- coding: utf-8 -*-  
__metaclass__=type
from mysql import connector
import os

GROUP=8
ROOT=u'练习源代码'
HOST='222.204.211.2'
DB='onlinejudge'

def creatConn():
	conn=connector.connect(host=HOST,user="root",passwd="root",db=DB)
	return conn

def closeConn(conn):
	conn.close()

RESULT={
		1:'QUEUE',
		2:'AC',
		3:'WA',
		4:'TLE',
		5:'MLE',
		6:'PE',
		7:'RE',
		8:'CE'
		}
TITLE={
		1:'A',
		2:'B',
		3:'C',
		4:'D',
		5:'E',
		6:'F',
		7:'G',
		8:'H',
		9:'I',
		10:'J',
		11:'K',
		12:'L',
		13:'M',
		14:'N',
		15:'O'
		}
class Escode:
	def __init__(self,sqls):
		self.sqlUser=sqls['sqlUser']
		self.sqlContest=sqls['sqlContest']
		self.sqlCode=sqls['sqlCode']
		self.sqlSequence=sqls['sqlSequence']
	def getUser(self,conn):
		cur = conn.cursor()
		cur.execute(eval(self.sqlUser))
		result=cur.fetchall()
		return result


	def extract(self,users,conn):
		cur = conn.cursor()
		try:
			os.mkdir(ROOT)
		except OSError:
			print "file exists!"
		cur.execute(eval(self.sqlContest))
		contests=cur.fetchall()
		for contest in contests:
			contestFolder=os.path.join(ROOT,contest[1])
			try:
				os.mkdir(contestFolder)
			except OSError:
				print "contest dir exists!"
			for user in users:
				folderName=user[3]+'_'+user[4]+'_'+user[1]
				print folderName
				userFolder=os.path.join(contestFolder,folderName)
				try:
					os.mkdir(userFolder)
				except OSError:
					print "file exists!"

				cur.execute(eval(self.sqlCode))
				codes=cur.fetchall()
				for code in codes:
					try:
						#print code[0],contest[0],"111111111111"
						cur.execute(eval(self.sqlSequence))
						sequence=cur.fetchall()
						#print sequence,type(sequence),sequence[0][0],code[-1]
						try:
							fileName=os.path.join(userFolder,TITLE[sequence[0][0]]+'_'+RESULT[code[-1]]+'.cpp')
						except:
							fileName=os.path.join(userFolder,TITLE[sequence[0][0]]+'_'+"WR"+'.cpp')
						f=file(fileName,'w')
						try:
							f.write(code[2].encode('gbk'))
						except UnicodeEncodeError:
							print type(code[2])
							print "encode error",fileName
						f.close()
					except IndexError:
						if sequence:
							print "stop!"
							return
	
	


if __name__=='__main__':
	conn=creatConn()
	sqlExercise={
			'sqlUser':r'"select * from t_user,t_group_user where t_user.id = t_group_user.user_id and t_group_user.group_id=%d;" % GROUP',
			'sqlContest':r'"select t_contest.id,t_contest.title from t_contest,t_contest_group where t_contest.id=t_contest_group.contest_id and t_contest_group.group_id=%d;" % GROUP',
			'sqlCode':r'"select problem_id,id,code,result from t_contest_group,t_solution where  t_contest_group.group_id=%d and t_contest_group.contest_id=t_solution.contest_id and t_solution.user_id=%d and t_solution.contest_id=%d;" % (GROUP,user[0],contest[0])',
			'sqlSequence':r'"select sequence from t_contest_problem where problem_id=%d and contest_id=%d" % (code[0],contest[0])'
			}
	es=Escode(sqlExercise)
	users=es.getUser(conn)
	print len(users)
	es.extract(users,conn)
	closeConn(conn)
	
