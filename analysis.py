import pandas as pd
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from connection import getconnection

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)

conn = getconnection()

query = """
SELECT o.*,
       c.customer_status,
       p.product_line, p.product_category, p.product_group, p.product_name,
       s.supplier_id, s.supplier_name, s.supplier_country
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON p.product_id = o.product_id
JOIN suppliers s ON s.supplier_id = p.supplier_id
"""

df = pd.read_sql(query, conn)
conn.close()

# date columns
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.to_period('M')
df['day'] = df['order_date'].dt.to_period('D')

# cost column
df['cost_buying_product'] = df['quantity_ordered'] * df['cost_price_per_unit']

formatter = mticker.FuncFormatter(lambda x, _x: f'{x:,.0f}')


# --- chart 1: total units sold per product category ---
total_units_sold = df.groupby('product_category')['quantity_ordered'].sum().sort_values(ascending=False).head(10)
total_units_sold.plot(kind='bar')
plt.xlabel('Product Category')
plt.ylabel('Units Sold')
plt.title('Total Units Sold For Each Product Category')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/01_total_units_sold.png', dpi=150)
plt.show()

# --- chart 2: total revenue per product ---
top_revenue_products = df.groupby('product_name')['total_retail_price'].sum().sort_values(ascending=False).head(20)
top_revenue_products.plot(kind='bar')
plt.xlabel('Product')
plt.ylabel('Total Revenue')
plt.title('Total Revenue Per Product')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/02_total_revenue_per_product.png', dpi=150)
plt.show()

# --- chart 3: monthly revenue 2017 ---
monthly_sales_2017 = df[df['order_date'].dt.year == 2017].groupby('month')['total_retail_price'].sum().sort_index()
monthly_sales_2017.plot(kind='line', marker='o')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.title('Total Revenue Per Month 2017')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/03_monthly_revenue_2017.png', dpi=150)
plt.show()

# --- chart 4: monthly revenue 2018 ---
monthly_sales_2018 = df[df['order_date'].dt.year == 2018].groupby('month')['total_retail_price'].sum().sort_index()
monthly_sales_2018.plot(kind='line', marker='o')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.title('Total Revenue Per Month 2018')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/04_monthly_revenue_2018.png', dpi=150)
plt.show()

# --- chart 5: total revenue by year ---
entire_sales_to_date = df.groupby(df['order_date'].dt.year)['total_retail_price'].sum().sort_index()
entire_sales_to_date.plot(kind='line', marker='o')
plt.xlabel('Year')
plt.ylabel('Total Revenue')
plt.title('Total Revenue To Date')
plt.xticks([2017, 2018, 2019, 2020, 2021])
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()
plt.savefig('charts/05_total_revenue_by_year.png', dpi=150)
plt.show()

# --- chart 6: most popular days of week to order ---
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_of_week_orders = df.groupby(df['order_date'].dt.day_name())['order_id'].count().reindex(day_order)
day_of_week_orders.plot(kind='bar')
plt.xlabel('Day of Week')
plt.ylabel('Total Orders')
plt.title('Most Popular Days to Order')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/06_orders_by_day_of_week.png', dpi=150)
plt.show()``

# --- chart 7: top 10 suppliers by spend ---
most_paid_supplier = df.groupby('supplier_name')['cost_buying_product'].sum().sort_values(ascending=False).head(10)
most_paid_supplier.plot(kind='bar')
plt.xlabel('Supplier')
plt.ylabel('Total Spent')
plt.title('Top 10 Suppliers We Spend On')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/07_top_suppliers_by_spend.png', dpi=150)
plt.show()

# --- chart 8: total products by supplier ---
total_products_supplier = df.groupby('supplier_name')['product_id'].count().sort_values(ascending=False).head(10)
total_products_supplier.plot(kind='bar')
plt.xlabel('Supplier')
plt.ylabel('Total Products')
plt.title('Total Products by Supplier')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/08_total_products_by_supplier.png', dpi=150)
plt.show()