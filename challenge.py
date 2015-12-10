#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Polimath challenge code.

Extracting xml and generating categories.
  Specific details can be found in CHALLENGE.txt
"""
import os
import argparse
from jinja2 import Environment, PackageLoader, FileSystemLoader

from modules.categoryXML import categoriesXml
from modules.categoryDb import categoriesDb
from modules.exceptions import CategoryNotFount


def saveCategoryHtml(categoryHtml, categoryId):
    """
    """
    file = open('%s.html' % categoryId, 'w')
    file.write(categoryHtml)
    file.close()


def renderCategoryHtml(categoryList):
    """
    """
    PATH = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))
    template = env.get_template('categoryTemplate.html')
    render = template.render({'category':categoryList})
    return render


def processSubCategories(db, categ, parentCategories):
    """
    """
    if len(parentCategories) > 0:
        print('Started processing: Level %s, %s subcategories.' % (parentCategories[0][2], parentCategories[0][1]))
        categories = categ.requestCategories(categoryFilter=parentCategories[0][0])
        categories = categ.getXmlCategories(categ.stringToXML(categories))
        if len(categories) > 1:
            parsedCategories = categ.parseCategories(categories)
            db.insertCategories(parsedCategories)
            # processSubCategories(db, categ, parsedCategories[1:]) # Process children
        return processSubCategories(db, categ, parentCategories[1:])  # Keep current node processing
    else:
        print('-------------')
        return


def getCategoryChildren(db, parentCategory):
    """
    """
    categories = []
    for category in parentCategory:
        category['children'] = db.findChildren(category['categoryid'])
        if len(category['children']) > 1:
            category['children'] = getCategoryChildren(db, category['children'][1:])
        categories.append(category)
    return categories


def createCategories():
    """
    """
    print('Connecting to database.')
    db = categoriesDb()
    db.connectDb()
    db.createCategoriesTable()

    categ = categoriesXml()
    print('Getting basic Level 1 categories.')
    categories = categ.requestCategories(levelFilter=0)
    #categories = categ.getCategoriesXML()
    categories = categ.getXmlCategories(categ.stringToXML(categories))

    print('Parsing categories.')
    parsedCategories = categ.parseCategories(categories)
    # db.insertCategories(parsedCategories)
    processSubCategories(db, categ, parsedCategories)
    print('Categories creation complete.')
    db.disconnectDb()


def renderCategory(categoryId):
    """
    """
    print('Connecting to database.')
    db = categoriesDb()
    db.connectDb()
    print('Finding Category %s.' % categoryId)
    category = db.findChildren(categoryId)  # db.findCategory(categoryId)
    category = getCategoryChildren(db, category[1:])

    saveCategoryHtml(renderCategoryHtml(category), categoryId)
    print('Html generated with name %s.html' % categoryId)
    db.disconnectDb()


def main():
    """
    Main function
    """
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
