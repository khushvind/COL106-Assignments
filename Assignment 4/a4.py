from math import log
import random
import math
import string

# Here I have taken m = len(p), n = len(x)

# Computes the pth power of 26 using loop
def pow_26(p,q):
	h=1
	if p == 0:
		return h
	else:
		for i in range(p):
			h = (h*26)%q
	return h

# This function return the index of letter a 
def index(a):
	return (string.ascii_uppercase.index(a))

# This function returns the value of function f(x) for a sting x
def f(y,q):
	sum = 0
	for i in range(0,len(y)):
		sum = (sum * 26 + index(y[i])) % q      # % takes O(log(q)) time
	return sum % q  
# Time Complexity: f(y,q) = O(m.log(q))
# Space Complexity = log(q) (Requires to store log(q) bits)

# This function returns the value of function f(x) for string x, and also the position of wildcard ('?')
def f_wildcard_p(y,q):
	if y[0] != '?':
		sum = index(y[0])
	else:
		sum = 0
		wildcards = 0
	for i in range(1,len(y)):
		if y[i] != '?':
			sum = (sum * 26 + index(y[i])) 
		else:
			sum = (sum * 26 + 0) 
			wildcards = i
	return [sum % q,wildcards]

# To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

# Pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)				
# Time Complexity of modPatternMatch(): O((m+n).log(q))    # This time complexity is proved below
# 	We know that q <= N = 2.(m.k/eps).log(m.k/eps) = 2.(m/eps).(const + log(m/eps)) 
# 	O(log(q)) < O(log(2.(m/eps).(const + log(m/eps)))) < O(log(m/eps)+log(const+log(m/eps)) which is O(log(m/eps))
# 	So time complexity : O((m+n).log(m/eps))
# Space Complexity: 
#	Space Complexity of madPatternMatch : O(log(m)+log(q)+k)
# 	Using similar argument, 
# 	Space Complexity: O(k + log n + log(m/eps))


# Pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)
# Time Complexity of modPatternMatch(): O((m+n).log(q))    # This time complexity is proved below
# 	We know that q <= N = 2.(m.k/eps).log(m.k/eps) = 2.(m/eps).(const + log(m/eps)) 
# 	O(log(q)) < O(log(2.(m/eps).(const + log(m/eps)))) < O(log(m/eps)+log(const+log(m/eps)) which is O(log(m/eps))
# 	So time complexity : O((m+n).log(m/eps))
# Space Complexity: 
#	Space Complexity of madPatternMatch : O(log(m)+log(q)+k)
# 	Using similar argument, 
# 	Space Complexity: O(k + log n + log(m/eps))


# Return appropriate N that satisfies the error bounds
def findN(eps,m):
	k = 2.2*log(26,2)
	return (int(2*(m*k/eps)*log(m*k/eps,2)))
# Verfication for the value of N: (Here the base of log used is 2)
# We need to choose a N such that, x[i....i+m-1] is not equal to the pattern p 
# To find the error, we need to find P( f(p)%q = f(x[i....i+m-1])%q/ (p != x[i....i+m-1]) <= eps
# Which is same as P(f(x[i....i+m-1])-f(p))%q == 0/(p != x[i....i+m-1])) <= eps
# No of prime factors of |f(x[i....i+m-1])-f(p)| if log(|f(x[i....i+m-1])-f(p)|) (given in assignment statement)
# No of primes less than N, are Pi(N)
# Probability that q is a factor is the difference |f(x[i....i+m-1])-f(p)| = No of prime factors of |f(x[i....i+m-1])-f(p)|/No of primes less than N
# log(|f(x[i....i+m-1])-f(p)|)/Pi(N) <= eps
# The max order of difference term |f(x[i....i+m-1])-f(p)| is 26^m, So log(26^m)/Pi(N) <= eps                
# m.log(26)/(N/2.log(N)) <= eps which implies 2.m.log(26)/eps <= N/log(N)
# Take k = 2.m.log(26)/eps, So k <= N/log(N)
# Now for approximate N to a.k.log(k), where a is some constant, and this approximation is quite suitable,(more better approximations my exist        
# Now a.k.log(k)/log(a.k.log(k) = a.k.log(k)/(log(a)+log(k)+log(log(k))) 
# Now using a plotting the graph of (log(a)+log(k)+log(log(k))/a.log(k), we try to find k and a such that (log(a)+log(k)+log(log(k))/a.log(k) <= 1
# By hit and trial for a on a graphing calculator, we can observe that for a >= 2, k <= a.k.log(k)/(log(a)+log(k)+log(log(k)) for all suitable k
# Hence we use N = 2 * 2(m.log(26)/eps).log(m.log(26)/eps), Better approximations may exist                                                                    



# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	f_p = f(p,q)							# Requires O(m.log(q)) time, and O(log(q)) bit space
	i_list = []								# Space required = O(No of elements strored in the list) = O(k)
	prev = f(x[0:len(p)],q)					# Runs in O(m)+O(m.log(q)) < O(m.log(q))
	if prev == f_p:
		i_list.append(0)					
	k = pow_26(len(p)-1,q)					# Runs in O(m)
	for i in range(len(x) - len(p)):
		prev = ((prev - (index(x[i])*k))*26 + (index(x[i+len(p)])))%q			# Requires O(log(q)) time (for each loop), and O(log(q) space 
		if prev % q == f_p:					
			i_list.append(i+1)
	return i_list
# Time Complexity: 
# 	n > m (observation)
#	Time taken by f(p,q) = O(m.log(q)) 
#	The time taken by f(x[0:len(p)],q) is O(m)+O(m.log(q)), O(m) for slicing, and O(m.log(q)) for function f()
# 	Time taken in each step of loop, O(1), the loop runs len(x)-len(p) = n - m  times, which is O((n-m).log(q)) as all operations in each step of loop run in O(1), 
# 	except the comparing operation, which runs in O(log(q)) time, here base of log(q) if 2
#	overall time taken is T(n,m) = O(m.log(q)) + O(m) + O(n.log(q) = O(m.log(q) + n.log(q))
# 	Time complexity = O((m+n).log(q))

# Space Complexity:
# 	Working memory need to store the value of f_p, the no of bits required to be stored = O(log(q)) bits
# 	No of bits that need to be stored in working memory for the current index = O(log(n) bits
# 	Space required to store the elements in the output list = O(k)
#	No of bits required to store the value of prev = log(q)
# 	Overall space complexity of the function modPatternMatch() = O(log(q)+ O(log(q)+ log(n) + O(k) = O(log(m)+log(q)+k)


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
	f_p,wildcards = f_wildcard_p(p,q)[0], f_wildcard_p(p,q)[1]			# Requires O(m.log(q)) time, and O(log(q)) bit space
	i_list = []															# Space required = O(No of elements strored in the list) = O(k)
	prev = f(x[0:len(p)],q)												# Runs in O(m)+O(m.log(q)) < O(m.log(q))
	k = pow_26(len(p)-1,q)												# Runs in O(m)	
	j = pow_26(len(p)-wildcards-1,q)									# Runs in O(m)
	if (prev - index(x[wildcards])*j)  == f_p:
		i_list.append(0)
	for i in range(0,len(x) - len(p)):
		prev = ((prev - (index(x[i])*k))*26 + (index(x[i+len(p)])))%q	# Requires O(log(q)) time (for each loop), and O(log(q) space 
		if (prev - (index(x[i+1+wildcards])*j)) % q == f_p:
			i_list.append(i+1)
	return i_list
# Time Complexity: 
# 	n > m (observation)
#	Time taken by f(p,q) = O(m.log(q)) 
#	The time taken by f(x[0:len(p)],q) is O(m)+O(m.log(q)), O(m) for slicing, and O(m.log(q)) for function f()
# 	Time taken in each step of loop, O(1), the loop runs len(x)-len(p) = n - m  times, which is O((n-m).log(q)) as all operations in each step of loop run in O(1), 
# 	except the comparing operation, which runs in O(log(q)) time, here base of log(q) if 2
#	overall time taken is T(n,m) = O(m.log(q)) + O(m) + O(m) + O(n.log(q) = O(m.log(q) + n.log(q))
# 	Time complexity = O((m+n).log(q)

# Space Complexity:
# 	Working memory need to store the value of f_p, the no of bits required to be stored = O(log(q)) bits
# 	No of bits that need to be stored in working memory for the current index = O(log(n) bits
# 	Space required to store the elements in the output list = O(k)
#	No of bits required to store the value of prev = log(q)
# 	Overall space complexity of the function modPatternMatch() = O(log(q)+ O(log(q)+ log(n) + O(k) = O(log(m)+log(q)+k)