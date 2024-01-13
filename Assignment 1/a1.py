class Empty(Exception):
    '''error in accessing an element from a container'''
    pass

class LinkedStack():         # Implementation of stack using linked list
    '''LIFO Stack implementation using a linked list as storage'''

    class _Node():          # Class to implement nodes
        '''Class for storing node'''
        __slot__ = ['_element','_next']

        def __init__(self,element,next):
            self._element = element
            self._next = next 

    def __init__(self):
        '''create an empty stack'''
        self._head = None
        self._size = 0

    def __len__(self):
        '''return the number of elements'''
        return self._size
    
    def is_empty(self):
        '''return True if the stack is empty'''
        return self._size == 0

    def push(self,i):
        '''Add i to the top of stack'''
        self._head = self._Node(i,self._head)               
        self._size += 1

    def pop(self):
        '''remove the top most element from the stack'''
        if self.is_empty():
            raise Exception("Stack is empty")
        popped = self._head._element
        self._head = self._head._next
        return popped

    def top(self):
        '''returns the element at the top of stack'''
        if self.is_empty():
            raise Empty('Stack is Empty')
        return self._head._element

    def __str__(self):
        '''for representing the stack as string'''
        string = self._head
        output = ''
        for i in range(self._size):
            output += str(string._element) + ', '
            string = string._next
        return '[' + output + ']>'



def findPositionandDistance(k):
    # This function returns the position and distance of the drone at the end of program.
    Brackets= LinkedStack()  # This stack keeps tracks of brackets and how many times the drone program needs to execute
    i = 0                   # i is the index for input 'k', which is given to the function
    n = len(k)
    def keep_track(k):      
        # This is a nested function, which maintains the stack 'Brackets' and keeps the track of x,y,z and d and the index i
        nonlocal i
        current = [0,0,0,0] # Initialisation of [x,y,z,d], (x,y,z) denote the position and d denotes the distance

        # Initialisation of while loop
        while i < n:
            # This loop checks elements of the input
            if k[i] == '+':             # Adds +1 to x, y, or z depending on what's being added in the input
                if k[i+1] == 'X':
                    current[0] += 1
                elif k[i+1] == 'Y':
                    current[1] += 1
                elif k[i+1] == 'Z':
                    current[2] += 1
                current[3] += 1
                i += 2
            elif k[i] == '-':           # Adds -1 to x, y, or z depending on what's being subtracted in the input
                if k[i+1] == 'X':
                    current[0] -= 1
                elif k[i+1] == 'Y':
                    current[1] -= 1
                elif k[i+1] == 'Z':
                    current[2] -= 1
                current[3] += 1
                i += 2
            elif (k[i].isdigit()):      # Handles the m(P) type of drone programs and adds the no of executions needed to the stack
                initial = i             # Keeps track of the left side index of m in m(P)
                while (k[i].isdigit()):
                    i += 1
                final = i               # Keeps track of the right side index of m in m(P)

                i += 1
                Brackets.push(int(k[initial:final]))        # pushes m in the stack. Here m is given by k[initial:final]
                A = keep_track(k)       # Calls the function keep_track for the inputs of m(P) drone program
                multiply = Brackets.pop()   # The drone program P for input m(P) needs to repeat n times, so here multiply = m
                for j in range(4):
                    current[j]+= multiply*A[j]      # Multiplies the no of times the program needs to execute to the values of [x,y,z,d] for one execution
            elif k[i] == ')':           # Terminates the recursion at close bracket
                i += 1
                return current          # returns the [x,y,z,d] for m(P) type of drone program
        return current                  # returns the final output of function keep_track(k)
    return keep_track(k)                # returns the final output