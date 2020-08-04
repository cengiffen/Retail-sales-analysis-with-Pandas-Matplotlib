import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter


# to see all columns with .head() while testing
pd.set_option('display.max_columns', None)

sales_data = pd.read_csv('grocery_retail_data_2016_2019.csv')

'''
Q1. What is the best month for sales?
'''
sales_data['DATENEW'] = pd.to_datetime(sales_data['DATENEW'])
sales_data['Month'] = sales_data['DATENEW'].dt.month
sales_data['Sales'] = sales_data['UNITS'] * sales_data['PRICE']

total_sales = sales_data.groupby('Month').sum()['Sales']
months = range(1, 13)

plt.bar(months, total_sales)
plt.xticks(months)
plt.ylabel('Sales in $')
plt.xlabel('Month')
plt.show()
'''
Plot shows a sales peak during July&August - in summer.
'''
'''
Q2. What is the best time for advertisement?
'''
sales_data['Hour'] = sales_data['DATENEW'].dt.hour
hour_count = sales_data.groupby('Hour').count()

hours = [hour for hour, df in sales_data.groupby('Hour')]

plt.plot(hours, hour_count)
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Transactions')
plt.grid()
plt.show()
'''
Plot shows a great peak during 11 am and also a peak on 00 am (midnight).
Advertisements can be put on 1-2 hours before these peaks.
'''
'''
Q3. What are the products that most often sold together?
'''
df = sales_data[sales_data['TICKET'].duplicated(keep=False)]

df['Grouped'] = df.groupby('TICKET')['NAME'].transform(lambda x: ','.join(x))
df = df[['TICKET', 'Grouped']].drop_duplicates()

count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)

'''
- 10 most common 2 items that are sold together:

('Field Tomatoes', 'Banana Cavendish') 6412
('Mandarin Imperial', 'Banana Cavendish') 4204
('Apples Pink Lady', 'Banana Cavendish') 3741
('Capsicum red', 'Banana Cavendish') 3664
('Broccoli', 'Banana Cavendish') 3546
('Pear Packham', 'Banana Cavendish') 3522
('Watermelon seedless', 'Banana Cavendish') 3520
('Cucumber Lebanese', 'Banana Cavendish') 3443
('Potato sweet Gold', 'Banana Cavendish') 2990
('Zucchini green', 'Banana Cavendish') 2776

We see that Banana Cavendish and Field Tomatoes are sold with big quantities,
so in order to get a valuable information regarding bundles, I will perform the function
for 4 items that are sold together the most.
We could also filter out those common items.
'''

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 4)))

for key, value in count.most_common(10):
    print(key, value)
'''
- 10 most common 4 items that are sold together:
('Mark down Bag ***', 'Mark down Bag ***', 'Mark down Bag ***', 'Mark down Bag ***') 814
('Mark down Bag ***', 'Mark down Bag ***', 'Mark down Bag ***', 'Banana Cavendish') 426
('Capsicum red', 'Broccoli', 'Field Tomatoes', 'Banana Cavendish') 304
('Broccoli', 'Beans green', 'Field Tomatoes', 'Banana Cavendish') 264
('Broccoli', 'Pear Packham', 'Field Tomatoes', 'Banana Cavendish') 260
('Broccoli', 'Carrots ', 'Field Tomatoes', 'Banana Cavendish') 251
('Potato sweet Gold', 'Broccoli', 'Field Tomatoes', 'Banana Cavendish') 249
('Capsicum red', 'Zucchini green', 'Field Tomatoes', 'Banana Cavendish') 243
('Broccoli', 'Zucchini green', 'Field Tomatoes', 'Banana Cavendish') 242
('Capsicum red', 'Broccoli', 'Zucchini green', 'Banana Cavendish') 239
'''
'''
Q4. What is the most sold product?
'''
product_group = sales_data.groupby('CATERGORY')
products = [product for product, df in product_group]
unit_purchased = product_group.sum()['UNITS']
prices = sales_data.groupby('CATERGORY').mean()['PRICE']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, unit_purchased)
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Category')
ax2.set_ylabel('Price', color='b')
ax1.set_ylabel('Unit Purchased', color='g')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()
'''
I am creating a bar chart for the product categories (there are too many unique products to have an isolated insight),
and on top of it putting a price plot to see the relation with the prices.
Data shows a clear correlation for the most product categories.
'''