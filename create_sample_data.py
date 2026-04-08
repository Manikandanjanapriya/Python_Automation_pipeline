# create_sample_data.py -- Run this first!
import csv, random
from datetime import datetime, timedelta
products = ['Laptop','Mouse','Keyboard','Monitor',
 'Headphones','Webcam','USB Hub','SSD','Charger','Speaker']
salespeople = ['Alice','Bob','Carol','David','Eve']
rows = [['Date','Salesperson','Product','Units Sold','Unit Price','Revenue']]
start = datetime(2026, 1, 1)
for _ in range(100):
 date = start + timedelta(days=random.randint(0, 90))
 sp = random.choice(salespeople)
 prod = random.choice(products)
 units = random.randint(1, 20)
 price = round(random.uniform(15, 1200), 2)
 rev = round(units * price, 2)
 rows.append([date.strftime('%Y-%m-%d'), sp, prod, units, price, rev])
with open('sales_data.csv', 'w', newline='') as f:
 csv.writer(f).writerows(rows)
print('Created sales_data.csv with 100 rows.')