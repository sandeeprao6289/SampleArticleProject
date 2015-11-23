import csv


def import_csv():
    
    with open('static/articles.csv', 'w') as csvfile:
        rows = csv.DictReader(csvfile)
        
        for row in rows:
            print "++++++++++",row,"+++++++++++++"
            
import_csv()