#Binary tree implementation as a class (sort of)
#Holly LeMaster

class BinaryTree:

	def __init__(self, root):
		self.root = root

	def returnTree(self):
		return [self.root, [], []]

	#Add left subtree to specified root
	def insertLeft(self, root, newBranch):
		t = root.pop(1)

		if len(t) > 1:
			root.insert(1, [newBranch, t, []])
		else:
			root.insert(1, [newBranch, [], []])

		return root

	#Add right subtree to specified root
	def insertRight(self, root, newBranch):
		t = root.pop(2)

		if len(t) > 1:
			root.insert(2, [newBranch, [], t])
		else:
			root.insert(2, [newBranch, [], []])

		return root

	#Access functions
	#Get value of specified root
	def getRootVal(self, root):
		return root[0]

	#Set value of specified root
	def setRootVal(self, root, newVal):
		root[0] = newVal

	#Get left child of specified root
	def getLeftChild(self, root):
		return root[1]

	#Get right child of specified root
	def getRightChild(self, root):
		return root[2]

#Test it
tree = BinaryTree(3)
root = tree.returnTree()
tree.insertLeft(root, 4)
tree.insertLeft(root, 5)
tree.insertRight(root, 6)
tree.insertRight(root, 7)

left = tree.getLeftChild(root)
print(left)

print(root)



