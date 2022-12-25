import json
import sys
import time
import os

# *** you can change everything except the name of the class, the act function and the problem_data ***

DEBUG = 4
if DEBUG > 0:
	debug_fout = open('debug_output.txt', 'w')

def info(*args):
	msg = 'Info: ' + (' '.join(args))
	print (msg)
	return
	
def error(*args):
	msg = 'Error: ' + (' '.join(args))
	print (msg)
	return
	
def debug(msg, level=1):
	if DEBUG >= level:
		msg = 'Debug: ' + msg
		debug_fout.write(msg + '\n')
	return
	
    # ^^^ DO NOT change the name of the class ***

class Al:
	def __init__(self,grid, i, j):
		assert(i >= 0 and i < 9)
		assert(j >= 0 and j < 9)
		self.i = i
		self.j = j
		self.current_val = -1
		self.vals = []
		self.used_vals = set()
		self.locked_vals = []
		
class sudoku_table_t:
	def __init__(self, int_2d_array):
		self.rows = 9
		self.cols = 9
		assert(type(int_2d_array) is list)
		assert(len(int_2d_array) == self.rows)
		
		self.constraints = [[] for i in range(self.rows)]
		
		for i in range(self.rows):
			assert(type(int_2d_array[i]) is list)
			assert(len(int_2d_array) == self.cols)
			for j in range(self.cols):
				self.constraints[i].append(set())
				val = int_2d_array[i][j]
				assert(is_valid(val) or val == -1)
		
		self.grid = int_2d_array
		return
		
	def next_placer_element(self):
		pe_list = []
		for i in range(self.rows):
			for j in range(self.cols):
				val = self.grid[i][j]
				if not is_valid(val):
					pe = placer_element_t(i, j)
					pe.vals = list(self.constraints[i][j])
					pe_list.append(pe)
		pe_list = sorted(pe_list, key = lambda pe : len(pe.vals))
		if pe_list:
			pe = pe_list[0]
			debug("Next PE (%d, %d) %d vals"%(pe.i + 1, pe.j + 1, len(pe.vals)))
			return pe
		else:
			return
			
		
	def undo_pe(self, pe):
		if pe.current_val == -1:
			return
		debug("<<<Undo %d at (%d, %d)"%(pe.current_val, pe.i + 1, pe.j + 1))
		pe.current_val = -1
		self.grid[pe.i][pe.j] = -1
		for i_j_pair in pe.locked_vals:
			i = i_j_pair[0]
			j = i_j_pair[1]
			self.grid[i][j] = -1
		return 
		
	def legal_vals(self, i, j):
		val_set = set()
		for icol in range(self.cols):
			if icol == j:
				continue
			val = self.grid[i][icol]
			if is_valid(val):
				val_set.add(val)
		for irow in range(self.rows):
			if irow == i:
				continue
			val = self.grid[irow][j]
			if is_valid(val):
				val_set.add(val)
		
		row_box = int(i / 3)
		col_box = int(j / 3)
		for irow in range(row_box * 3, row_box * 3 + 3):
			for icol in range(col_box * 3, col_box * 3 + 3):
				if irow == i and icol == j:
					continue
				val_set.add(self.grid[irow][icol])
				
		legal_vals = set(range(1, 10)) - val_set
		return legal_vals
		
	def dump(self, stage=''):
		pad_stars = 30 - len(stage)
		if pad_stars < 0:
			pad_stars = ''
		else:
			pad_stars = '*' * pad_stars
		if stage:
			info(pad_stars + ' Begin ' + stage + ' ' + pad_stars)
		
		info(' --------- --------- ---------')
		for i in range(self.rows):
			row_str = '|'
			for j in range(self.cols):
				val = self.grid[i][j]
				if val == -1:
					row_str += '   '
				else:
					row_str += ' %d '%val
				if ((j + 1) % 3) == 0:
					row_str += '|'
			info(row_str)
			if ((i + 1) % 3) == 0:
				info(' --------- --------- ---------')
					
			
		if stage:
			info(pad_stars + '* End ' + stage + ' *' + pad_stars)
		return
	
    # the solve function takes a json string as input
    # and outputs the solved version as json
		
	def solve(self,problem):
		for i in range(self.rows):
			for j in range(self.cols):
				val = self.grid[i][j]
				if not is_valid(val):
					return False
		return True
		
def num_unsolved(self):
		count = 0
		for i in range(self.rows):
			for j in range(self.cols):
				val = self.grid[i][j]
				if not is_valid(val):
					count += 1
		return count
		
def l_load_table():
	info('Beginning placement preparation')
	
	if len(sys.argv) != 2:
		error('Expected exactly one command line argument giving the name of the sudoku file in jSON format')
		exit(1)
	
	sudoku_filename = sys.argv[1]
	if not os.path.isfile(sudoku_filename):
		error('Could not open sudoku filename %s'%sudoku_filename)
		exit(1)
	
	f_in = open(sudoku_filename)
	int_2d_array = json.load(f_in)
	table = sudoku_table_t(int_2d_array)
	table.dump(stage = 'initial board')
	info('Placement preparation operations ending')
	print ('')

        # ^^^ DO NOT change the solve function above ***
	#TODO implement your code here
	
def main():
	table = l_load_table()
	l_do_placement(table)
	problem_data = json.loads(problem)
	
	return finished





        
	
