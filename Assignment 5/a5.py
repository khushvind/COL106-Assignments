class BinaryHeap():       
    '''Heap implementation using Array'''
    def __init__(self,l,n):
        '''create a list to implement heap'''
        self._data = [l]
        self.size = 1
        self.location_vertex = [-1 for i in range(n) ]
        self.location_vertex[l[1]]=0
    
    def HeapUp(self,i):
        '''Implementation of heap up, when x.parent.key < x.key'''
        k = (i-1)//2
        x = self._data[i]
        while (self._data[k] < x) and k >= 0:
            self._data[k],self._data[i] = self._data[i],self._data[k]
            self.location_vertex[self._data[i][1]]=i
            self.location_vertex[self._data[k][1]]=k
            i = k
            k = (k-1)//2

    def HeapDown(self,i):
        '''Implementation of heap down, when x.child.key > x.key'''
        x = self._data[i]
        while (True):
            i_left = i*2+1
            i_right = i*2+2
            if i==0 and self.size==1:
                break
            elif (i_right <=self.size -1):
                if self._data[i_right] <= self._data[i_left]: 
                    k = i_left
                else: 
                    k = i_right
                if self._data[k] > x:
                    self._data[k],self._data[i] = self._data[i],self._data[k]
                    self.location_vertex[self._data[i][1]]=i
                    self.location_vertex[self._data[k][1]]=k
                else:
                    break
            elif (i_left <=self.size -1):
                k = i_left
                if self._data[k] > x:
                    self._data[k],self._data[i] = self._data[i],self._data[k]
                    self.location_vertex[self._data[i][1]]=i
                    self.location_vertex[self._data[k][1]]=k
                else:
                    break
            else:
                break
            i = k
            
    def enqueue(self,x):
        '''Add element to the binary tree'''
        if self.location_vertex[x[1]] == -1:
            self._data.append(x)
            self.size += 1
            self.location_vertex[x[1]]=self.size-1
            self.HeapUp(self.size - 1)
        else:
            if self._data[self.location_vertex[x[1]]] > x:
                pass
            else:
                self._data[self.location_vertex[x[1]]]=x
                k = self.location_vertex[x[1]]
                if self._data[(k-1)//2] < x:
                   self.HeapUp(k)
                else:
                    self.HeapDown(k)

    def extract_max(self):
        '''return the minimum element of heap'''
        extracted, self._data[0] = self._data[0], self._data[-1]
        self.location_vertex[extracted[1]]= -1
        self.location_vertex[self._data[0][1]]= 0
        self.size -= 1
        self._data.pop()
        if self.size >0:
            self.HeapDown(0)
        return (extracted)

    def is_empty(self):
        '''Returns if the Heap is empty'''
        if len(self._data) == 0:
            return True
        else:
            return False
    

def find_path(parents,s,t):   # Function to find the path which provides the max capacity
    path = [t]
    current = t
    while (True):
        current = parents[current]
        path.append(current)
        if current == s:
            break
    path.reverse()
    return path

    # This function is a modified version of Dijkstra's algorithm to find the max capacity
def findMaxCapacity(n,links,s,t):           # Function to find max capacity that can be trasferred between two vertices
    # This function goes through all the vertices in the graph, and finds the max capacity for each vertex from the source
    adjacency_list = [[] for i in range(n)]
    for i in links:
        u,v,c = i
        adjacency_list[u].append((c,v))
        adjacency_list[v].append((c,u))
    max_c = [ -1 for i in range(n)]
    max_c[s] = float('inf')                 # The capacity of source is kept infinity
    parents = [False for i in range(n)]  
    priority_heap = BinaryHeap((max_c[s],s),n)  
    while not priority_heap.is_empty():
        c,v = priority_heap.extract_max()
        if v == t:
            break
        for i in adjacency_list[v]:
            if i[1] == s:
                continue
            max_possible = max((min(i[0],c),max_c[i[1]]))
            if max_possible > max_c[i[1]]:
                max_c[i[1]] = max_possible
                priority_heap.enqueue((min(i[0],c),i[1]))
                parents[i[1]] = v
    path = find_path(parents,s,t)
    return (max_c[t],path)
    # Returns max capacity, and the path

