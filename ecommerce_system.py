import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class EcommerceManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Ecommerce Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        self.init_database()
        self.create_gui()
        self.load_products()
        self.load_orders()
        self.load_customers()

    def init_database(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Rish@lv1073',  # <-- Your password here
                database='ecommercemanagment'
            )
            self.cursor = self.conn.cursor(buffered=True)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
            self.root.destroy()
            return

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price FLOAT NOT NULL,
                stock INT NOT NULL,
                description TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(30),
                address TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT,
                product_id INT,
                quantity INT,
                total_price FLOAT,
                order_date DATETIME,
                status VARCHAR(50),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        self.cursor.execute("SELECT COUNT(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            self.insert_sample_data()

        self.conn.commit()

    def insert_sample_data(self):
        products = [
            ('Laptop', 'Electronics', 999.99, 50, 'High-performance laptop'),
            ('Smartphone', 'Electronics', 699.99, 100, 'Latest smartphone'),
            ('T-Shirt', 'Clothing', 19.99, 200, 'Cotton t-shirt'),
            ('Coffee Mug', 'Home', 9.99, 150, 'Ceramic coffee mug'),
            ('Book', 'Education', 29.99, 80, 'Programming book')
        ]
        customers = [
            ('John Doe', 'john@email.com', '123-456-7890', '123 Main St'),
            ('Jane Smith', 'jane@email.com', '098-765-4321', '456 Oak Ave')
        ]
        self.cursor.executemany('''
            INSERT INTO products (name, category, price, stock, description)
            VALUES (%s, %s, %s, %s, %s)
        ''', products)
        self.cursor.executemany('''
            INSERT INTO customers (name, email, phone, address)
            VALUES (%s, %s, %s, %s)
        ''', customers)
        self.conn.commit()

    def create_gui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.products_frame = ttk.Frame(self.notebook)
        self.orders_frame = ttk.Frame(self.notebook)
        self.customers_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        self.notebook.add(self.products_frame, text='Products')
        self.notebook.add(self.orders_frame, text='Orders')
        self.notebook.add(self.customers_frame, text='Customers')
        self.setup_dashboard()
        self.setup_products_tab()
        self.setup_orders_tab()
        self.setup_customers_tab()

    def setup_dashboard(self):
        title_label = tk.Label(self.dashboard_frame, text="Ecommerce Dashboard",
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        stats_frame = tk.Frame(self.dashboard_frame, bg='#f0f0f0')
        stats_frame.pack(pady=20)
        total_products = self.get_statistic("SELECT COUNT(*) FROM products")
        total_customers = self.get_statistic("SELECT COUNT(*) FROM customers")
        total_orders = self.get_statistic("SELECT COUNT(*) FROM orders")
        total_revenue = self.get_statistic("SELECT SUM(total_price) FROM orders") or 0
        stats_data = [
            ("Total Products", total_products, "#4CAF50"),
            ("Total Customers", total_customers, "#2196F3"),
            ("Total Orders", total_orders, "#FF9800"),
            ("Total Revenue", f"${total_revenue:.2f}", "#F44336")
        ]
        for i, (label, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(stats_frame, bg=color, relief='raised', bd=1)
            stat_frame.grid(row=0, column=i, padx=10, pady=10, ipadx=20, ipady=10)
            value_label = tk.Label(stat_frame, text=str(value), font=('Arial', 14, 'bold'), bg=color, fg='white')
            value_label.pack()
            label_label = tk.Label(stat_frame, text=label, font=('Arial', 10), bg=color, fg='white')
            label_label.pack()

    def get_statistic(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def setup_products_tab(self):
        left_frame = tk.Frame(self.products_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        tk.Label(left_frame, text="Product List", font=('Arial', 12, 'bold')).pack(anchor='w')
        self.products_tree = ttk.Treeview(left_frame, columns=('ID', 'Name', 'Category', 'Price', 'Stock'), show='headings')
        self.products_tree.heading('ID', text='ID')
        self.products_tree.heading('Name', text='Name')
        self.products_tree.heading('Category', text='Category')
        self.products_tree.heading('Price', text='Price')
        self.products_tree.heading('Stock', text='Stock')
        self.products_tree.column('ID', width=50)
        self.products_tree.column('Name', width=150)
        self.products_tree.column('Category', width=100)
        self.products_tree.column('Price', width=80)
        self.products_tree.column('Stock', width=80)
        self.products_tree.pack(fill='both', expand=True)
        right_frame = tk.Frame(self.products_frame)
        right_frame.pack(side='right', fill='y', padx=5, pady=5)
        tk.Label(right_frame, text="Add/Edit Product", font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        form_frame = tk.Frame(right_frame)
        form_frame.pack(fill='x', pady=5)
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.product_name = tk.Entry(form_frame, width=20)
        self.product_name.grid(row=0, column=1, pady=2)
        tk.Label(form_frame, text="Category:").grid(row=1, column=0, sticky='w', pady=2)
        self.product_category = tk.Entry(form_frame, width=20)
        self.product_category.grid(row=1, column=1, pady=2)
        tk.Label(form_frame, text="Price:").grid(row=2, column=0, sticky='w', pady=2)
        self.product_price = tk.Entry(form_frame, width=20)
        self.product_price.grid(row=2, column=1, pady=2)
        tk.Label(form_frame, text="Stock:").grid(row=3, column=0, sticky='w', pady=2)
        self.product_stock = tk.Entry(form_frame, width=20)
        self.product_stock.grid(row=3, column=1, pady=2)
        tk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky='w', pady=2)
        self.product_description = tk.Text(form_frame, width=20, height=4)
        self.product_description.grid(row=4, column=1, pady=2)
        button_frame = tk.Frame(right_frame)
        button_frame.pack(fill='x', pady=10)
        tk.Button(button_frame, text="Add Product", command=self.add_product, bg='#4CAF50', fg='white').pack(fill='x', pady=2)
        tk.Button(button_frame, text="Update Product", command=self.update_product, bg='#2196F3', fg='white').pack(fill='x', pady=2)
        tk.Button(button_frame, text="Delete Product", command=self.delete_product, bg='#f44336', fg='white').pack(fill='x', pady=2)
        tk.Button(button_frame, text="Clear Form", command=self.clear_product_form, bg='#FF9800', fg='white').pack(fill='x', pady=2)
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)

    def setup_orders_tab(self):
        tk.Label(self.orders_frame, text="Order List", font=('Arial', 12, 'bold')).pack(anchor='w')
        self.orders_tree = ttk.Treeview(self.orders_frame, columns=('ID', 'Customer', 'Product', 'Quantity', 'Total', 'Date', 'Status'), show='headings')
        self.orders_tree.heading('ID', text='Order ID')
        self.orders_tree.heading('Customer', text='Customer')
        self.orders_tree.heading('Product', text='Product')
        self.orders_tree.heading('Quantity', text='Qty')
        self.orders_tree.heading('Total', text='Total')
        self.orders_tree.heading('Date', text='Date')
        self.orders_tree.heading('Status', text='Status')
        self.orders_tree.pack(fill='both', expand=True, padx=5, pady=5)
        order_button_frame = tk.Frame(self.orders_frame)
        order_button_frame.pack(fill='x', pady=5)
        tk.Button(order_button_frame, text="Create New Order", command=self.create_order_window, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(order_button_frame, text="Update Status", command=self.update_order_status, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(order_button_frame, text="Delete Order", command=self.delete_order, bg='#f44336', fg='white').pack(side='left', padx=5)

    def setup_customers_tab(self):
        left_frame = tk.Frame(self.customers_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        tk.Label(left_frame, text="Customer List", font=('Arial', 12, 'bold')).pack(anchor='w')
        self.customers_tree = ttk.Treeview(left_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Address'), show='headings')
        self.customers_tree.heading('ID', text='ID')
        self.customers_tree.heading('Name', text='Name')
        self.customers_tree.heading('Email', text='Email')
        self.customers_tree.heading('Phone', text='Phone')
        self.customers_tree.heading('Address', text='Address')
        self.customers_tree.column('ID', width=50)
        self.customers_tree.column('Name', width=150)
        self.customers_tree.column('Email', width=150)
        self.customers_tree.column('Phone', width=100)
        self.customers_tree.column('Address', width=200)
        self.customers_tree.pack(fill='both', expand=True)

        right_frame = tk.Frame(self.customers_frame)
        right_frame.pack(side='right', fill='y', padx=5, pady=5)
        tk.Label(right_frame, text="Add/Edit Customer", font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        form_frame = tk.Frame(right_frame)
        form_frame.pack(fill='x', pady=5)
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.customer_name = tk.Entry(form_frame, width=20)
        self.customer_name.grid(row=0, column=1, pady=2)
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky='w', pady=2)
        self.customer_email = tk.Entry(form_frame, width=20)
        self.customer_email.grid(row=1, column=1, pady=2)
        tk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky='w', pady=2)
        self.customer_phone = tk.Entry(form_frame, width=20)
        self.customer_phone.grid(row=2, column=1, pady=2)
        tk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky='w', pady=2)
        self.customer_address = tk.Entry(form_frame, width=20)
        self.customer_address.grid(row=3, column=1, pady=2)

        button_frame = tk.Frame(right_frame)
        button_frame.pack(fill='x', pady=10)
        tk.Button(button_frame, text="Add Customer", command=self.add_customer, bg='#4CAF50', fg='white').pack(fill='x', pady=2)
        tk.Button(button_frame, text="Update Customer", command=self.update_customer, bg='#2196F3', fg='white').pack(fill='x', pady=2)
        tk.Button(button_frame, text="Delete Customer", command=self.delete_customer, bg='#f44336', fg='white').pack(fill='x', pady=2)
        tk.Button(button_frame, text="Clear Form", command=self.clear_customer_form, bg='#FF9800', fg='white').pack(fill='x', pady=2)
        self.customers_tree.bind('<<TreeviewSelect>>', self.on_customer_select)

    def load_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        self.cursor.execute("SELECT * FROM products")
        for product in self.cursor.fetchall():
            self.products_tree.insert('', 'end', values=product)

    def load_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        self.cursor.execute('''
            SELECT o.id, c.name, p.name, o.quantity, o.total_price, o.order_date, o.status
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN products p ON o.product_id = p.id
        ''')
        for order in self.cursor.fetchall():
            self.orders_tree.insert('', 'end', values=order)

    def load_customers(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        self.cursor.execute("SELECT * FROM customers")
        for customer in self.cursor.fetchall():
            self.customers_tree.insert('', 'end', values=customer)

    def add_customer(self):
        try:
            name = self.customer_name.get()
            email = self.customer_email.get()
            phone = self.customer_phone.get()
            address = self.customer_address.get()
            if not name or not email:
                messagebox.showerror("Error", "Name and email are required!")
                return
            self.cursor.execute('''
                INSERT INTO customers (name, email, phone, address)
                VALUES (%s, %s, %s, %s)
            ''', (name, email, phone, address))
            self.conn.commit()
            self.load_customers()
            self.clear_customer_form()
            messagebox.showinfo("Success", "Customer added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a customer to update!")
            return
        customer_id = self.customers_tree.item(selected[0])['values'][0]
        try:
            name = self.customer_name.get()
            email = self.customer_email.get()
            phone = self.customer_phone.get()
            address = self.customer_address.get()
            self.cursor.execute('''
                UPDATE customers
                SET name=%s, email=%s, phone=%s, address=%s
                WHERE id=%s
            ''', (name, email, phone, address, customer_id))
            self.conn.commit()
            self.load_customers()
            messagebox.showinfo("Success", "Customer updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a customer to delete!")
            return
        customer_id = self.customers_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            self.cursor.execute("DELETE FROM customers WHERE id=%s", (customer_id,))
            self.conn.commit()
            self.load_customers()
            self.clear_customer_form()
            messagebox.showinfo("Success", "Customer deleted successfully!")

    def clear_customer_form(self):
        self.customer_name.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)
        self.customer_address.delete(0, tk.END)

    def on_customer_select(self, event):
        selected = self.customers_tree.selection()
        if selected:
            customer_data = self.customers_tree.item(selected[0])['values']
            self.clear_customer_form()
            self.customer_name.insert(0, customer_data[1])
            self.customer_email.insert(0, customer_data[2])
            self.customer_phone.insert(0, customer_data[3])
            self.customer_address.insert(0, customer_data[4] if len(customer_data) > 4 else "")

    # Product functions (from before, unchanged except for possible bugfixes)
    def add_product(self):
        try:
            name = self.product_name.get()
            category = self.product_category.get()
            price = float(self.product_price.get())
            stock = int(self.product_stock.get())
            description = self.product_description.get("1.0", tk.END).strip()
            if not name or not category:
                messagebox.showerror("Error", "Name and category are required!")
                return
            self.cursor.execute('''
                INSERT INTO products (name, category, price, stock, description)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, category, price, stock, description))
            self.conn.commit()
            self.load_products()
            self.clear_product_form()
            messagebox.showinfo("Success", "Product added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and stock values!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to update!")
            return
        try:
            product_id = self.products_tree.item(selected[0])['values'][0]
            name = self.product_name.get()
            category = self.product_category.get()
            price = float(self.product_price.get())
            stock = int(self.product_stock.get())
            description = self.product_description.get("1.0", tk.END).strip()
            self.cursor.execute('''
                UPDATE products 
                SET name=%s, category=%s, price=%s, stock=%s, description=%s
                WHERE id=%s
            ''', (name, category, price, stock, description, product_id))
            self.conn.commit()
            self.load_products()
            messagebox.showinfo("Success", "Product updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and stock values!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            product_id = self.products_tree.item(selected[0])['values'][0]
            self.cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
            self.conn.commit()
            self.load_products()
            self.clear_product_form()
            messagebox.showinfo("Success", "Product deleted successfully!")

    def clear_product_form(self):
        self.product_name.delete(0, tk.END)
        self.product_category.delete(0, tk.END)
        self.product_price.delete(0, tk.END)
        self.product_stock.delete(0, tk.END)
        self.product_description.delete("1.0", tk.END)

    def on_product_select(self, event):
        selected = self.products_tree.selection()
        if selected:
            product_data = self.products_tree.item(selected[0])['values']
            self.clear_product_form()
            self.product_name.insert(0, product_data[1])
            self.product_category.insert(0, product_data[2])
            self.product_price.insert(0, str(product_data[3]))
            self.product_stock.insert(0, str(product_data[4]))
            self.product_description.insert("1.0", product_data[5] if len(product_data) > 5 else "")

    # Orders tab functions (unchanged from before)
    def create_order_window(self):
        order_window = tk.Toplevel(self.root)
        order_window.title("Create New Order")
        order_window.geometry("400x300")
        tk.Label(order_window, text="Customer:").pack(anchor='w', pady=5)
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(order_window, textvariable=customer_var, state='readonly')
        self.cursor.execute("SELECT id, name FROM customers")
        customers = self.cursor.fetchall()
        customer_combo['values'] = [f"{cust[0]} - {cust[1]}" for cust in customers]
        customer_combo.pack(fill='x', pady=5)
        tk.Label(order_window, text="Product:").pack(anchor='w', pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(order_window, textvariable=product_var, state='readonly')
        self.cursor.execute("SELECT id, name, price, stock FROM products")
        products = self.cursor.fetchall()
        product_combo['values'] = [f"{prod[0]} - {prod[1]} (${prod[2]}) - Stock: {prod[3]}" for prod in products]
        product_combo.pack(fill='x', pady=5)
        tk.Label(order_window, text="Quantity:").pack(anchor='w', pady=5)
        quantity_entry = tk.Entry(order_window)
        quantity_entry.pack(fill='x', pady=5)
        def create_order():
            try:
                customer_id = int(customer_var.get().split(' - ')[0])
                product_id = int(product_var.get().split(' - ')[0])
                quantity = int(quantity_entry.get())
                self.cursor.execute("SELECT price, stock FROM products WHERE id=%s", (product_id,))
                product_data = self.cursor.fetchone()
                if not product_data:
                    messagebox.showerror("Error", "Product not found!")
                    return
                price, stock = product_data
                if quantity > stock:
                    messagebox.showerror("Error", f"Insufficient stock! Available: {stock}")
                    return
                total_price = price * quantity
                self.cursor.execute('''
                    INSERT INTO orders (customer_id, product_id, quantity, total_price, order_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (customer_id, product_id, quantity, total_price,
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Pending"))
                self.cursor.execute("UPDATE products SET stock = stock - %s WHERE id=%s", (quantity, product_id))
                self.conn.commit()
                self.load_orders()
                self.load_products()
                order_window.destroy()
                messagebox.showinfo("Success", "Order created successfully!")
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Please fill all fields correctly!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        tk.Button(order_window, text="Create Order", command=create_order, bg='#4CAF50', fg='white').pack(pady=10)

    def update_order_status(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order!")
            return
        order_id = self.orders_tree.item(selected[0])['values'][0]
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Order Status")
        status_window.geometry("300x150")
        tk.Label(status_window, text="Select new status:").pack(pady=10)
        status_var = tk.StringVar(value="Pending")
        status_combo = ttk.Combobox(status_window, textvariable=status_var,
                                   values=["Pending", "Processing", "Shipped", "Delivered", "Cancelled"])
        status_combo.pack(pady=10)
        def update_status():
            self.cursor.execute("UPDATE orders SET status=%s WHERE id=%s", (status_var.get(), order_id))
            self.conn.commit()
            self.load_orders()
            status_window.destroy()
            messagebox.showinfo("Success", "Order status updated!")
        tk.Button(status_window, text="Update Status", command=update_status).pack(pady=10)

    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order to delete!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this order?"):
            order_id = self.orders_tree.item(selected[0])['values'][0]
            self.cursor.execute("SELECT product_id, quantity FROM orders WHERE id=%s", (order_id,))
            order_data = self.cursor.fetchone()
            if order_data:
                product_id, quantity = order_data
                self.cursor.execute("UPDATE products SET stock = stock + %s WHERE id=%s", (quantity, product_id))
            self.cursor.execute("DELETE FROM orders WHERE id=%s", (order_id,))
            self.conn.commit()
            self.load_orders()
            self.load_products()
            messagebox.showinfo("Success", "Order deleted successfully!")

def main():
    root = tk.Tk()
    app = EcommerceManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
