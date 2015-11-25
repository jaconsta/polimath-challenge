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
                        #id INTEGER PRIMARY KEY,
        cursor.execute('''CREATE TABLE categories (
                        categoryid INTEGER,
                        name TEXT,
                        level INTEGER,
                        parent INTEGER,
                        bestoffer INTEGER,
                        PRIMARY KEY(categoryid),
                        CONSTRAINT category_parent_fk FOREIGN KEY (parent) REFERENCES categories(categoryid))
                        ''')
        self.db.commit()

    def insertCategories(self, categories):
        '''
        '''
        # print (categories)
        cursor = self.db.cursor()
        cursor.executemany('''INSERT INTO categories (categoryid, name, level, parent, bestoffer) VALUES (?,?,?,?,?)''', categories)
        self.db.commit()

    def findCategory(self, categoryId):
        cursor = self.db.cursor()
        category = (categoryId, )
        cursor.execute('SELECT * FROM categories WHERE categoryId=?', category)
        return cursor.fetchone()

