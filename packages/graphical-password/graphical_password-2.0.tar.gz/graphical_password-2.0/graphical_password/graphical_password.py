import uuid
import hashlib

from imghdr import what
from os.path import exists

import image_examples
from tree import *
from exceptions import GPerror

def catcher(func):
    def _wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as error:
            raise GPerror(error.args)
    return _wrapper

class Image:
    def __init__(self, path: str) -> None:
        self.triggered = False

        @catcher
        def check():
            assert(exists(path), 'Файла с таким именем не существует.')
            assert(what(path) is not None, 'Файл не является картинкой.')
        check()

        with open(path, mode='rb') as file:
            self.data = file.read()
    
    def trigger(self):
        self.triggered = not self.triggered

    def is_triggered(self):
        return self.trigger


class Group_Image:
    def __init__(self) -> None:
        self.images = []
        self.root = None
        self.counter = 0
        self.tree_size = 0
        self.associate = dict()
        self.index_in_tree = []

    def __getitem__(self, index):
        return self.images[index]
    
    def trigger(self, index):
        # get the index in self.images

        @catcher
        def check():
            assert(0 <= index < len(self.images), 
                   'Индекс картинки должен быть положительным числом, меньшим, чем количество всех картинок в группе.')
        check()
        
        self.images[index].trigger()
        if self.images[index].is_triggered():
            self.root = insert(self.root, self.counter)
            self.index_in_tree[index] = self.counter
            self.associate[self.counter] = index
            self.counter += 1
            self.tree_size += 1
        else:
            self.root = deleteNode(self.root, self.index_in_tree[index])
            self.index_in_tree[index] = -1
            self.tree_size -= 1
            
    def add_to_group(self, picture: Image):
        @catcher
        def check():
            assert(isinstance(picture, Image), 'В группу можно добавить только объекты картинок.')
            assert(self.tree_size > 3, 'Слишком мало выбранных картинок. Высока вероятность отгадать пароль.')
        check()

        self.images.append(picture)
        self.index_in_tree.append(-1)
        
    def get_password(self):
        @catcher
        def check():
            assert(len(self.images) > 0, 'В группе нет картинок.')
            assert(self.tree_size > 0, 'В группе нет выбранных картинок.')
        check()

        def inorder(root):
            if root is None:
                return ''
            return inorder(root.left) + str(self.images[self.associate[root.key]].data) + inorder(root.right)
        password = inorder(self.root)

        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()