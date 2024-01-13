class PointDatabase():
    '''Implementation of Database of pointsk, (similar to Range Tree)'''

    class Tree_Node():
        '''Implementation of Node of Tree'''
        __slots__ = 'key','Y_Tree','left','right','range' 
        def __init__(self):
            self.key = None
            self.Y_Tree = None          
            # Y_Tree is an associated data structure at each node and has all the elements of subtree of node as its own element, and it is a list
            self.left = None
            self.right = None
            self.range = None
    
    def __init__(self,P):
        '''Implementation of Data Structure'''
        # Here I have created a tree with root at 'root', the tree is a height balanced BST, wrt its x coordinates. 
        # Each node also contains an associated data structure, which is a list of elements of the subtree rooted at the node. This list is sorted wrt y coordinates 
        if len(P) != 0:
            X = P
            X.sort()
            self.root = self.make_tree(X)
        else:
            self.root = None

    def merge(self,a,b,y):   # This function merges two sorted list and inserts y in them
        '''Function to merge two sorted lists and insert y'''
        x = y[1]
        output = []
        i,j = 0,0
        inserted = False
        while i<len(a) and j<len(b):
            if a[i][1] < b[j][1]:
                if x<a[i][1] and not inserted:
                    output.append(y)
                    inserted = True
                output.append(a[i])
                i+= 1
            elif a[i][1] > b[j][1]:
                if x<b[j][1] and not inserted:
                    output.append(y)
                    inserted = True
                output.append(b[j])
                j+= 1
            else:
                if x<a[i][1] and not inserted:
                    output.append(y)
                    inserted = True
                output.append(a[i])
                i+= 1
                j+= 1
        if i == len(a):
            for b_ in b[j:]:
                if x<b_[1] and not inserted:
                    output.append(y)
                    inserted = True
                output.append(b_)
        else:
            for a_ in a[i:]:
                if x<a_[1] and not inserted:
                    output.append(y)
                    inserted = True
                output.append(a_)
        if not inserted:
            output.append(y)
        return output

    def make_tree(self,X):
        '''Function to make a tree using recursion'''
        # This function makes a tree
        root = self.Tree_Node()
        i = (len(X)+1)//2 
        root.key = X[i-1]
        if len(X)>1:
            if len(X[i:])> 0:
                root.right = self.make_tree(X[i:])    # Creates the right subtree of root
            if len(X[:i-1])> 0:
                root.left = self.make_tree(X[:i-1])   # Creates the left subtree of root

        # The following lines assign the associated data structure (Y_Tree) at each node
        l,r = root.left,root.right
        if len(X) == 1:
            root.Y_Tree = X
        else:
            if l == None:
                l_list = []
            else: 
                l_list = l.Y_Tree 
            if r == None:
                r_list = []
            else: 
                r_list = r.Y_Tree
            root.Y_Tree = self.merge(l_list, r_list, root.key)  # merges the associated data stuructures (list sorted wrt y coordinates)

        # The following lines help to assign the range attribute at each node
        if l == None:
            a = root.key[0]
        else:
            a = l.range[0]
        if r == None:
            b = root.key[0]
        else:
            b = r.range[1]
        root.range = [a,b] # stores the range of 'x' for the subtree rooted at this root
        return root 
        # Returns the node

    def inorder(self):
        '''Outputs the inorder traversal of X - tree'''
        output = []
        K = self.root
        def recur(K):
            nonlocal output
            if K != None:
                recur(K.left)
                output.append(K.key)
                recur(K.right)
        recur(K)
        print (output)

    def preorder(self):
        '''Outputs the preorder traversal of X - tree'''
        output = []
        K = self.root
        def recur(K):
            nonlocal output
            if K != None:
                output.append(K.key)
                recur(K.left)
                recur(K.right)
        recur(K)
        print (output)

    def searchNearby(self,q ,d ):
        '''Searches the points occuring on and inside the square with center q, and side 2d'''
        if self.root == None:       # When no tree exists
            return []
        x1 = q[0] - d
        x2 = q[0] + d
        y1 = q[1] - d
        y2 = q[1] + d
        output = []
          
        def One_d_Query(P,y):
            # Binary search for Y_Tree data structure
            # It works by finding the left and right limits of range and then returns all the elements within that range
            y1,y2 = y
            n = len(P)
            if y2 < P[0][1] or P[n-1][1] < y1:
                return [] 
            l,r = 0,n-1
            while l!= r:
                i = (l+r)//2
                if P[i][1] == y1 or (i == 0 and y1<=P[i][1]) :
                    left = i
                    break
                elif P[i][1] < y1:
                    l = i + 1
                elif y1 < P[i][1]:
                    if P[i-1][1]<= y1 < P[i][1]:
                        if P[i-1][1]==y1:
                            left = i-1
                        else:
                            left = i
                        break
                    else:
                        r = i - 1
                if l == r:
                    left = l
            l,r = 0,n-1
            while l != r:
                i = (l+r)//2 
                if P[i][1] == y2 or (i == n-1 and P[i][1] <= y2) :
                    right = i
                    break
                elif y2 < P[i][1]:
                    r = i - 1
                elif P[i][1] < y2:
                    if P[i][1]<y2 <= P[i+1][1]:
                        if y2 == P[i+1][1]:
                            right = i+1
                        else:
                            right = i
                        break
                    else:
                        l = i + 1
                if l == r:
                    right = r
            return P[left :right+1]
            
        def Search(t,x,y):
            # This function performs the recursion and recursively finds the required points
            # It is similar to query search in Range Tree
            nonlocal output
            if x[0] <= t.key[0] <= x[1] and y[0] <= t.key[1] <= y[1]:
                    output.append(t.key)
            if t.left == None and t.right == None:
                pass
            elif t.left == None:
                output = list(set(output+Search(t.right,x,y)))
            elif t.right == None:
                output = list(set(output+Search(t.left,x,y)))
            else:
                x1,x2 = t.range[0],t.range[1]   # Returns the 'x' range of subtree at root t
                if x[0] <= x1 <= x2 <= x[1]:
                    output += One_d_Query(t.Y_Tree,y)           # when both side range of subtree lie inside [x1,x2], this line does binary search in Y_Tree
                elif x1 < x[0] <= x2 or x1 <= x[1] < x2:
                    output += list(set(Search(t.left,x,y)+Search(t.right,x,y)))
            return (output)
        Search(self.root,(x1,x2),(y1,y2))
        final_list = list(set(output))
        return final_list
        # returns the final list 