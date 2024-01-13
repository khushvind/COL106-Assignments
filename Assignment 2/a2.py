class BinaryHeap():                     # Implementation of heap Data Strucutre. I have modified it to add a list '_collision' to reduce the time complexity
    '''Heap implementation using Array'''
    def __init__(self,l,n):
        '''create a list to implement heap'''
        self._data = l                     
        # Each element of list is a tuple of type (t,x,i) which shows collision b/w i and i+1 particles, where t is time of collision, x is position of collision, and i is the index of particle
        self.size = len(l)
        self._collision = [False for i in range(n)]      # This list stores the index of i collision in Heap List, or stores 'False' if no collision exists
        for i in range(self.size):
            self._collision[self._data[i][-1]] = i
    
    def HeapUp(self,i):
        '''Implementation of heap up, when x.parent.key > x.key'''
        k = (i-1)//2
        x = self._data[i]
        while (self._data[k] > x) and k >= 0:
            self._data[k],self._data[i] = self._data[i],self._data[k]
            self._collision[self._data[i][-1]] = i 
            self._collision[self._data[k][-1]] = k 
            i = k
            k = (k-1)//2

    def HeapDown(self,i):
        '''Implementation of heap down, when x.child.key < x.key'''
        x = self._data[i]
        end = False
        while (not end):
            i_left = i*2+1
            i_right = i*2+2
            if i==0 and self.size==1:
                self._collision[self._data[i][-1]] = i
                end = True
            elif (i_right <=self.size -1):
                if self._data[i_right] >= self._data[i_left]: 
                    k = i_left
                else: 
                    k = i_right
                if self._data[k] < x:
                    self._data[k],self._data[i] = self._data[i],self._data[k]
                    self._collision[self._data[i][-1]] = i 
                    self._collision[self._data[k][-1]] = k 
                else:
                    end = True
                i = k
            elif (i_left <=self.size -1):
                k = i_left
                if self._data[k] < x:
                    self._data[k],self._data[i] = self._data[i],self._data[k]
                    self._collision[self._data[i][-1]] = i 
                    self._collision[self._data[k][-1]] = k 
                else:
                    end = True
            else:
                end = True
            
    def enqueue(self,x):
        '''Add element to the binary tree'''
        self._data.append(x)
        self._collision[x[-1]] = self.size
        self.size += 1
        self.HeapUp(self.size - 1)

    def extract_min(self):
        '''return the minimum element of heap'''
        self._collision[self._data[0][-1]] = False
        extracted, self._data[0] = self._data[0], self._data[-1]
        self.size -= 1
        if self.size>0:
            self._collision[self._data[0][-1]] = 0
        self._data.pop()
        if self.size >0:
            self.HeapDown(0)
        return (extracted)

    def change_key(self,i,x):    
        '''Changes the key at i in Heap list to x'''
        k = self._collision[i]
        self._collision[i] = False
        self._data[k] = x
        self._collision[x[-1]] = k
        if self._data[(k-1)//2] > x:
            self.HeapUp(k)
        else:
            self.HeapDown(k)

    def is_empty(self):
        '''Returns if the Heap is empty'''
        if len(self._data) == 0:
            return True
        else:
            return False

    def will_collide(self,i):
        if str(self._collision[i]) == 'False':
            return False
        else:
            return True
    
    def find_collision(self,i):
        '''Finds if i collision is already present in Heap list'''
        return self._data[self._collision[i]]

    def __str__(self):
        '''to print the Heap in list form'''
        return ('[' + ' '.join(list(map(str,self._data)))) + ']'


def BuildHeap(l,n):
    # This function builds a heap using an initial set of given collisions
    H = BinaryHeap(l,n)
    for i in reversed(range(len(l))):
        H.HeapDown(i)
    return H   

def vel(M,v,i):
    # This function returns the values of velocity after the collision of i and i+1 particles
    v1 = ((M[i]-M[i+1])*v[i]+2*M[i+1]*v[i+1])/(M[i]+M[i+1])    
    v2 = (2*M[i]*v[i]-(M[i]-M[i+1])*v[i+1])/(M[i]+M[i+1])   
    return (v1,v2) 

def time_pos(x,v,i):
    # This function returns the time and position of collision between the particles i and i+1
    t = (x[i+1]-x[i])/abs(v[i+1]-v[i])
    pos = (v[i+1]*x[i]-x[i+1]*v[i])/(v[i+1]-v[i])
    return (t,pos)

def find_time_pos1(x,v,t,i):
    # This function returns the time and position of collision between the particles i and i+1, after adjusting the position for i
    time = (x[i+1]-(x[i]+v[i]*t))/abs(v[i+1]-v[i])
    pos = (v[i+1]*(x[i]+v[i]*t)-x[i+1]*v[i])/(v[i+1]-v[i])
    return time,pos

def find_time_pos2(x,v,t,i):
    # This function returns the time and position of collision between the particles i and i+1, after adjusting the position for i+1
    time = ((x[i+1]+v[i+1]*t)-x[i])/abs(v[i+1]-v[i])
    pos = (v[i+1]*x[i]-(x[i+1]+v[i+1]*t)*v[i])/(v[i+1]-v[i])
    return time,pos

def listCollisions(M,x,v,m,T):
    # This function returns a list of collisions in order of time and position such that the number of collision is < m or time taken by them <T
    n = len(M)
    collision_list = [] # This list will contain all the possible collisions that will happen directly after time t == 0 
    p_time = [0 for i in range(n)]
    time = 0
    for i in range(n-1):
        if v[i+1]-v[i] < 0:
            t,pos = time_pos(x,v,i) 
            if len(collision_list) != 0:
                if collision_list[-1][-1] == i-1 and t < collision_list[-1][0]:
                    collision_list[-1] = (time+t,pos,i)
                elif collision_list[-1][-1] != i-1:
                    collision_list.append((time+t,pos,i))   
            else:
                collision_list.append((time+t,pos,i))
    
    collisions = BuildHeap(collision_list,n)    # 'collisions' is a heap that contains the collisions
    col = []                                    # 'col' is a list that will contain the collision as they happen
    while len(col)<m and time<T:   # Loop invariant: col contains collisions that have happened such that len(col) < m or time of collision < T
        # Termination: len(col)>=m or time >= T
        if collisions.is_empty():
            break
        c = collisions.extract_min()        # Returns the cooision from 'collisions' which happens in next least time
        time = c[0]
        if time >= T:
            break
        i = c[-1]
        x[i],x[i+1] = c[1],c[1]
        v[i],v[i+1] = vel(M,v,i)
        p_time[i],p_time[i+1] = time,time
        col.append((round(time,4),i,round(c[1],4)))
        if i >= 1:                          # This checks for possible collision for element before i, and enqueues the collision to 'collisions' is possible
            k = i-1
            if v[k+1]-v[k] < 0:             # This is the condition for collision between k and k+1
                if collisions.will_collide(k-1):
                    c1 = collisions.find_collision(k-1)
                    t,pos = find_time_pos1(x,v,time-p_time[k],k)
                    if time + t < c1[0]:
                        collisions.change_key(k-1,(time+t , pos, k))
                    elif time + t == c1[0]:
                        collisions.enqueue((time+t , pos, k))
                else:
                    t,pos = find_time_pos1(x,v,time-p_time[k],k)
                    collisions.enqueue((time+t , pos, k))
        if i<= n-3:                         # This checks for possible collision for element after i+1, and enqueues the collision to 'collisions' is possible
            k = i+1                
            if v[k+1]-v[k] < 0:             # This is the condition for collision between k and k+1
                if collisions.will_collide(k+1):
                    c1 = collisions.find_collision(k+1)
                    t,pos = find_time_pos2(x,v,time-p_time[k+1],k)
                    if time + t < c1[0]:
                        collisions.change_key(k+1,(time+t , pos, k))
                    elif time + t == c1[0]:
                        collisions.enqueue((time+t , pos, k))
                else:    
                    t,pos = find_time_pos2(x,v,time-p_time[k+1],k)
                    collisions.enqueue((time+t , pos, k))
    return (col)            
    # Returns the list of collisions in a sorted order.