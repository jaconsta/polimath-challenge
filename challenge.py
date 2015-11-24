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

class CategoryNotFount(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def getCategoriesXML():
    '''
    Uses the provided shell script file to get the categories from EBay.
    '''
    ebayCategories = subprocess.getoutput('sh ./get_categories.sh')
    # print(ebayCategories)
    return ebayCategories

def stringToXML(unparsedXML):
    '''
    Converts a string xml to a valid xml object
    '''
    xmlRoot = ET.fromstring(unparsedXML)
    return xmlRoot

def getXmlXmlxs(xmlRoot):
    '''
    '''
    pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
    result = re.match(pattern, xmlRoot.tag)
    return result.group('xmlxs')

def getXmlTagname(xmlTag):
    '''
    '''
    pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
    result = re.match(pattern, xmlTag)
    return result.group('tagname')

def getXmlCategories(xmlRoot):
    '''
    '''
    xmlns = '{urn:ebay:apis:eBLBaseComponents}'
    #print('Root tag: ' + xmlRoot.tag)
    # CategoryArray
    categories = list(xmlRoot.iter(xmlns + 'Category'))
    print ('Found %i categories' % len(categories))
    return categories

def connectDb(name='challenge'):
    '''
    '''
    conn = sqlite3.connect('%s.db' % name)
    return conn

def disconnectDb(db):
    '''
    '''
    db.close()

def createCategoriesTable(db):
    '''
    '''
    cursor = db.cursor()
    # Force non existance
    cursor.execute('''DROP TABLE IF EXISTS categories''')
    db.commit()
    # And create the table
    cursor.execute('''CREATE TABLE categories (
                    id INTEGER PRIMARY KEY,
                    categoryid INTEGER, name TEXT,
                    level INTEGER, bestoffer INTEGER)
                    ''')
    db.commit()

def insertCategories(db, categories):
    '''
    '''
    # print (categories)
    cursor = db.cursor()
    cursor.executemany('''INSERT INTO categories (categoryid, name, level, bestoffer) VALUES (?,?,?,?)''', categories)
    db.commit()

def findCategory(db, categoryId):
    cursor = db.cursor()
    category = (categoryId, )
    cursor.execute('SELECT * FROM categories WHERE categoryId=?', category)
    return cursor.fetchone()

def parseCategories(unparsedCateg):
    '''
      <BestOfferEnabled>true</BestOfferEnabled>
      <CategoryID>12605</CategoryID>
      <CategoryLevel>2</CategoryLevel>
      <CategoryName>Residential</CategoryName>
      <CategoryParentID>10542</CategoryParentID>
      <LeafCategory>true</LeafCategory>
      <LSD>true</LSD>
    '''
    categoryAttributes=('CategoryID', 'CategoryName', 'CategoryLevel', 'BestOfferEnabled',)
    categories=[]
    for categoryChild in unparsedCateg:
        attributes = {}
        for category in categoryChild:
            if getXmlTagname(category.tag) in categoryAttributes:
                attributes[getXmlTagname(category.tag)] = category.text
        categories.append((attributes['CategoryID'],
                            attributes['CategoryName'],
                            attributes['CategoryLevel'],
                            1 if attributes['BestOfferEnabled'] == 'true' else 0, )) # Ensure correct order.
    return categories

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
    print('Getting categories.')
    categories = getCategoriesXML()
    categories = getXmlCategories(stringToXML(categories))

    print('Connecting to database.')
    db = connectDb()
    createCategoriesTable(db)

    print('Parsing categories.')
    parsedCategories = parseCategories(categories)
    # print('parsedCategories: ', parsedCategories)
    insertCategories(db, parsedCategories)
    print('Categories creation complete.')
    disconnectDb(db)

def renderCategory(categoryId):
    '''
    '''
    print('Connecting to database.')
    db = connectDb()
    print('Finding Category %s.'% categoryId)
    category = findCategory(db, categoryId)
    saveCategoryHtml(renderCategoryHtml(category), categoryId)
    print('Html generated with name %s.html', categoryId)

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
# print('Starting challenge.')
# print('Getting categories.')
# categories = getCategoriesXML()
# categories = getXmlCategories(stringToXML(categories))
#
# print('Connecting to database.')
# db = connectDb()
# createCategoriesTable(db)
#
# print('Parsing categories.')
# parsedCategories = parseCategories(categories)
# print('parsedCategories: ', parsedCategories)
# insertCategories(db, parsedCategories)
# print('Categories creation complete.')
# disconnectDb(db)
# print('Bye bye.')
