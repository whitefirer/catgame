# -*- coding: utf8 -*-
#whitefirer@gmail.com
#copyright@2015
import random

CAT_COSTTYPE = 888
CAT_MAPTYPE = 8
WALL_COSTTYPE = 100
WALL_MAPTYPE = 1
NOWALL_COSTTYPE = 0
NOWALL_MAPTYPE = 0

class CostType:
	def __init__(self, cost, ways):
		self.cost = cost
		self.ways = ways

class CatGame:
	def __init__(self):
		self.col = 9
		self.row = 9
		self.catpos = (4,4)
		self.noway = 0
		self.map = [[0 for col in range(self.col)] for row in range(self.row)]
		self.costmap = [[CostType(0,0) for col in range(self.col)] for row in range(self.row)]
	
	def InitGame(self):
		self.InitMap()
		self.InitCostMap()
		self.SetCatPos(4,4)
		self.noway = 0
		self.map[self.catpos[1]][self.catpos[0]] = CAT_MAPTYPE
		self.UpdataCostMap()
	
	def InitMap(self):
		self.map = [[0 for col in range(self.col)] for row in range(self.row)]
		
	def InitCostMap(self):
		self.costmap = [[CostType(0,0) for col in range(self.col)] for row in range(self.row)]
		for row,line in enumerate(self.map):
			for col, data in enumerate(line):
				if data == 1:
					self.costmap[row][col].cost = WALL_COSTTYPE
				elif data == 8:
					self.costmap[row][col].cost = CAT_COSTTYPE
				else:
					self.costmap[row][col].cost = NOWALL_COSTTYPE
		
	def SetCatPos(self, col, row):
		self.map[self.catpos[1]][self.catpos[0]] = NOWALL_MAPTYPE
		self.catpos = (col,row)
		self.map[self.catpos[1]][self.catpos[0]] = CAT_MAPTYPE
		self.UpdataCostMap()
	
	def SetWall(self, col, row):
		self.map[row][col] = WALL_MAPTYPE
		self.costmap[row][col].cost = WALL_COSTTYPE
		self.UpdataCostMap()
		
	def GetNextPos(self):
		col = self.catpos[0]
		row =  self.catpos[1]
		ways = self.costmap[row][col].ways
		bestpos = -2,-2
		bestcost = 100
		if self.catpos[0] in [0, self.col-1] or self.catpos[1] in [0, self.row-1]:
			return -1,-1#代表输了
		
		if row%2 == 0:#奇数行
			cost = self.costmap[row-1][col-1].cost#左上
			if bestcost > cost:
				bestpos = col-1,row-1
				bestcost = cost
			elif bestcost == cost:
				if self.costmap[row-1][col-1].ways > ways:
					bestpos = col-1,row-1
		
		cost = self.costmap[row-1][col].cost#上
		if bestcost > cost:
			bestpos = col,row-1
			bestcost = cost
		elif bestcost == cost:
			if self.costmap[row-1][col].ways > ways:
				bestpos = col,row-1
			
		if row%2:
			cost = self.costmap[row-1][col+1].cost#右上
			if bestcost > cost:
				bestpos = col+1,row-1
				bestcost = cost
			elif bestcost == cost:
				if self.costmap[row-1][col+1].ways > ways:
					bestpos = col+1,row-1
				
		cost = self.costmap[row][col+1].cost#右
		if bestcost > cost:
			bestpos = col+1,row
			bestcost = cost
		elif bestcost == cost:
			if self.costmap[row][col+1].ways > ways:
				bestpos = col+1,row
			
		if row%2:#奇数行
			cost = self.costmap[row+1][col+1].cost#右下
			if bestcost > cost:
				bestpos = col+1,row+1
				bestcost = cost
			elif bestcost == cost:
				if self.costmap[row+1][col+1].ways > ways:
					bestpos = col+1,row+1
		
		cost = self.costmap[row+1][col].cost#下
		if bestcost > cost:
			bestpos = col,row+1
		elif bestcost == cost:
			if self.costmap[row+1][col].ways > ways:
				bestpos = col,row+1
				bestcost = cost
			
		if row%2 == 0:
			cost = self.costmap[row+1][col-1].cost#左下
			if bestcost > cost:
				bestpos = col-1,row+1
				bestcost = cost
			elif bestcost == cost:
				if self.costmap[row+1][col-1].ways > ways:
					bestpos = col-1,row+1
					
		print bestpos,self.costmap[bestpos[0]][bestpos[1]].ways		
		return bestpos
				
		
	def IsValid(self, col, row):
		if self.map[row][col] == 0 and self.costmap[row][col].cost < WALL_COSTTYPE:
			return True
		return False
		
	def IsFree(self, col, row):
		if self.map[row][col] in [0, 8]:
			return True
		return False
		
	def GetCost(self, col, row):
		cost = 0
		min = 99
		self.costmap[row][col].ways = self.GetWays(col, row)
		if col in [0, self.col-1] or row in [0, self.row-1]:
			return 0
		if self.costmap[row][col].cost != 0 and (col, row) != self.catpos:
			if self.costmap[row][col].cost == 888:
				return 0
			return self.costmap[row][col].cost
		if row%2 == 0:#奇数行
			if col > 0 and row > 0 and col <= self.catpos[0] and row <= self.catpos[1]:#左上
				if self.IsValid(col-1, row-1):
					cost = self.GetCost(col-1, row-1) + 1
					if min > cost:
						min = cost
						
		if row > 0 and row <= self.catpos[1]:#上
			if self.IsValid(col, row-1):
				cost = self.GetCost(col, row-1) + 1
				if min > cost:
					min = cost
		
		if row%2:		
			if col < self.col and row > 0 and col >= self.catpos[0] and row <= self.catpos[1]:#右上
				if self.IsValid(col+1, row-1):
					cost = self.GetCost(col+1, row-1) + 1
					if min > cost:
						min = cost
			
		if col < self.col and col >= self.catpos[0]:#右
			if self.IsValid(col+1, row):
				cost = self.GetCost(col+1, row) + 1
				if min > cost:
					min = cost

		if row%2:		
			if col < self.col and row < self.row and col >= self.catpos[0] and row >= self.catpos[0]:#右下
				if self.IsValid(col+1, row+1):
					cost = self.GetCost(col+1, row+1) + 1
					if min > cost:
						min = cost	
							
		if row < self.row and row >= self.catpos[1]:#下
			if self.IsValid(col, row+1):
				cost = self.GetCost(col, row+1) + 1
				if min > cost:
					min = cost
							
		if row%2 == 0:#奇数行
			if col > 0 and row < self.row and col <= self.catpos[0] and row >= self.catpos[1]:#左下
				if self.IsValid(col-1, row+1):
					cost = self.GetCost(col-1, row+1) + 1
					if min > cost:
						min = cost
						
		if col > 0 and col <= self.catpos[0]:#左
			if self.IsValid(col-1, row):
				cost = self.GetCost(col-1, row) + 1
				if min > cost:
					min = cost
					
		#if min == 99:#99 or 0 cost pos waitting next cal
		#	print 'Is there anything wrong?(%d, %d)'%(col, row)
					
		if (col, row) != self.catpos:
			self.costmap[row][col].cost = min
		
		return min

	def UpdataCostMap(self):
		self.InitCostMap()
		self.GetCost(self.catpos[0], self.catpos[1])
			
	def GetWays(self, col, row):
		if col in [0, self.col-1] or row in [0, self.row-1]:
			return -1
		ways = 0
		if row%2 == 0:#奇数行
			if self.IsFree(col-1, row-1):#左上
				ways += 1
						
		if self.IsFree(col, row-1):#上
			ways += 1
		
		if row%2:		
			if self.IsFree(col+1, row-1):#右上
				ways += 1
			
		if self.IsFree(col+1, row):#右
			ways += 1

		if row%2:		
			if self.IsFree(col+1, row+1):#右下
				ways += 1
							
		
		if self.IsFree(col, row+1):#下
			ways += 1
							
		if row%2 == 0:#奇数行
			if self.IsFree(col-1, row+1):#左下
				ways += 1
						
		if self.IsFree(col-1, row):#左
			ways += 1
			
		return ways
		
	def IsWin(self):
		col,row = self.catpos[0], self.catpos[1]
		if col in [0, self.col-1] or row in [0, self.row-1]:
			return False
		ways = self.GetWays(col, row)
		if ways == 0:
			return True
		return False
		
	def PrintCostMap(self):
		idx = 0
		for i in self.costmap:
			if idx % 2:
				s = ''
				for data in i:
					cost = data.cost
					if cost == 100:
						cost = '#'
					elif cost == 888:
						cost = '@'
					else:
						cost = str(data.cost)
					s += ' ' + cost
				print s
			else:
				s = ''
				for data in i:
					cost = data.cost
					if cost == 100:
						cost = '#'
					elif cost == 888:
						cost = '@'
					else:
						cost = str(data.cost)
					s += cost + ' '
				print s
			idx += 1
		print ''
		
	def PrintWaysMap(self):
		idx = 0
		for i in self.costmap:
			if idx % 2:
				s = ''
				for data in i:
					s += ' ' + str(data.ways)
				print s
			else:
				s = ''
				for data in i:
					s += str(data.ways) + ' '
				print s
			idx += 1
		print ''
			
	def PrintMap(self):
		idx = 0
		for i in self.map:
			if idx % 2:
				print ' ' + str(i)
			else:
				print i
			idx += 1
			
		print ''
	
	def TestGame(self):
		self.InitGame()
		'''
		self.SetWall(7,7)
		self.SetWall(1,4)
		self.SetWall(2,4)
		self.SetWall(5,6)
		self.SetWall(4,6)
		self.SetWall(3,3)
		
		self.SetWall(3,4)
		self.SetWall(3,5)
		self.SetWall(3,6)
		self.SetWall(4,3)
		self.SetWall(5,3)
		self.SetWall(5,5)
		self.SetWall(5,4)
		self.SetWall(4,5)
		'''
		self.SetWall(2,0)
		self.SetWall(2,2)
		self.SetWall(2,3)
		self.SetWall(2,4)
		self.SetWall(2,5)
		self.SetWall(2,6)
		self.SetWall(2,7)
		self.SetWall(2,8)
		while True:
			self.PrintCostMap()
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
			x,y = self.GetNextPos()
			if (x,y) == (-1,-1):
				print 'badend'
				raw_input('>>>')
				self.InitGame()
			else:
				if x >= 0 and y >= 0:
					self.SetCatPos(x, y)
				if self.IsWin():
					print 'welldone'
					raw_input('>>>')
					self.InitGame()
		
		
Test = CatGame()

Test.TestGame()
	