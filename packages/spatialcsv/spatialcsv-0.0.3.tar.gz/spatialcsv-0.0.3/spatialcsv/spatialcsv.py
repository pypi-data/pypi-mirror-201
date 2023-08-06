"""Main module."""
import pandas as pd
import csv


#def import_csv(filepath, skip=none, delimiters=','):
 #   pass



class Locations:
    """Inputs a csv with locational data and outputs the proper format to import into a webmap"""

    def __init__(self, csv, lat=None, long=None, **kwargs):
        """
        Keyword arguments:
        csv -- the filepath to the csv file. It is assumed that the delimiter is ','
        lat -- the column header name of the latitude values
        long -- the column header name of the longitude values
        """
        self.csv = csv
        self.lat = lat
        self.long = long


    def checks(self):
        """
        Checks to make sure file exists, has a header, 
        the lat and long variables exist in the header
        """
        with open(self.csv, 'r') as csvfile:
            head = csv.Sniffer().has_header(csvfile.read(1024))
                
            if head:
                pass
            else:
                print("This csv file does not seem to have a header. Please add column names in the top line of the csv.")
        
        # add exception  FileNotFoundError:
        
        if self.lat in self.header():
            pass
        else:
            print(f"The value '{self.lat}' is not in the header.")
        if self.long in self.header():
            pass
        else:
            print(f"The value '{self.long}' is not in the header.")
        print("done")


    def header(self):
        """Returns header row"""
        with open(self.csv) as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            print(list(header))
            return header



