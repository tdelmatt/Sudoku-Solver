assignments = []


#***************************HELPER FUNCTIONS********************************************

def cross(A, B):
	"Cross product of elements in A and elements in B."
	return [a+b for a in A for b in B]

	
col = '123456789'
row = 'ABCDEFGHI'
boxes = cross(row, col)
allrows = [cross(r, col) for r in row]
allcolumns = [cross(row, c) for c in col]
allsquares = [cross(row3s, col3s) for row3s in ["ABC", "DEF", "GHI"] for col3s in ["123", "456", "789"]]
diagonal1 = [a+col[n] for n, a in enumerate(row)]
diagonal2 = [a+col[8-n] for n, a in enumerate(row)]
alldiagonals = [diagonal1, diagonal2]
totalunits = allrows + allsquares + allcolumns + alldiagonals
units = {}

for box in boxes:
	units.setdefault(box, [unit for unit in totalunits if box in unit])
    
#summing the sets eliminates duplicates, subtracting the set eliminates the 
#element itself from its peers
peers = dict((box, set(sum(units[box], []))-set([box])) for box in boxes)

#****************************END HELPER FUNCTIONS********************************************


def assign_value(values, box, value):
	"""
	Please use this function to update your values dictionary!
	Assigns a value to a given box. If it updates the board record it.
	"""
	# Don't waste memory appending actions that don't actually change any values
	if values[box] == value:
		return values
	
	values[box] = value
	if len(value) == 1:
		assignments.append(values.copy())
	return values

	
#group boxes in each unit by length in separate lists 
#check if there are "length" other boxes in each list group, if not there are not enough for naked twins 
# 2 < length < 8 
#check that "length" of those other boxes have the same digits, if not there are no naked twins in the list group
#Once we find the naked twins we can eliminate those values from the rest of the unit.
def naked_twins(values):
	"""Eliminate values using the naked twins strategy.
	Args:
	values(dict): a dictionary of the form {'box_name': '123456789', ...}
	Returns:
	the values dictionary with the naked twins eliminated from peers.
	"""
	
	for unit in totalunits:
	
		#each unitlengths sublist (lengths) contains all boxes of the same length that are potential naked twins
		unitlengths = [[box for box in unit if len(values[box]) == j] for j in range(2,9)]

		#for all length arrays
		for n, lengths in enumerate(unitlengths):

				#now we need to search through lengths
				#for all boxes in each length array
				for n1, box in enumerate(lengths):
					
					#n+2 corresponds to the length of the boxes in that array
					#we know there must be at least n+2 boxes in that array with the same digits/value
					#if there are not enough lengths to possibly have naked twins, break
					if len(lengths) - n1 < n+2:
						break
					
					#we will add possible twins to this array
					postwins = [box]
					
					#remaining boxes in lengths array that are not current box
					otherlengths = [box1 for box1 in lengths[n1+1:len(lengths)]]
					
					#for all remaining boxes
					for box2 in otherlengths:
						
						#if the value is the same as our comparison box (box)
						if(values[box] == values[box2]):
							
							#append it to the possible twins array
							postwins.append(box2)
					
					#if the length of needed twins equals the length of possible twins
					#then we have naked twins, eliminate them from the board, and re-run naked twins with the 
					#updated values
					#the recursive call here prevents naked twins from not finding all available naked twins at any given time.  
					if len(postwins) == n+2:
						
						#remaining unit boxes not in naked twins
						notintwins = [box3 for box3 in unit if box3 not in postwins]
						
						#eliminate naked twins values from notintwins boxes
						for digit in values[postwins[0]]:
							for box4 in notintwins:
								values[box4] = values[box4].replace(digit, '')
								
	return values

	
def grid_values(grid):
	"""
	Convert grid into a dict of {square: char} with '123456789' for empties.
	Args:
	grid(string) - A grid in string form.
	Returns:
	A grid in dictionary form
		Keys: The boxes, e.g., 'A1'
		Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
		"""
	assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
	
	tempgrid = []
	for c in grid:
		#print(c)
		if c == '.':
			#print("dot encountered!")
			tempgrid.append('123456789')
		else:
			tempgrid.append(c)
			#pass
	     
	return dict(zip(boxes, tempgrid))


def display(values):
	"""
	Display the values as a 2-D grid.
	Args:
		values(dict): The sudoku in dictionary form
	"""
	print("------+------+------") 
	line = ""
	for n, digit in enumerate(boxes):
		n = n + 1
		astr = values[digit]
		if len(astr) > 1:
			astr = '.'
		if (n % 9 == 0) & (n >= 9):
			line = line + astr
			print(line)
			line = ""
		elif(n % 3 == 0) & (n >= 3):
			line = line + astr + " |"
		else:
			line = line + astr + " "
			
		if (n % 27 == 0) & (n  >= 27):
			print("------+------+------") 


