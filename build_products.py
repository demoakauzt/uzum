with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

header = []
footer = []
in_footer = False

for line in lines:
    header.append(line)
    if '</header>' in line:
        break

# Optional: Set active state if needed (there's no specific 'Mahsulotlar' link in the top nav right now, but we can just use the header)
header_str = ''.join(header)
header_str = header_str.replace('<title>Menga Uzum Market</title>', '<title>Mahsulotlar - Menga Uzum Market</title>')

for line in reversed(lines):
    footer.insert(0, line)
    if '<footer' in line:
        break

products_content = '''
    <style>
        .products-hero {
            text-align: center;
            padding: 80px 20px 40px;
            background: #f4f9fc;
        }
        .products-title {
            font-size: 3.5rem;
            color: #0b2c24;
            font-weight: 300;
            margin-bottom: 20px;
        }
        .products-subtitle {
            color: #555;
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .products-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        
        .filters {
            display: flex;
            gap: 15px;
            margin-bottom: 40px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .filter-btn {
            background: white;
            border: 1px solid #e1efe6;
            padding: 8px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            color: #555;
            transition: all 0.3s ease;
        }
        .filter-btn:hover, .filter-btn.active {
            background: #004532;
            color: white;
            border-color: #004532;
        }
        
        .products-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
        }
        
        .product-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .p-image-wrapper {
            position: relative;
            height: 200px;
            overflow: hidden;
            background: #f8f8f8;
        }
        .p-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        .product-card:hover .p-image {
            transform: scale(1.05);
        }
        
        .p-badge {
            position: absolute;
            top: 15px;
            left: 15px;
            background: #ff4757;
            color: white;
            padding: 4px 10px;
            font-size: 0.7rem;
            border-radius: 4px;
            font-weight: 600;
        }
        
        .p-info {
            padding: 20px;
        }
        .p-category {
            color: #888;
            font-size: 0.8rem;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .p-name {
            color: #0b2c24;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .p-price-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .p-price {
            font-size: 1.3rem;
            font-weight: 700;
            color: #004532;
        }
        .p-old-price {
            text-decoration: line-through;
            color: #999;
            font-size: 0.9rem;
            margin-left: 10px;
        }
        
        .add-to-cart {
            width: 100%;
            padding: 12px;
            background: #f4f9fc;
            color: #004532;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .add-to-cart:hover {
            background: #004532;
            color: white;
        }

        @media (max-width: 992px) {
            .products-grid { grid-template-columns: repeat(3, 1fr); }
        }
        @media (max-width: 768px) {
            .products-grid { grid-template-columns: repeat(2, 1fr); }
            .products-title { font-size: 2.5rem; }
        }
        @media (max-width: 480px) {
            .products-grid { grid-template-columns: 1fr; }
        }
    </style>

    <main style="padding-top: 80px;">
        <section class="products-hero">
            <h1 class="products-title">Barcha Mahsulotlar</h1>
            <p class="products-subtitle">Eng yangi va sifatli mahsulotlarni toping. Har kuni yangilanadigan keng tanlov.</p>
        </section>

        <section class="products-container">
            <div class="filters">
                <button class="filter-btn active">Barchasi</button>
                <button class="filter-btn">Sabzavotlar</button>
                <button class="filter-btn">Mevalar</button>
                <button class="filter-btn">Pishiriqlar</button>
                <button class="filter-btn">Ichimliklar</button>
            </div>

            <div class="products-grid">
                <!-- Products will be generated below -->
'''

# List of high quality unspalsh ids for products
products = [
    {"name": "Yangi qulupnay", "cat": "Mevalar", "price": "45 000 so'm", "old": "55 000", "img": "1519999482648-25049ddd37b1", "badge": "-18%"},
    {"name": "Anor", "cat": "Mevalar", "price": "35 000 so'm", "img": "1615486171545-9279a013f9c6"},
    {"name": "Yashil olma", "cat": "Mevalar", "price": "15 000 so'm", "img": "1568702846914-96b305d2aaeb"},
    {"name": "Avokado", "cat": "Sabzavotlar", "price": "65 000 so'm", "img": "1523049673857-eb18f1d7b546"},
    
    {"name": "Fransuz kruassani", "cat": "Pishiriqlar", "price": "20 000 so'm", "img": "1555507036-ab1e4006aaeb", "badge": "Yangi"},
    {"name": "Tost noni", "cat": "Pishiriqlar", "price": "12 000 so'm", "img": "1598373182133-d4d547f38497"},
    {"name": "Keks", "cat": "Pishiriqlar", "price": "30 000 so'm", "old": "35 000", "img": "1550617931-e17a7b70dce2", "badge": "Aksiya"},
    {"name": "Sariyog'", "cat": "Sut mahsulotlari", "price": "45 000 so'm", "img": "1588195538320-0624bb181057"},
    
    {"name": "Limon", "cat": "Mevalar", "price": "25 000 so'm", "img": "1603569283847-3295e910af0f"},
    {"name": "Gilos", "cat": "Mevalar", "price": "50 000 so'm", "old": "60 000", "img": "1528821128474-27f963b062b2", "badge": "-15%"},
    {"name": "Brokkoli", "cat": "Sabzavotlar", "price": "22 000 so'm", "img": "1459411621453-7b03977f4bfc"},
    {"name": "Apelsin sharbati", "cat": "Ichimliklar", "price": "28 000 so'm", "img": "1600271886742-f049cd451bba"},
    
    {"name": "Pomidor", "cat": "Sabzavotlar", "price": "18 000 so'm", "img": "1592924357228-91a4daadcfe1"},
    {"name": "Tarvuz", "cat": "Mevalar", "price": "30 000 so'm", "img": "1563114773-86cd262f3b79", "badge": "Yangi"},
    {"name": "Non", "cat": "Pishiriqlar", "price": "5 000 so'm", "img": "1509440159596-0249088772ff"},
    {"name": "Salat bargi", "cat": "Sabzavotlar", "price": "10 000 so'm", "img": "1622206151226-18ca2c9ea900"},
]

for p in products:
    badge_html = f'<div class="p-badge">{p["badge"]}</div>' if "badge" in p else ''
    old_price_html = f'<span class="p-old-price">{p["old"]}</span>' if "old" in p else ''
    
    card = f'''
                <div class="product-card">
                    <div class="p-image-wrapper">
                        {badge_html}
                        <img src="https://images.unsplash.com/photo-{p["img"]}?auto=format&fit=crop&w=400&h=300" alt="{p["name"]}" class="p-image">
                    </div>
                    <div class="p-info">
                        <div class="p-category">{p["cat"]}</div>
                        <h3 class="p-name">{p["name"]}</h3>
                        <div class="p-price-row">
                            <div><span class="p-price">{p["price"]}</span>{old_price_html}</div>
                        </div>
                        <button class="add-to-cart"><i class="fas fa-shopping-cart"></i> Savatga qo'shish</button>
                    </div>
                </div>
    '''
    products_content += card

products_content += '''
            </div>
        </section>
    </main>
'''

with open('products.html', 'w', encoding='utf-8') as f:
    f.write(header_str + products_content + ''.join(footer))
