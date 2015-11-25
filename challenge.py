#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Polimath challenge code.

Extracting xml and generating categories.
  Specific details can be found in CHALLENGE.txt
'''
import os
import re
import subprocess
import xml.etree.ElementTree as ET
import sqlite3
import argparse
from jinja2 import Environment, PackageLoader, FileSystemLoader

from modules.categoryXML import categoriesXml
from modules.categoryDb import categoriesDb
from modules.exceptions import CategoryNotFount

#class CategoryNotFount(Exception):
#    def __init__(self, value):
#        self.value = value
#    def __str__(self):
#        return repr(self.value)

#def getCategoriesXML():
#    '''
#    Uses the provided shell script file to get the categories from EBay.
#    '''
#    ebayCategories = subprocess.getoutput('sh ./get_categories.sh')
#    # print(ebayCategories)
#    return ebayCategories
#
#def stringToXML(unparsedXML):
#    '''
#    Converts a string xml to a valid xml object
#    '''
#    xmlRoot = ET.fromstring(unparsedXML)
#    return xmlRoot
#
#def getXmlXmlxs(xmlRoot):
#    '''
#    '''
#    pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
#    result = re.match(pattern, xmlRoot.tag)
#    return result.group('xmlxs')
#
#def getXmlTagname(xmlTag):
#    '''
#    '''
#    pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
#    result = re.match(pattern, xmlTag)
#    return result.group('tagname')
#
#def getXmlCategories(xmlRoot):
#    '''
#    '''
#    xmlns = '{urn:ebay:apis:eBLBaseComponents}'
#    #print('Root tag: ' + xmlRoot.tag)
#    # CategoryArray
#    categories = list(xmlRoot.iter(xmlns + 'Category'))
#    print ('Found %i categories' % len(categories))
#    return categories
#
#def connectDb(name='challenge'):
#    '''
#    '''
#    conn = sqlite3.connect('%s.sqlite3' % name)
#    return conn
#
#def disconnectDb(db):
#    '''
#    '''
#    db.close()
#
#def createCategoriesTable(db):
#    '''
#    '''
#    cursor = db.cursor()
#    # Force non existance
#    cursor.execute('''DROP TABLE IF EXISTS categories''')
#    db.commit()
#    # And create the table
#                    #id INTEGER PRIMARY KEY,
#    cursor.execute('''CREATE TABLE categories (
#                    categoryid INTEGER,
#                    name TEXT,
#                    level INTEGER,
#                    parent INTEGER,
#                    bestoffer INTEGER,
#                    PRIMARY KEY(categoryid),
#                    CONSTRAINT category_parent_fk FOREIGN KEY (parent) REFERENCES categories(categoryid))
#                    ''')
#    db.commit()
#
#def insertCategories(db, categories):
#    '''
#    '''
#    # print (categories)
#    cursor = db.cursor()
#    cursor.executemany('''INSERT INTO categories (categoryid, name, level, parent, bestoffer) VALUES (?,?,?,?,?)''', categories)
#    db.commit()
#
#def findCategory(db, categoryId):
#    cursor = db.cursor()
#    category = (categoryId, )
#    cursor.execute('SELECT * FROM categories WHERE categoryId=?', category)
#    return cursor.fetchone()


def saveCategoryHtml(categoryHtml, categoryId):
    '''
    '''
    file = open('%s.html'%categoryId, 'w')
    file.write(categoryHtml)
    file.close()

def renderCategoryHtml(categoryList):
    '''
    '''
    PATH = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))
    template = env.get_template('categoryTemplate.html')
    render = template.render({'category':categoryList})
    return render

def createCategories():
    '''
    '''
    categ = categoriesXml()
    print('Getting categories.')
    categories = categ.getCategoriesXML()
    categories = categ.getXmlCategories(categ.stringToXML(categories))

    print('Connecting to database.')
    db = categoriesDb()
    db.connectDb()
    db.createCategoriesTable()

    print('Parsing categories.')
    parsedCategories = categ.parseCategories(categories)
    # print('parsedCategories: ', parsedCategories)
    db.insertCategories(parsedCategories)
    print('Categories creation complete.')
    db.disconnectDb()

def renderCategory(categoryId):
    '''
    '''
    print('Connecting to database.')
    db = categoriesDb()
    db.connectDb()
    print('Finding Category %s.'% categoryId)
    category = db.findCategory(categoryId)
    saveCategoryHtml(renderCategoryHtml(category), categoryId)
    print('Html generated with name %s.html', categoryId)
    db.disconnectDb()

def main():
    '''
    Main function
    '''
    print('Starting challenge.')
    parser = argparse.ArgumentParser()
    # Help values
    parser.add_argument('--rebuild', action="store_true", help='Refresh the category list.')
    parser.add_argument('--render', type=int, help='Creates the html with the category description.', default=False)
    # Process the desired output
    args = parser.parse_args()

    if args.rebuild:
        print("You asked for rebuild")
        createCategories()
    elif args.render:
        print("You asked for render")
        renderCategory(args.render)
    else:
        print('Please select a valid argument.')

    print('Challenge finished!')
    print('Bye bye')

main()