def eliminate(values):
	"""
	Eliminate values from peers of each box with a single value.
	Go through all the boxes, and whenever there is a box with a single value,
	eliminate this value from the set of values of all its peers.
	Args:
		values: Sudoku in dictionary form.
	Returns:
		Resulting Sudoku in dictionary form after eliminating values.
	"""
	#for all boxes in dictionary
	for box in boxes:
	
		#if length(box) == 1:
		#meaning it is a found value
		if len(values[box]) == 1:
		
			#get peers
			temppeers = peers[box]
			
			#for all in peer indices (temppeers)
			for peer in temppeers:
			
				tempnmb = ""
				
				#for all numbers in peer value string
				for nmb in values[peer]:
					if nmb != values[box]:
						tempnmb = tempnmb + nmb
                
				values.update({peer: tempnmb})
				
	return values

	
def only_choice(values):
	"""Finalize all values that are the only choice for a unit.

	Go through all the units, and whenever there is a unit with a value
	that only fits in one box, assign the value to this box.

	Input: Sudoku in dictionary form.
	Output: Resulting Sudoku in dictionary form after filling in only choices.
	"""
	# TODO: Implement only choice strategy here

	#--------------MY OVERVIEW---------------

	#we are trying to find the most efficient way to check if each unit has one
	#of each number.  In order to do this, we probably need to keep an indexed count of 
	#how many of each number there is.  So that would be a 0-8 list (corresponding to 1-9)
	#each containing a list of indices within that unit that contain that number
	#at the end, we check the length of the list of indices for each number to see if any 
	#have one occurrence exactly.  !--- we could assert that none have zero occurrences ---!
	#If a unit has one occurrence, we will make its index equal to that value, omitting the rest.  

	#for all unit in units
	for unit in totalunits:
		
		numind = [[] for i in range(9)]
        
		#for all boxes in unit
		for box in unit:
            
			#for all char in values[box]
			for chr in values[box]:
			
				num = int(chr) - 1
				numind[num].append(box)
				
		#print(numind)
		for count, numlist in enumerate(numind):
			
			if len(numlist) == 1:
				values.update({numlist[0]:(str(count+1))})
			
	return values

	
def reduce_puzzle(values):
	improving = True
	
	#while the puzzle is still improving, continue the loop
	while improving == True:
		copyvalues = values.copy()
		
		#heuristics to reduce puzzle
		eliminate(values)
		only_choice(values)
		naked_twins(values)
		
		
		#for all boxes, check that there has been a length reduction somewhere, meaning the 
		#puzzle is still being reduced
		improving = False
		for box in boxes:
			if len(values[box]) < (len(copyvalues[box])):
				improving = True
				break
	
	#check to make sure that there are no boxes of length 0
	# a box of length 0 indicates a false solution
	#a false solution will lead to two of the same number in a unit
	#one of those will eliminate the other in eliminate
	for box in boxes:
		if len(values[box]) == 0:
			return 0
	return values

	
def search(values):
	"Using depth-first search and propagation, create a search tree and solve the sudoku."
	# First, reduce the puzzle using the previous function
	values = reduce_puzzle(values)  

	#if reduction ends in a false solution, return 0 so 
	#that recursion returns
	if values == 0:
		return 0
	
	#if successful solution, then return those values
	if all(len(values[s]) == 1 for s in boxes):
		return values
	
	# Choose one of the unfilled squares with the fewest possibilities
	#if the reduction did not yield a valid solution, then we need to continue reducing via
	#search, find the best square.  
	lenbox, box = min([(len(values[box]), box) for box in boxes if len(values[box]) > 1])
	
	
	for digit in values[box]:
		#print(digit)
		copyvalues = values.copy()
		copyvalues[box] = digit
		ding = search(copyvalues)
		if ding:
			return ding
		

def solve(grid):
	"""
	Find the solution to a Sudoku grid.
	Args:
		grid(string): a string representing a sudoku grid.
			Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	Returns:
		The dictionary representation of the final sudoku grid. False if no solution exists.
	"""
	
	values = grid_values(grid)
	return search(values)


if __name__ == '__main__':
	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	display(solve(diag_sudoku_grid))

	try:
		from visualize import visualize_assignments
		visualize_assignments(assignments)

	except SystemExit:
		pass
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
