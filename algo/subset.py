# The algorithm is given here:
# http://en.wikipedia.org/wiki/Subset_sum_problem#Pseudo-polynomial_time_dynamic_programming_solution

def get_subset(lst, s):
	'''Given a list of integer `lst` and an integer s, returns
	a subset of lst that sums to s, as well as lst minus that subset
	'''
	q = {}
	for i in range(len(lst)):
		for j in range(1, s+1):
			if lst[i] == j:
				q[(i, j)] = (True, [j])
			elif i >= 1 and q[(i-1, j)][0]:
				q[(i, j)] = (True, q[(i-1, j)][1])
			elif i >= 1 and j >= lst[i] and q[(i-1, j-lst[i])][0]:
				q[(i, j)] = (True, q[(i-1, j-lst[i])][1] + [lst[i]])
			else:
				q[(i, j)] = (False, [])

		if q[(i, s)][0]:
			for k in q[(i, s)][1]:
				lst.remove(k)

			return q[(i, s)][1], lst

	return None, lst

def get_n_subsets(n, lst, s):
	''' Returns n subsets of lst, each of which sums to s'''
	solutions = []
	for i in range(n):
		sol, lst = get_subset(lst, s)
		solutions.append(sol)

	return solutions, lst


# print(get_n_subsets(7, [1, 2, 3, 4, 5, 7, 8, 4, 1, 2, 3, 1, 1, 1, 2], 5))
# [stdout]:	([[2, 3], [1, 4], [5], [4, 1], [2, 3], [1, 1, 1, 2], None], [7, 8])
