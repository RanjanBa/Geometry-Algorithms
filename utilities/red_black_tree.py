class Node:
    RED_COLOR = 'RED'
    BLACK_COLOR = 'BLACK'
    def __init__(self, value, color=RED_COLOR):
        self.value = value
        self.color = color
        self.left : Node = None
        self.right : Node = None
        self.parent : Node = None

    def __str__(self):
        return self.color + ' '+ str(self.value)

class RedBlackTree:
    def __init__(self, cmp):
        self.__root : Node = None
        self.__size : int = 0
        self.__cmp = cmp

    @property
    def root(self):
        return self.__root

    @property
    def size(self):
        return self.__size

    def __str__(self, level=0, indent="\t") -> str:
        return 'size: ' + str(self.__size) + '\n' + self.__print(nd=self.__root)

    def __leftRotation(self, nd: Node):
        if nd.right is None:
            raise "nd.right is nil!"

        rt_child = nd.right
        rt_child_left_child = rt_child.left

        # left child becomes right child of node
        nd.right = rt_child_left_child
        if rt_child_left_child:
            rt_child_left_child.parent = nd

        if nd.parent is None:
            self.__root = rt_child
        else:
            if nd == nd.parent.left:
                nd.parent.left = rt_child
            else:
                nd.parent.right = rt_child
        
        rt_child.parent = nd.parent
        rt_child.left = nd
        nd.parent = rt_child

    def __rightRotation(self, nd: Node):
        if nd.left is None:
            raise "nd.left is nil!"
        
        lf_child = nd.left
        lf_child_rt_child = lf_child.right

        nd.left = lf_child_rt_child
        if lf_child_rt_child:
            lf_child_rt_child.parent = nd

        if nd.parent is None:
            self.__root = lf_child
        else:
            if nd == nd.parent.left:
                nd.parent.left = lf_child
            else:
                nd.parent.right = lf_child
            
        lf_child.parent = nd.parent
        lf_child.right = nd
        nd.parent = lf_child

    def __print(self,nd : Node=None, level=0, indent='   ') -> str:
        if nd is None:
            return ''
        txt = level * indent + str(nd) + '\n'
        if nd.left:
            txt += self.__print(nd=nd.left,level=level+1)
        if nd.right:
            txt += self.__print(nd=nd.right,level=level+1)
        return txt

    def __delete_fix(self, nd: Node):
        if nd is None:
            return
        while nd != self.__root and nd.color == Node.BLACK_COLOR:
            pass
        nd.color = Node.BLACK_COLOR

    def minimum(self, nd: Node = None):
        if nd is None:
            nd = self.__root
        
        while nd and nd.left:
            nd = nd.left

        return nd

    def maximum(self, nd: Node = None):
        if nd is None:
            nd = self.__root
        
        while nd and nd.right:
            nd = nd.right
        
        return nd

    def predecessor(self, nd: Node):
        if nd.left:
            return self.maximum(nd.left)

        parent = nd.parent
        while parent and parent.left == nd:
            nd = parent
            parent = parent.parent

        return parent

    def successor(self, nd: Node):
        if nd.right:
            return self.minimum(nd.right)
        parent = nd.parent

        while parent and parent.right == nd:
            nd = parent
            parent = parent.parent
        
        return parent

    def insert(self, nd : Node):
        prev_node : Node = None
        cur_node = self.__root
        while cur_node:
            prev_node = cur_node
            if self.__cmp(cur_node.value, nd.value):
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        
        nd.parent = prev_node

        if prev_node is None:
            self.__root = nd
        else:
            if self.__cmp(prev_node.value, nd.value):
                prev_node.left = nd
            else:
                prev_node.right = nd

        self.__size += 1        
        if nd == self.__root:
            nd.color = Node.BLACK_COLOR
            return
        
        nd.color = Node.RED_COLOR
        print('type: ', type(nd))
        while nd != self.__root and nd.parent.color == Node.RED_COLOR:
            grand_parent = nd.parent.parent
            parent_sibling = grand_parent.left
            if parent_sibling == nd.parent:
                parent_sibling = grand_parent.right
            
            if parent_sibling and parent_sibling.color == Node.RED_COLOR:
                parent_sibling.color = Node.BLACK_COLOR
                nd.parent.color = Node.BLACK_COLOR
                parent_sibling.parent.color = Node.RED_COLOR
                nd = parent_sibling.parent
            else:
                # rotation
                if nd.parent == grand_parent.left:
                    if nd == nd.parent.right:
                        nd = nd.parent
                        self.__leftRotation(nd)
                    nd.parent.color = Node.BLACK_COLOR
                    nd.parent.parent.color = Node.RED_COLOR
                    self.__rightRotation(nd.parent)
                else:
                    # parent of node is right child
                    if nd == nd.parent.left:
                        nd = nd.parent
                        self.__rightRotation(nd)

                    nd.parent.color = Node.BLACK_COLOR
                    nd.parent.parent.color = Node.RED_COLOR
                    self.__leftRotation(nd.parent)
        self.__root.color = Node.BLACK_COLOR

    def delete(self, nd: Node):
        if nd is None:
            raise Exception('None nd can\'t be deleted.')
        
        deleting_nd = nd
        if nd.left != None and nd.right != None:
            deleting_nd = self.successor(nd)
        
        # copy value
        nd.value = deleting_nd.value

        if deleting_nd.left:
            fixing_nd = deleting_nd.left
            fixing_nd.parent = deleting_nd.parent
        elif deleting_nd.right:
            fixing_nd = deleting_nd.right
            fixing_nd.parent = deleting_nd.parent
        else:
            fixing_nd = deleting_nd.parent
        
        if fixing_nd is None:
            self.__root = None
        else:
            if deleting_nd.parent is None:
                self.__root = fixing_nd
            else:
                if deleting_nd.parent.left == deleting_nd:
                    deleting_nd.parent.left = fixing_nd
                else:
                    deleting_nd.parent.right = fixing_nd

        if deleting_nd.color == Node.BLACK_COLOR:
            self.__delete_fix(fixing_nd)

        self.__size -= 1