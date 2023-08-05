# Операции с двоичным деревом поиска на Python

# Создаем узел
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# Отсортированный (inorder) обход
def inorder(root, level):
    if root is not None:

        # Обходим левое поддерево
        inorder(root.left, level + 1)

        # Обходим корень
        print(f'{root.key}:{level}', end=' ')

        # Обходим правое поддерево
        inorder(root.right, level + 1)

# Вставка элемента
def insert(node, key):
    # Возвращаем новый узел, если дерево пустое
    if node is None:
        return Node(key)

    # Идем в нужное место и вставляет узел
    if key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)
    return node

# Поиск inorder-преемника
def minValueNode(node):
    current = node
    # Найдем крайний левый лист — он и будет inorder-преемником
    while(current.left is not None):
        current = current.left
    return current

# Удаление узла
def deleteNode(root, key):
    # Возвращаем, если дерево пустое
    if root is None:
        return root

    # Найдем узел, который нужно удалить
    if key < root.key:
        root.left = deleteNode(root.left, key)
    elif(key > root.key):
        root.right = deleteNode(root.right, key)
    else:
        # Если у узла только один дочерний узел или вообще их нет        
        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        # Если у узла два дочерних узла,
        # помещаем центрированного преемника
        # на место узла, который нужно удалить
        temp = minValueNode(root.right)

        root.key = temp.key

        # Удаляем inorder-преемниа
        root.right = deleteNode(root.right, temp.key)

    return root