
# -*- coding:utf-8  -*-

import mysql.connector

class DB:
	user=''
	password=''
	host=''
	dataBase=''
	query=''

	def __init__(self, path):
		ini=open(path, 'r')
		param=[]
		for str in ini:
			param.append(str[:-1])
		self.host=param[0]
		self.dataBase=param[1]
		self.user=param[2]
		self.password=param[3]

	def connect(self):
		try:
			self.connection=mysql.connector.connect(host=self.host, database=self.dataBase, user=self.user, password=self.password)
		except:
			print('Connection error')
#queryType=1 for SELECT, queryType=2 for INSERT/UPDATE
	def executeQuery(self, query, queryType):
		if(self.connection!=''):
			cursor=self.connection.cursor()
			if(queryType==1):
				cursor.execute(query)
				return cursor.fetchall()
			elif(queryType==2):
				try:
					cursor.execute(query)
					self.connection.commit()
					return 1
				except:
					print('Insert error, pass')
					return 0

	def closeConnection(self):
		self.connection.close()

