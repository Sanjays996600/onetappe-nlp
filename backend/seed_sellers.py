import sqlite3

conn = sqlite3.connect('/Users/sanjaysuman/One Tappe/OneTappeProject/backend/sellers.db')
cursor = conn.cursor()

# Insert dummy sellers
sellers = [
    (1, 'S. Power Works', 'electrician', '827001', '9am-6pm'),
    (2, 'R.K. Repair', 'electrician', '827001', '9am-6pm'),
    (3, 'Jha Electricals', 'electrician', '827001', '9am-6pm'),
    (4, 'Plumb Perfect', 'plumber', '827002', '9am-6pm')
]

cursor.executemany('INSERT OR REPLACE INTO sellers (id, name, category, pincode, business_hours) VALUES (?, ?, ?, ?, ?)', sellers)
conn.commit()
conn.close()