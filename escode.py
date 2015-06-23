# -*- coding: utf-8 -*-  
__metaclass__=type
from mysql import connector
import os

#GROUP=8
ROOT=u'源代码'
EXAM=u'比赛源代码'
EXERCISE=u'练习源代码'
HOSTREMOTE='222.204.211.2'
DBREMOTE='onlinejudge'
#CONTEST=20140520
HOSTLOCAL='127.0.0.1'
#DBLOCAL='dhuoj'
sqlExercise={
		'sqlUser':r"select t_user.loginId,t_user.name,t_user.class,t_user.id from t_user,t_group_user where t_user.id = t_group_user.user_id and t_group_user.group_id=%d;",
		'sqlContest':r"select t_contest.id,t_contest.title from t_contest,t_contest_group where t_contest.id=t_contest_group.contest_id and t_contest_group.group_id=%d;",
		'sqlCode':r'"select problem_id,id,code,language,result from t_contest_group,t_solution where  t_contest_group.group_id=%d and t_contest_group.contest_id=t_solution.contest_id and t_solution.user_id=%d and t_solution.contest_id=%d;" % (self.group,user[3],contest[0])',
		'sqlSequence':r'"select sequence from t_contest_problem where problem_id=%d and contest_id=%d" % (code[0],contest[0])'
		}
sqlExam={
		'sqlUser':r"select user.user_id,user.nick,user.school from user,contest_reservation where user.user_id = contest_reservation.user_id and contest_reservation.contest_id=%d;",
		'sqlContest':r"select contest.contest_id,contest.title from contest where contest.contest_id=%d;",
		'sqlCode':r'"select solution.problem_id,solution.solution_id,source_code.source,solution.language,solution.result from solution,source_code where solution.user_id=\'%s\' and solution.contest_id=%d and solution.solution_id=source_code.solution_id;" % (user[0],contest[0])',
		'sqlSequence':r'"select sequence from contest_problem where problem_id=%d and contest_id=%d" % (code[0],contest[0])'
		}

def creatConn(host,db):
	conn=connector.connect(host=host,user="root",passwd="root",db=db)
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
		0:'A+B',
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
		15:'O',
                16:'P',
                17:'Q',
                18:'R',
                19:'S',
                20:'T'
		}
LANGUAGEEXAM={
		0:'pas',
		1:'c',
		2:'cpp',
		3:'java',
		}
LANGUAGEEXERCISE={
		0:'cpp',
		1:'c',
		2:'java',
		}
class Escode:
	def __init__(self,sqls,isExam,contest=None,group=None):
		self.sqlUser=sqls['sqlUser']
		self.sqlContest=sqls['sqlContest']
		self.sqlCode=sqls['sqlCode']
		self.sqlSequence=sqls['sqlSequence']
		self.isExam=isExam
                self.contest = contest
                self.group = group
	def getUser(self,conn):
		cur = conn.cursor()
                if self.isExam:
                    self.sqlUser=self.sqlUser % self.contest
                else:
                    self.sqlUser=self.sqlUser % self.group
                print self.sqlUser
                cur.execute(self.sqlUser)

		result=cur.fetchall()
                print result
		return result


	def extract(self,users,conn):
		cur = conn.cursor()
		try:
			if self.isExam:
				os.mkdir(EXAM)
			else:
				os.mkdir(EXERCISE)
		except OSError:
			print "file exists!"
                if self.isExam:
                    self.sqlContest=self.sqlContest % self.contest
                else:
                    self.sqlContest=self.sqlContest % self.group
                print self.sqlContest
                cur.execute(self.sqlContest)
		contests=cur.fetchall()
		print contests,'aaaaaaaaaaaaaaaa'
		for contest in contests:
			contestFolder=os.path.join(EXAM if self.isExam else EXERCISE,contest[1])
			try:
				os.mkdir(contestFolder)
			except OSError:
				print "contest dir exists!"
			for user in users:
				folderName=user[0]+'_'+user[1]+'_'+user[2]
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
						ext = (LANGUAGEEXAM if self.isExam else LANGUAGEEXERCISE)[code[-2]]
						try:
							fileName=os.path.join(userFolder,user[0]+'_'+user[1]+'_'+TITLE[sequence[0][0]]+'_'+RESULT[code[-1]]+'_'+str(code[1])+'.'+ext)
						except:
							fileName=os.path.join(userFolder,user[0]+'_'+user[1]+'_'+TITLE[sequence[0][0]]+'_'+'WR'+'_'+str(code[1])+'.'+ext)
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
	conn=creatConn(HOSTREMOTE,DBREMOTE)
	es=Escode(sqlExercise)
	users=es.getUser(conn)
	print len(users)
	es.extract(users,conn)
	closeConn(conn)
	
