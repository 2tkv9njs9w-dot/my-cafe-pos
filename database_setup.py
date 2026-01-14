import sqlite3

def init_db():
    conn = sqlite3.connect('cafe_pos.db')
    cursor = conn.cursor()

    # ສ້າງຕາຕະລາງພະນັກງານ
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')

    # ສ້າງຕາຕະລາງສິນຄ້າ
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, category TEXT, image_url TEXT)''')

    # ສ້າງຕາຕະລາງເກັບຍອດຂາຍ (Orders)
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, total_price REAL, order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # ເພີ່ມ User Admin
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', '123', 'admin')")
    
    # ລາຍການສິນຄ້າ (ກວດຊື່ຮູບໃນໂຟນເດີ images ໃຫ້ກົງກັບບ່ອນນີ້ເດີ້)
    products_to_add = [
        ('Espresso', 15000, 'Coffee', 'hot_espresso.jpg'),
        ('Iced Coffee', 25000, 'Coffee', 'iced_coffee.jpg'),
        ('Latte', 25000, 'Coffee', 'latte.jpg'),
        ('Capuccino', 20000, 'Coffee', 'capuccino.jpg')
    ]

    for p in products_to_add:
        cursor.execute("INSERT OR IGNORE INTO products (name, price, category, image_url) VALUES (?, ?, ?, ?)", p)

    conn.commit()
    conn.close()
    print("--- 1. ສ້າງ Database ສຳເລັດແລ້ວ! ---")

if __name__ == '__main__':
    init_db()