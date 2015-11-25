#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
'''
import subprocess
import xml.etree.ElementTree as ET
import re

class categoriesXml():
    def __init__(self):
        self.xmlxs = '{urn:ebay:apis:eBLBaseComponents}'
        self.ebayUrl = 'https://api.sandbox.ebay.com/ws/api.dll'
        self.ebayToken = 'AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48'
        self.pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
    def getEbayHeaders():
        return {'X-EBAY-API-CALL-NAME': 'GetCategories',
                'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
                'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
                'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
                'X-EBAY-API-SITEID': '0',
                'iX-EBAY-API-COMPATIBILITY-LEVEL': '861',}
    def getCategoriesXML(self, route='sh ./get_categories.sh'):
        '''
        Uses the provided shell script file to get the categories from EBay.
        '''
        ebayCategories = subprocess.getoutput(route)
        # print(ebayCategories)
        return ebayCategories
    def stringToXML(self, unparsedXML):
        '''
        Converts a string xml to a valid xml object
        '''
        xmlRoot = ET.fromstring(unparsedXML)
        self.xmlRoot = xmlRoot
        return xmlRoot

    def getXmlXmlxs(self, xmlRoot):
        '''
        '''
        # pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
        result = re.match(self.pattern, xmlRoot.tag)
        self.xmlxs = result
        return result.group('xmlxs')

    def getXmlTagname(self, xmlTag):
        '''
        '''
        # pattern = '(?P<xmlxs>{.*[}])?(?P<tagname>[\w]*)'
        result = re.match(self.pattern, xmlTag)
        return result.group('tagname')

    def getXmlCategories(self, xmlRoot):
        '''
        '''
        xmlns = '{urn:ebay:apis:eBLBaseComponents}'
        #print('Root tag: ' + xmlRoot.tag)
        # CategoryArray
        categories = list(xmlRoot.iter(xmlns + 'Category'))
        self.unparsedCategories = categories
        print ('Found %i categories' % len(self.unparsedCategories))
        return categories
    def parseCategories(self, unparsedCateg):
        '''
          <BestOfferEnabled>true</BestOfferEnabled>
          <CategoryID>12605</CategoryID>
          <CategoryLevel>2</CategoryLevel>
          <CategoryName>Residential</CategoryName>
          <CategoryParentID>10542</CategoryParentID>
          <LeafCategory>true</LeafCategory>
          <LSD>true</LSD>
        '''
        categoryAttributes=('CategoryID', 'CategoryName', 'CategoryLevel', 'BestOfferEnabled', 'CategoryParentID')
        categories=[]
        for categoryChild in unparsedCateg:
            attributes = {}
            for category in categoryChild:
                if self.getXmlTagname(category.tag) in categoryAttributes:
                    attributes[self.getXmlTagname(category.tag)] = category.text
            categories.append((attributes['CategoryID'],
                                attributes['CategoryName'],
                                attributes['CategoryLevel'],
                                attributes['CategoryParentID'],
                                1 if attributes['BestOfferEnabled'] == 'true' else 0, )) # Ensure correct order.
        self.categories = categories
        return categories
