import sqlite3
import os
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__, static_folder='.', static_url_path='')

# Google OAuth Credentials
GOOGLE_CLIENT_ID = "937984856077-9uk43pn7ljstlpstp0261j95mnfmq6qi.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Contact form submissions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            family_name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Google users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_email TEXT UNIQUE,
            name TEXT,
            picture TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price TEXT,
            old_price TEXT,
            image_url TEXT,
            badge TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Seed initial products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        initial_products = [
            ("Yangi qulupnay", "Mevalar", "45 000 so'm", "55 000", "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=400&h=300", "-18%"),
            ("Anor", "Mevalar", "35 000 so'm", "", "https://images.unsplash.com/photo-1528659556-91e84a2c5a08?auto=format&fit=crop&w=400&h=300", ""),
            ("Yashil olma", "Mevalar", "15 000 so'm", "", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?auto=format&fit=crop&w=400&h=300", ""),
            ("Avokado", "Sabzavotlar", "65 000 so'm", "", "https://images.unsplash.com/photo-1518349586146-2cb634358a9e?auto=format&fit=crop&w=400&h=300", ""),
            ("Fransuz kruassani", "Pishiriqlar", "20 000 so'm", "", "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&h=300", "Yangi"),
            ("Tost noni", "Pishiriqlar", "12 000 so'm", "", "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&h=300", ""),
            ("Keks", "Pishiriqlar", "30 000 so'm", "35 000", "https://images.unsplash.com/photo-1550617931-e17a7b70dce2?auto=format&fit=crop&w=400&h=300", "Aksiya"),
            ("Sariyog'", "Sut mahsulotlari", "45 000 so'm", "", "https://images.unsplash.com/photo-1588195538320-0624bb181057?auto=format&fit=crop&w=400&h=300", ""),
            ("Limon", "Mevalar", "25 000 so'm", "", "https://images.unsplash.com/photo-1556881286-fc6915169721?auto=format&fit=crop&w=400&h=300", ""),
            ("Gilos", "Mevalar", "50 000 so'm", "60 000", "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=400&h=300", "-15%"),
            ("Brokkoli", "Sabzavotlar", "22 000 so'm", "", "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?auto=format&fit=crop&w=400&h=300", ""),
            ("Apelsin sharbati", "Ichimliklar", "28 000 so'm", "", "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=400&h=300", ""),
            ("Pomidor", "Sabzavotlar", "18 000 so'm", "", "https://images.unsplash.com/photo-1592924357228-91a4daadcfe1?auto=format&fit=crop&w=400&h=300", ""),
            ("Tarvuz", "Mevalar", "30 000 so'm", "", "https://images.unsplash.com/photo-1563114773-86cd262f3b79?auto=format&fit=crop&w=400&h=300", "Yangi"),
            ("Non", "Pishiriqlar", "5 000 so'm", "", "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&h=300", ""),
            ("Salat bargi", "Sabzavotlar", "10 000 so'm", "", "https://images.unsplash.com/photo-1622206151226-18ca2c9ea900?auto=format&fit=crop&w=400&h=300", ""),
        ]
        cursor.executemany('''
            INSERT INTO products (name, category, price, old_price, image_url, badge)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', initial_products)

    conn.commit()
    conn.close()

init_db()

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/register.html')
def serve_register():
    return send_from_directory('.', 'register.html')

@app.route('/blog.html')
def serve_blog():
    return send_from_directory('.', 'blog.html')

@app.route('/products.html')
def serve_products():
    return send_from_directory('.', 'products.html')

@app.route('/admin.html')
def serve_admin():
    return send_from_directory('.', 'admin.html')

@app.route('/static/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# API endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        products.append({
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3],
            'old_price': row[4],
            'image_url': row[5],
            'badge': row[6]
        })
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Ma\'lumot yuborilmadi'}), 400
            
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, category, price, old_price, image_url, badge)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['category'], data['price'], data.get('old_price', ''), data['image_url'], data.get('badge', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Product add error: {e}")
        return jsonify({'error': str(e)}), 500

from werkzeug.utils import secure_filename

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Fayl tanlanmagan'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Fayl nomi bo\'sh'}), 400
        
        filename = secure_filename(file.filename)
        # Ensure filename is unique to avoid overwriting
        import time
        filename = f"{int(time.time())}_{filename}"
        
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'url': f'/static/uploads/{filename}'})
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (first_name, last_name, family_name, email, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['firstName'], data['lastName'], data['familyName'], data['email'], data['message']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (google_email, name, picture) VALUES (?, ?, ?)',
                   (data['email'], data['name'], data['picture']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    print("Menga Uzum Market serveri ishga tushdi!")
    print("Brauzeringizda ushbu manzilga kiring: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
