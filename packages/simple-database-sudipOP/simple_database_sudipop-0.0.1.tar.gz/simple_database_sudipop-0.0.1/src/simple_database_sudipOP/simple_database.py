import os
import pickle

DATABASE_EXTENSION = ".hide"
KEY_EXTENSION = ".key"


class Database:
    def __init__(self, data_base_file: str):
        '''load a database'''
        self.data_base_path = data_base_file
        self.__data = []
        self.__keys = None
        self.__load_data_base()

    def __load_data_base(self):
        if not os.path.exists(self.data_base_path):
            print("No databse found")
            return

        with open(self.data_base_path, 'rb') as file:
            self.__data = pickle.loads(file.read())

        with open(self.data_base_path.replace(DATABASE_EXTENSION, KEY_EXTENSION), 'rb') as key_file:
            self.__keys = pickle.loads(key_file.read())

    @staticmethod
    def create(database_name: str, path: str = ".", keys: tuple = None):
        if path != '.':
            os.makedirs(path)

        with open(f"{path}/{database_name}{DATABASE_EXTENSION}", 'wb') as f1:
            f1.write(pickle.dumps([]))

        with open(f"{path}/{database_name}{KEY_EXTENSION}", 'wb') as f2:
            f2.write(pickle.dumps(keys))

        print(
            f"Database created at {path}/{database_name}{DATABASE_EXTENSION}")

    def getKeys(self) -> tuple:
        '''get the name of the keys'''
        return self.__keys

    def gets(self) -> list:
        '''get the whole database'''
        return self.__data

    def get(self, index: int) -> dict:
        '''get the value at given index'''
        if (index < 0 or index > len(self.__data) - 1):
            print("invalid index")
            return None
        return self.__data[index]

    def add(self, data: tuple) -> bool:
        '''add data\n
           careful about the same key pair\n
           return true : sucessfully add the data\n
                  false: something gone wrong
        '''
        if (len(data) != len(self.__keys)):
            print("can not add the data, please check your input data")
            return False

        self.__data.append(dict(zip(self.__keys, data)))
        return True

    def remove(self, index: int) -> bool:
        '''
            remove value at index\n
            return true: sucessfully remove the data\n
                   false: can not remove the data
        '''

        if (index < 0 or index > len(self.__data) - 1):
            print("invalid index")
            return False

        self.__data.pop(index)
        return True

    def pop(self):
        '''remove the last data'''
        if (len(self.__data) == 0):
            print("database is empty")
        else:
            self.__data.pop()

    def changeData(self, index:int, new_data:tuple) -> bool:
        '''change data at index'''
        d_len = len(self.__data)
        n_len = len(new_data)
        k_len = len(self.__keys)
        if (index < 0 or index > d_len + 1 or k_len != n_len):
            print('invalid inputs')
            return False
        
        self.__data[index] = dict(zip(self.__keys, new_data))
        return True
    

    def save(self):
        '''save the database\n
           this function is not needed, when this object is destroyed it automatically saved the data
        '''
        with open(self.data_base_path, 'wb') as file:
            file.write(pickle.dumps(self.__data))

    def __del__(self):
        self.save()
