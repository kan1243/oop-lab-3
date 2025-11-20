import csv, os
from pathlib import Path

class DataLoader:
    """Handles loading CSV data files."""
    
    def __init__(self, base_path=None):
        """Initialize the DataLoader with a base path for data files.
        """
        if base_path is None:
            self.base_path = Path(__file__).parent.resolve()
        else:
            self.base_path = Path(base_path)
    
    def load_csv(self, filename):
        """Load a CSV file and return its contents as a list of dictionaries.
        """
        filepath = self.base_path / filename
        data = []
        
        with filepath.open() as f:
            rows = csv.DictReader(f)
            for row in rows:
                data.append(dict(row))
        
        return data

class DB:
    def __init__(self):
        self.all_table = []


    def insert(self, data):
        self.all_table.append(data)


    def search(self, key):
        if key == 'cities':
            return self.all_table[0]
        elif key == 'countries':
            return self.all_table[1]
    

class Table:
    def __init__(self, name, data):
        self.table_name = name
        self.table = data

    def convert(self, text_to_convert):
        try:
            convert = float(text_to_convert)
        except:
            return text_to_convert
        else:
            return convert
        

    def filter(self, condition):
        req = [row for row in self.table if condition(row)]
        return Table(self.table_name, req)
    

    def aggregate(self, func, key):
        req = []
        for row in self.table:
            use_data = self.convert(row[key])
            req.append(use_data)
        return func(req)


    def join(self, object, key):
        joined_rows = []

        for row1 in self.table:
            for row2 in object.table:
                if row1[key] == row2[key]:
                    merged = {**row1,**row2}
                    joined_rows.append(merged)

        return Table(self.table_name + "_joined_" + object.table_name, joined_rows)            

    def __str__(self):
        return self.table_name + ':' + str(self.table)

loader = DataLoader()
cities = loader.load_csv('Cities.csv')
table1 = Table('cities', cities)
countries = loader.load_csv('Countries.csv')
table2 = Table('countries', countries)

my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)

my_table1 = my_DB.search('cities')
print("List all cities in Italy:") 
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
print(my_table1_filtered)
print()

print("Average temperature for all cities in Italy:")
print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
print()

my_table2 = my_DB.search('countries')
print("List all non-EU countries:") 
my_table2_filtered = my_table2.filter(lambda x: x['EU'] == 'no')
print(my_table2_filtered)
print()

print("Number of countries that have coastline:")
print(my_table2.filter(lambda x: x['coastline'] == 'yes').aggregate(lambda x: len(x), 'coastline'))
print()

my_table3 = my_table1.join(my_table2, 'country')
print("First 5 entries of the joined table (cities and countries):")
for item in my_table3.table[:5]:
    print(item)
print()

print("Cities whose temperatures are below 5.0 in non-EU countries:")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)
print()

print("The min and max temperatures for cities in EU countries that do not have coastlines")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
print()

