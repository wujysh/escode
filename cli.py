#!/usr/bin/python
# -*- coding: utf-8 -*-  
import optparse
import escode

def main():
	p=optparse.OptionParser(description="Use for extract source code from DHU acm judge program.",
			prog="escode",
			version='0.0.1',
			usage="""
	python cli.py --host="127.0.0.1" -d dhuoj -c 20140520
	python cli.py --host="222.204.211.2" -d onlinejudge -g 8
					""")
	p.add_option('--host')
	p.add_option('-d','--db')
	p.add_option('-g','--group',type='int')
	p.add_option('-c','--contest',type='int')
	options,arguments=p.parse_args()
	#print options,arguments
	if not arguments:
		print "Need some parm,please!"
		return 
	conn=escode.creatConn(options.host,options.db)

	if options.group:
		GROUP=options.group
		es=escode.Escode(escode.sqlExercise,False)
		users=es.getUser(conn)
		es.extract(users,conn)
	elif options.contest:
		CONTEST=options.contest
		es=escode.Escode(escode.sqlExam,True)
		users=es.getUser(conn)
		es.extract(users,conn)



if __name__=='__main__':
	main()
