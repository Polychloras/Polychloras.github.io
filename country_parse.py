import os
import string
import json

'''
Name(s): Emily Massie, Mehrdad Yadholli
Project Goal: Build a Website in D3 to visulize information on 12 South American Countries
Date: 10/30/2023

Script: This python file reads each of the tweleve documents and 
organizes the information before placing it into a json file for html use


'''
# Country
# Creates one instance of a country
#
class country():
     def __init__(self):
          self.table = {}
          self.timeline = {}
          self.meminit = {}
          self.sites = []
          self.orgs = []
          self.issue = []
          self.links = []

     # Organze Actors and Categories
     def set_listed_vals(self, strg, name):
        name_vals = strg.split(':')
        vals = name_vals[1].replace('.', '')
        vals = vals.split(';')
        for val in range(len(vals)):
             vals[val] = vals[val].lower().strip()
        self.table.update({name: vals})

     # add all information to class
     def add_vals(self, listed):
        self.name = listed[0]
        self.table.update({'Country': self.name})
        self.set_dates(listed[1])
        self.set_listed_vals(listed[2], 'Categories')
        self.set_listed_vals(listed[3], 'Actors')
        
      # read in summary and historical events  
        if(listed[4] == 'Key historical events'):
             self.table.update({'Summary':""})
             b = self.set_events(listed, 5)
        else:
             self.table.update({'Summary':listed[4]})
             b = self.set_events(listed, 6)

     # set all other information based on header location
        c = self.set_meminit(listed, b+1)
        d = self.set_sites(listed, c+1)
        e = self.set_orgs(listed, d+1)
        f = self.set_iss(listed, e+1)
        self.table.update({'Links': listed[f+1:]})

     # organize events
     def set_events(self, listed, a):
          b = listed.index('Memory initiatives')
          event_date = []
          event_desc = []
          for event in listed[a:b]:
                 year_event = event.split('-')
                 event_date.append(int(year_event[0]))
                 event_desc.append(event)
                 self.timeline.update({"Dates":event_date})
                 self.timeline.update({"Events":event_desc})
          return b

     # organize memory inititives
     def set_meminit(self, listed, b):
          c = listed.index('Sites of memory')
          events = []
          dates = []
          for strg in listed[b:c]:
               topic_summ = strg.split('-', 1)
               dates.append(int(topic_summ[0]))
               events.append(topic_summ[1])
          
          self.meminit.update({'Dates':dates})
          self.meminit.update({"Event": events})
               
          return c       

     # get all momory sites
     def set_sites(self, listed, c):
          d = listed.index('Organisations')
          for i in listed[c:d]:
               self.set_sitesinfo(i)
          return d
     
     # organize each site
     def set_sitesinfo(self, strg):
            topic_summ = strg.split(':')
            self.sites.append(topic_summ[0] +': ' + topic_summ[1])
    
    # get all organizations
     def set_orgs(self, listed, c):
          d = listed.index('Issues specific to the country')
          for i in listed[c:d]:
               self.set_orgsinfo(i)
          return d

     # set each organiization into file
     def set_orgsinfo(self, strg):
            topic_summ = strg.split(':')
            self.orgs.append(topic_summ[0] +": " + topic_summ[1])

     # set issues specific to country
     def set_iss(self, listed, c):
          d = listed.index('Links')
          for i in listed[c:d]:
               self.set_issinfo(i)
          return d

     def set_issinfo(self, strg):
            self.issue.append(strg)

     # set the dates and topic from document header
     def set_dates(self, strg):
            strg = strg.lower().strip()
            topic_date = strg.split('(')
            topics = topic_date[0].replace('and', ',')
            topics = topics.split(',')
            for topic in range(len(topics)):
                 topics[topic] =  topics[topic].strip()
            date = topic_date[1].replace(')', '')
            date = date.split('-')
            start = date[0][0:4]
            if(not date[1] == ''):
                end = date[1].strip().lower()
            else:
                end = '2023'
            self.table.update({'Topics':topics})
            self.table.update({'Start_Date': int(start)})
            self.table.update({'End_Date': int(end)})

#------- Getter Functions --------------------------------------
     def get_time(self):
          return self.timeline
     
     def get_mil(self):
          return self.table
     
     def get_mem(self):
          return self.meminit
     
     def get_memsites(self):
          return self.sites
     
     def get_orgs(self):
          return self.orgs
     
     def get_issue(self):
          return self.issue
     
     # return all country values
     def add_country(self):
          self.table.update({'Events': self.get_time()})
          self.table.update({'Memory_Inititives': self.get_mem()})
          self.table.update({'Sites_of_Memory': self.get_memsites()})
          self.table.update({'Organizations': self.get_orgs()})
          self.table.update({'Issues':self.get_issue()})
          return self.table

def remove_all(list_top, char):
     nlines = list_top.count(char)
     for i in range(nlines):
          list_top.remove('\n')


def clean_all(list_top):
     lines = []
     for line in list_top:
          if(len(line) > 0):
               lines.append(line.strip())
     return lines

def get_categories(country_dict, element):
     categories = []
     for country in country_dict:
          ctry_cat = country[element]
          
          if (type(ctry_cat) != list):
               categories.append(ctry_cat)
          else:
               for elements in ctry_cat:               
                    if(categories.count(elements) < 1):
                              categories.append(elements)
          
     return dict({'feature': element, 'items':categories})

def main():
    folder_name = 'Countries'
    country_dicts = []
    country_ele = []
    if(not os.path.isdir(folder_name)):
        print("Error")
        exit()
    else:
        countries = os.listdir(folder_name)
        for doc in countries:
            file_name = f'{folder_name}/{doc}'
            if(not os.path.isfile(file_name)):
                    print('Error')
                    exit()
            country_file = open(file_name, 'r', encoding = "utf-8")
            lines = country_file.readlines()
            country_file.close()
            remove_all(lines, '\n')
            lines = clean_all(lines)
            country_new = country()
            country_new.add_vals(lines)
            table = country_new.add_country()
            country_dicts.append(table)
            
        keys = list(country_dicts[0].keys())

        for element in keys:
             print(element)
             element_dict = get_categories(country_dicts, element)
             country_ele.append(element_dict)
           
        # https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        countries_json = open('12Data.json', 'w')
        info_dump = json.dumps(country_dicts, indent= 1)
        countries_json.write(info_dump)

        elements_json = open('12Collective.json', 'w')
        ele_dump = json.dumps(country_ele, indent= 1)
        elements_json.write(ele_dump)
        


main()