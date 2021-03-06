# -*- coding: utf-8 -*-
#whitefirer@gmail.com
#copyright@2015
import random
import copy
import time

CAT_MAPTYPE = 8
WALL_MAPTYPE = 1
NOWALL_MAPTYPE = 0

class CostType:
	def __init__(self, cost, ways):
		self.cost = cost
		self.ways = ways

class CatGame:
	def __init__(self):
		self.col = 9
		self.row = 9
		self.quickmodlist = [1,3, 5, 7]#取模列表
		self.catpos = (4,4)
		self.oldpos = (4, 4)
		self.noway = 0
		self.failed = False
		self.wined = False
		self.result = ''
		self.map = [[0 for col in range(self.col)] for row in range(self.row)]
		#方向定义
		self.dirs = [[0,-1,'U'],[1,0,'R'],[0,1,'D'],[-1,0,'L']]
		self.dirs1 = [[-1,-1,'Q'],[0,-1,'U'],[1,0,'R'],[0,1,'D'],[-1,1,'Z'],[-1,0,'L']]
		self.dirs2 = [[0,-1,'U'],[1,-1,'E'],[1,0,'R'],[1,1,'V'],[0,1,'D'],[-1,0,'L']]#%2=0
		self.dirsmap = {
			'L' : (-1, 0),#左
			'Q' : (-1, -1),#左上
			'U' : (0, -1),#上
			'E' : (1, -1),#右上
			'R' : (1, 0),#右
			'V' : (1, 1),#右下
			'D' : (0, 1),#下
			'Z' : (-1, 1)#左下
		}
		
	
	def InitGame(self):
		self.InitMap()
		self.SetCatPos(4,4)
		self.oldpos = (4, 4)
		self.noway = 0
		self.failed = False
		self.wined = False
		self.result = ''
		self.map[self.catpos[1]][self.catpos[0]] = CAT_MAPTYPE
	
	def InitMap(self):
		self.map = [[0 for col in range(self.col)] for row in range(self.row)]
		
	def SetCatPos(self, col, row):
		if col < 0 or row < 0 or col >= self.col or row >= self.row:
			self.failed = True
			return
		if col in [0, self.col-1] or row in [0, self.row-1]:
			self.failed = True
		self.oldpos = (self.catpos[0], self.catpos[1])
		self.map[self.catpos[1]][self.catpos[0]] = NOWALL_MAPTYPE
		self.catpos = (col,row)
		self.map[self.catpos[1]][self.catpos[0]] = CAT_MAPTYPE
	
	def SetWall(self, col, row):
		self.map[row][col] = WALL_MAPTYPE
		
	def IsWall(self, col, row):
		return (self.map[row][col] == WALL_MAPTYPE)
				
	def IsFail(self):
		return self.failed
	
	def IsWin(self):
		if self.GetWays(self.catpos[0], self.catpos[1]) == 0:
			return self.wined
		return False	
		
	def IsFree(self, col, row):
		return (self.map[row][col] in [0, 8])
			
	def GetWays(self, col, row):
		if col in [0, self.col-1] or row in [0, self.row-1]:
			return -1
		ways = 0
		dirs = self.dirs1
		if row in self.quickmodlist:
			dirs = self.dirs2
		for d in dirs: #检查六个方向
			if self.IsFree(col+d[0], row+d[1]):
				ways += 1
			
		return ways
	
	def shuffle(self, dataList):
		l = len(dataList)
		for i in xrange(l):
			j = random.randint(i,l-1)
			dataList[j],dataList[i] = dataList[i],dataList[j]
			
	def GetRandomWays(self, col, row):
		if col in [0, self.col-1] or row in [0, self.row-1]:
			return col, row
		dirs = self.dirs1
		if row in self.quickmodlist:
			dirs = self.dirs2
		randomlist = []
		
		ways = 0
		for d in dirs: #检查六个方向
			if self.IsFree(col+d[0], row+d[1]):
				#tempway = self.GetWays(col+d[0], row+d[1])
				#if tempway > ways:
				#	ways = tempway
				#	randomlist = [(col+d[0], row+d[1])]
				#elif tempway == ways:
					randomlist.append((col+d[0], row+d[1]))

		self.shuffle(randomlist)
		if len(randomlist):
			if len(randomlist) > 1 and (self.oldpos[0], self.oldpos[1]) in randomlist:
				randomlist.remove((self.oldpos[0], self.oldpos[1]))
			return randomlist[0][0],  randomlist[0][1]
			
		return -2,-2
		
	#迷宫算法
	def GetPath(self, data, startx, starty, endx, endy): #单终点
		self.result='' #结果存放处
		
		def move(path,x,y,field): #移动函数
			field[y][x] = len(path) + 1 #把自己变成1, 防止无限递归
			pathlen = len(path)
			resultlen = len(self.result)
			if pathlen >= resultlen and resultlen != 0:
				return
			if x in [0, 8] or y in [0, 8]: #如果到终点了
				if len(self.result) > len(path) or len(self.result) == 0:
					self.result = path#将路径放入结果
					return
			dirs = self.dirs1
			if y in self.quickmodlist:
				dirs = self.dirs2
			for d in dirs: #检查六个方向
				if y+d[1] in range(0, 9) and x+d[0] in range(0, 9):
					if field[y+d[1]][x+d[0]] > len(path)+1 or field[y+d[1]][x+d[0]] == 0: #如果某个方向为0
						move(path+d[2],x+d[0],y+d[1],field) #递归
		move('',startx,startx,data) #调用移动函数, 此时路径为空
		
		return self.result #将结果路径返回 
		
	def GetBestPath(self):#另一种方式，每个边界点定点取路，实际效果跟直接用边界点集做结束条件一样,当然更费时，所以不用
		path = ''
		for row in range(0, 9):
			for col in [0, 8]:
				data = copy.deepcopy(self.map)
				if self.map[row][col] == 0:
					temppath = self.GetPath(data, self.catpos[0], self.catpos[1], col, row)
					if len(temppath) < len(path) or len(path) == 0:
						path = temppath
		dirs = self.dirs1			
		for col in range(1, 8):
			for row in [0, 8]:
				data = copy.deepcopy(self.map)
				if self.map[row][col] == 0:
					temppath = self.GetPath(data, self.catpos[0], self.catpos[1], col, row)
					if len(temppath) < len(path) or len(path) == 0:
						path = temppath
			
		return path	
		
	#迷宫算法
	def GetCatPath(self): #主函数
		data = copy.deepcopy(self.map)
		#data = self.map
		self.result='' #结果存放处
		#方向定义
		#dirs = [[-1,0,'L'],[0,-1,'U'],[1,0,'R'],[0,1,'D']]
		#dirs2 = [[-1,0,'L'],[0,-1,'U'],[1,-1,'E'],[1,0,'R'],[1,1,'V'],[0,1,'D']]#%2=0
		#dirs1 = [[-1,0,'L'],[-1,-1,'Q'],[0,-1,'U'],[1,0,'R'],[0,1,'D'],[-1,1,'Z']]
		def move(path,x,y,field): #移动函数
			pathlen = len(path)
			resultlen = len(self.result)
			if pathlen >= resultlen and resultlen != 0:#这个条件很重要，当此时查找的路线已经比之前的长时就没必要查找了
				return
			field[y][x] = pathlen + 1 #把自己变成1, 防止无限递归
			if x in [0, 8] or y in [0, 8]: #如果到终点了
				if resultlen > pathlen or resultlen == 0:
					self.result = path#将路径放入结果
					return
			dirs = self.dirs1
			if y in self.quickmodlist:#发现比取模快上那么点
				dirs = self.dirs2
			for d in dirs: #检查六个方向
				if y+d[1] in range(0, 9) and x+d[0] in range(0, 9):
					if field[y+d[1]][x+d[0]] > pathlen+1 or field[y+d[1]][x+d[0]] == 0: #如果某个方向为0
						move(path+d[2],x+d[0],y+d[1],field) #递归
		move('',self.catpos[0],self.catpos[1],data) #调用移动函数, 此时路径为空
		self.waysmap = data
		#self.PrintMap()
		#print ''
		#self.PrintWaysMap()
		return self.result #将结果路径返回 
		
		
	def GetNextPos(self):
		if self.catpos[0] in [0, self.col-1] or self.catpos[1] in [0, self.row-1]:
			self.failed = True
			return -1, -1
		path = self.GetCatPath()
		if path == '':
			self.wined = True
			return self.GetRandomWays(self.catpos[0], self.catpos[1])
		else:
			dpos = self.dirsmap.get(path[0],(0,0))
			return self.catpos[0]+dpos[0], self.catpos[1]+dpos[1]
			
	def PrintMap(self):
		idx = 0
		for i in self.map:
			if idx in self.quickmodlist:
				print ' ' + str(i)
			else:
				print i
			idx += 1
		print self.result	
		print ''
	
	def TestGame(self):
		self.InitGame()
		
		#print self.GetBestPath()
		'''
		self.SetWall(7,7)
		self.SetWall(1,4)
		self.SetWall(2,4)
		self.SetWall(5,6)
		self.SetWall(4,6)
		self.SetWall(3,3)
		'''
		self.SetWall(3,4)
		self.SetWall(3,5)
		self.SetWall(3,6)
		self.SetWall(4,3)
		self.SetWall(5,3)
		self.SetWall(5,5)
		self.SetWall(5,4)
		self.SetWall(4,5)
		
		self.SetWall(2,0)
		self.SetWall(2,2)
		self.SetWall(2,3)
		self.SetWall(2,4)
		self.SetWall(2,5)
		self.SetWall(2,6)
		self.SetWall(2,7)
		self.SetWall(2,8)
		path = ''
		
		
		while True:
			self.PrintMap()
			col = random.randint(0,self.col-1)
			row = random.randint(0,self.row-1)
			
			s = raw_input('>>>')
			if s!= '':
				lst = s.split(' ')
				if 'exec' == lst[0]:
					exec(lst[1])
					continue
				else:
					col = int(lst[0])
					row = int(lst[1])
			
			if self.map[row][col] == 0:
				self.SetWall(col, row)
			t = time.time()
			x,y = self.GetNextPos()
			dt = time.time() - t
			print dt
			if x in [0,8] or y in [0,8]:
				self.PrintMap()
				print 'badend'
				raw_input('>>>')
				self.InitGame()
			else:
				if x >= 0 and y >= 0:
					self.SetCatPos(x, y)
				if self.IsWin():
					self.PrintMap()
					print 'welldone'
					raw_input('>>>')
					self.InitGame()
		
		
		
Test = CatGame()

Test.TestGame()
	