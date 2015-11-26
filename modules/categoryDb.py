#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
'''

import sqlite3

class categoriesDb():
    def __init__(self, name='challenge'):
        self.dbname = name
    def connectDb(self, name='challenge'):
        '''
        Creates a new connection to the local sqlite database
        '''
        conn = sqlite3.connect('%s.sqlite3' % self.dbname)
        self.db = conn
        return conn

    def disconnectDb(self):
        '''
        Closes connection to database
        '''
        self.db.close()

    def createCategoriesTable(self):
        '''
        '''
        cursor = self.db.cursor()
        # Force non existance
        cursor.execute('''DROP TABLE IF EXISTS categories''')
        self.db.commit()
        # And create the table
        cursor.execute('''CREATE TABLE categories (
                        categoryid INTEGER,
                        name TEXT,
                        level INTEGER,
                        parent INTEGER,
                        bestoffer INTEGER,
                        CONSTRAINT category_parent_fk FOREIGN KEY (parent) REFERENCES categories(categoryid))
                        ''')
        self.db.commit()
        # First dummy insert
        cursor.execute('''INSERT INTO categories (categoryid, name, level, parent, bestoffer) values (1, "root", 0, 1, 0)''')
        self.db.commit()
        #cursor.execute('''''')
        #self.db.commit()

    def insertCategories(self, categories):
        '''
        '''
        # print (categories)
        cursor = self.db.cursor()
        cursor.executemany('''INSERT INTO categories (categoryid, name, level, parent, bestoffer) VALUES (?,?,?,?,?)''', categories)
        self.db.commit()

    def toDictionay(self, result):
        if (len(result)<1):
            return []
        values = tuple(result)
        return list(map(lambda x,y: dict(zip(x.keys(), y)), result, values))

    def findCategory(self, categoryId):
        self.db.row_factory = sqlite3.Row
        cursor = self.db.cursor()
        category = (categoryId, )
        cursor.execute('SELECT * FROM categories WHERE categoryId=?', category)
        return cursor.fetchone()

    def findChildren(self, parentId):
        self.db.row_factory = sqlite3.Row
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM categories WHERE parent=?', (parentId,))
        return self.toDictionay(cursor.fetchall())

