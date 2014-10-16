import csv
import sys

cash = sys.argv[1]
orders_csv = sys.argv[2]
values_csv = sys.argv[3]

with open(orders_csv, 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print row