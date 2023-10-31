import os
import string
import csv

class country():
     def __init__(self):
          self.table = {}
          self.timeline = {}
          self.meminit = {}
          self.sites = {}
          self.orgs = {}

     def set_listed_vals(self, strg, name):
        name_vals = strg.split(':')
        vals = name_vals[1].replace('.', '')
        vals = vals.split(';')
        self.table.update({name: vals})

     def add_vals(self, listed):
        self.name = listed[0]
        self.table.update({'Country': self.name})
        self.set_dates(listed[1])
        self.set_listed_vals(listed[2], 'Categories')
        self.set_listed_vals(listed[3], 'Actors')
        
        if(listed[4] == 'Key historical events'):
             self.table.update({'Summary':""})
             b = self.set_events(listed, 5)
        else:
             self.table.update({'Summary':listed[4]})
             b = self.set_events(listed, 6)
        c = self.set_meminit(listed, b+1)
        d = self.set_sites(listed, c+1)
        e = self.set_orgs(listed, d+1)
        self.table.update({'Issues specific to the country': listed[e+1:]})

     def set_events(self, listed, a):
          b = listed.index('Memory initiatives')
          for event in listed[a:b]:
                 year_event = event.split('-')
                 self.timeline.update({year_event[1]:year_event[0]})
          return b

     def set_meminit(self, listed, b):
          c = listed.index('Sites of memory')
          for i in listed[b:c]:
               self.set_memdates(i)
          return c

     def set_memdates(self, strg):
            topic_summ = strg.split(':')
            self.meminit.update({topic_summ[0]: topic_summ[1]})

     def set_sites(self, listed, c):
          d = listed.index('Organisations')
          for i in listed[c:d]:
               self.set_sitesinfo(i)
          return d
     
     def set_sitesinfo(self, strg):
            topic_summ = strg.split(':')
            self.sites.update({topic_summ[0]: topic_summ[1]})
    
     def set_orgs(self, listed, c):
          d = listed.index('Issues specific to the country')
          for i in listed[c:d]:
               self.set_orgsinfo(i)
          return d

     def set_orgsinfo(self, strg):
            topic_summ = strg.split(':')
            self.orgs.update({topic_summ[0]: topic_summ[1]})

     def set_dates(self, strg):
            strg = strg.lower().strip()
            topic_date = strg.split('(')
            topics = topic_date[0].replace('and', ',')
            topics = topics.split(',')
            date = topic_date[1].replace(')', '')
            date = date.split('-')
            start = date[0][0:4]
            if(not date[1] == ''):
                end = date[1].strip()
            else:
                end = '2023'
            self.table.update({'Topics':topics})
            self.table.update({'Start': int(start)})
            self.table.update({'End': int(end)})

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
     
     def add_country(self):
          self.table.update({'Events': self.get_time()})
          self.table.update({'Memory Inititives': self.get_mem()})
          self.table.update({'Sites of Memory': self.get_memsites()})
          self.table.update({'Organizations': self.get_orgs()})
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

def main():
    folder_name = 'Countries'
    country_dicts = []
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
 
        #https://docs.python.org/3/library/csv.html
        south_america = open('12countries.csv', 'w', newline = '')
        fieldnames = ['Country', 'Topics', 'Start', 'End', 'Categories', 'Actors', 'Summary', 'Issues specific to the country', 'Events', 'Memory Inititives', 'Sites of Memory', 'Organizations']
        writer = csv.DictWriter(south_america, fieldnames = fieldnames)
        writer.writeheader()
        for table in country_dicts:
             writer.writerow(table)

main()