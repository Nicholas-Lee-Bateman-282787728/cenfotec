def isPal(x):
	assert type(x) == list
	temp = type(x.reverse)
	print temp
	print x
	if temp == x:
		return True
	else:
		return False

def silly(n):
	result = []
	for i in range(n):
		elem = raw_input('Enter element: ')
		result.append(elem)
	if isPal(result):
		print('Yes')
	else:
		print('No')

silly(5)