#Veniamin Velikoretskikh  veniamin@pdx.edu
#CS302 Fall 2025  Karla Fant

#This file will hold the implementation of the BST and Node class
# Node class has a constructor and getters
# BST class has insert, retrieve, display and remove by user_id. All recursive.
# BST class also has helper function to find inorder successor, and helper to find the num of nodes


import CS302_Core_Hierarchy


# Node class
# will have getters, to get and set left and right nodes
# The data will be a profile of a Social media
class Node:
    def __init__(self, profile):
        if not isinstance(profile, CS302_Core_Hierarchy.SocialMediaProfile) and profile is not None:
            raise TypeError("Node data must be a Social Media Profile")
        
        self._data = profile
        self._left = None
        self._right = None

    def get_data(self):
        return self._data
    
    def get_left(self):
        return self._left
    
    def get_right(self):
        return self._right
    
    def set_left(self, node):
        self._left = node

    def set_right(self, node):
        self._right = node


# BST Class
# ---------------------------------------------------
class BST:
    def __init__(self):
        self._root = None

    # wrapper for insert
    def insert(self, profile):
        if not isinstance(profile, CS302_Core_Hierarchy.SocialMediaProfile):
            raise TypeError("Can only insert Social Media Profile objects")
        self._root = self._insert_recursive(self._root, profile)

    # protected recursive insert
    def _insert_recursive(self, node, profile):
        if node is None:
            return Node(profile)
        
        if profile < node.get_data():
            node.set_left(self._insert_recursive(node.get_left(), profile))
        elif profile > node.get_data():
            node.set_right(self._insert_recursive(node.get_right(), profile))
        else:
            #same user_id , we'll replace updated profile data is stored
            node._data = profile
        return node
    
    #-------------------------------------------------------
    # Wrapper for retrieve
    def retrieve(self, user_id):
        return self._retrieve_recursive(self._root, user_id)
    
    # Protected recursive retrieve
    def _retrieve_recursive(self, node, user_id):
        if node is None:
            return None
        if user_id == node.get_data().get_user_id():
            return node.get_data()
        elif user_id < node.get_data().get_user_id():
            return self._retrieve_recursive(node.get_left(), user_id)
        else:
            return self._retrieve_recursive(node.get_right(), user_id)
        
    #--------------------------------------------------------
    # wrapper for display in order
    def display_inorder(self):
        return self._display_inorder_recursive(self._root)
    
    # protected recursive display in order
    def _display_inorder_recursive(self, node):
        if node is None:
            return []
        return (self._display_inorder_recursive(node.get_left()) +
                [node.get_data()] + 
                self._display_inorder_recursive(node.get_right()))
    

    #--------------------------------------------------------
    # wrapper for remove by user_id
    def remove(self, user_id):
        self._root, removed = self._remove_recursive(self._root, user_id)
        # returns true or false if removed or not
        return removed
    
    # protected recursive remove by user_id
    def _remove_recursive(self, node, user_id):
        if node is None:
            return (None, False)

        current_id = node.get_data().get_user_id()

        if user_id < current_id:
            new_left, removed = self._remove_recursive(node.get_left(), user_id)
            node.set_left(new_left)
            return (node, removed)
        
        elif user_id > current_id:
            new_right, removed = self._remove_recursive(node.get_right(), user_id)
            node.set_right(new_right)
            return (node, removed)
        
        else:
            # Found the node to remove

            # Case 1, no children
            if node.get_left() is None and node.get_right() is None:
                return (None, True)

            # Case 2, one child
            if node.get_left() is None:
                return (node.get_right(), True)
            if node.get_right() is None:
                return (node.get_left(), True)
            
            # Case 3, two childre, replace with inorder successor
            successor = self._find_min_node(node.get_right())

            # copy successor data into current node
            node._data = successor.get_data()

            #remove successor by user_id 
            new_right, _ = self._remove_recursive(node.get_right(), successor.get_data().get_user_id())
            node.set_right(new_right)
            return (node, True)
        
    #----------------------------------------------------------------

    #helper function to find the min node in a subtree
    def _find_min_node(self, node):
        if node.get_left() is None:
            return node
        return self._find_min_node(node.get_left())
    

    # count nodes wrapper
    def size(self):
        return self._size_recursive(self._root)
    
    # count nodes recursive
    def _size_recursive(self, node):
        if node is None:
            return 0
        return 1 + self._size_recursive(node.get_left()) + self._size_recursive(node.get_right())
    




# Quick test for the functions in BST class, so I can run just this file.
if __name__ == "__main__":
    tree = BST()
    a = CS302_Core_Hierarchy.SocialMediaProfile("m", "M")
    b = CS302_Core_Hierarchy.SocialMediaProfile("g", "G")
    c = CS302_Core_Hierarchy.SocialMediaProfile("t", "T")
    tree.insert(a)
    tree.insert(b)
    tree.insert(c)
    print("Before remove:", [p.get_user_id() for p in tree.display_inorder()])
    tree.remove("g")
    print("After remove:", [p.get_user_id() for p in tree.display_inorder()])