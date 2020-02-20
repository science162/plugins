#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
get_ipython().system('pip install zipfile36')
get_ipython().system('pip install requests')
get_ipython().system('pip install wget')
"""
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import zipfile as zp
import os
import wget
import re

class PluginReader:
    
    temp = os.path.join(os.curdir,'temp') 
    
    def __init__(self, url):
        self.url = url
    
    def createTempDir():
        try:
            os.mkdir(os.path.join(os.curdir,'temp'))
        except FileExistsError:
            print("Le dossier temp est déjà créé")


    def dropTempDir(self):
        try:
            os.remove(os.path.join(self.temp,'content.xml'))
            os.remove(os.path.join(self.temp,'content.jar'))
            os.remove(self.temp)
        except PermissionError:
            print('Droit de suppression absent')
        except FileNotFoundError:
            print('Fichier absent')

    def getxml(self):
        return  ET.XML(requests.get(self.url).text)

    def getXMLData(self):
        path = wget.download(self.url,self.temp)
        os.rename(zp.ZipFile(path).extract('content.xml'),os.path.join(self.temp,'content.xml'))
        data = ET.parse(os.path.join(self.temp,'content.xml'))
        return data

    def getData(self):
        jar = re.compile('\.jar$', re.IGNORECASE)
        xml = re.compile('\.xml$', re.IGNORECASE)
        if len(re.findall(jar,self.url)) > 0:
            if re.findall(jar,self.url)[0] == '.jar':
                root = self.getXMLData().getroot()
        elif len(re.findall(xml,self.url)):
            if re.findall(xml,self.url)[0] == '.xml':
                root = getxml()
        return root



    def listPlugins(self):
        self.dropTempDir()
        root = self.getXMLData().getroot()
        plugins = {}
        for child in root:
            for schild in child:
                if schild.tag == 'unit':
                    for xchild in schild:
                        if xchild.tag == 'provides':
                            dico = {}
                            versionList = []
                            for provided in xchild:
                                versionList.append(provided.attrib['version'])
                            plugins[schild.attrib['id']] = sorted(set(versionList),reverse=True) 
        self.dropTempDir()
        return plugins
    
    def getPlugin(self,id):
        return self.listPlugins()[id]
            
url1 = 'https://download.jboss.org/jbosstools/updates/m2e-extensions/m2e-jdt-compiler/1.0.0/content.jar'
url2 =  'http://dependencies.sarl.io/content.jar' 
url3 = 'http://download.eclipse.org/releases/2019-12/201910181000/content.jar'
url4 = 'http://download.tuxfamily.org/arakhne/p2/content.jar'


# In[2]:


p = PluginReader(url3)
plug = p.listPlugins()


# In[4]:


print(plug)


# In[ ]:




