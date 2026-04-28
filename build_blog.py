with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

header = []
footer = []
in_footer = False

for line in lines:
    header.append(line)
    if '</header>' in line:
        break

# Change active class for Blog in header
for i, line in enumerate(header):
    if 'class="nav-link">Blog' in line:
        header[i] = line.replace('href="#"', 'href="blog.html"').replace('nav-link', 'nav-link active')
    elif 'class="nav-link">Biz haqimizda' in line:
        pass
    elif 'href="blog.html"' in line:
        pass
    
# Add active state styles
header_str = ''.join(header)
header_str = header_str.replace('<title>Menga Uzum Market</title>', '<title>Blog - Menga Uzum Market</title>')

for line in reversed(lines):
    footer.insert(0, line)
    if '<footer' in line:
        break

blog_content = '''
    <style>
        .blog-hero {
            text-align: center;
            padding: 80px 20px 40px;
            background: white;
        }
        .icon-sparkle {
            color: #0d4a36;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .blog-title {
            font-size: 4rem;
            color: #0b2c24;
            font-weight: 300;
            line-height: 1.1;
            margin-bottom: 20px;
        }
        .blog-subtitle {
            color: #555;
            max-width: 600px;
            margin: 0 auto;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .blog-section {
            background-color: #f4f9fc;
            padding: 80px 20px;
            text-align: center;
        }
        .blog-section-label {
            color: #666;
            font-size: 0.8rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }
        .blog-section-title {
            color: #0b2c24;
            font-size: 3.5rem;
            font-weight: 300;
            margin-bottom: 10px;
        }
        .blog-section-subtitle {
            color: #555;
            margin-bottom: 30px;
        }
        
        .blog-btn-primary {
            background-color: #004532;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 50px;
            font-size: 1rem;
            cursor: pointer;
            margin-bottom: 60px;
            text-decoration: none;
            display: inline-block;
        }
        
        .blog-grid-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
            text-align: left;
        }
        
        .b-card {
            background: transparent;
        }
        
        .b-card-img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 15px;
        }
        
        .b-card-meta {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }
        
        .b-tag {
            background: #e1efe6;
            color: #555;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .b-time {
            color: #777;
            font-size: 0.8rem;
        }
        
        .b-title {
            color: #0b2c24;
            font-size: 1.3rem;
            margin-bottom: 10px;
            font-weight: 500;
        }
        
        .b-desc {
            color: #555;
            font-size: 0.95rem;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        
        .b-link {
            color: #0b2c24;
            font-weight: 600;
            text-decoration: none;
            font-size: 0.95rem;
        }
        .b-link:hover {
            text-decoration: underline;
        }

        /* Responsive */
        @media (max-width: 992px) {
            .blog-grid-container {
                grid-template-columns: repeat(2, 1fr);
            }
            .blog-title {
                font-size: 3rem;
            }
            .blog-section-title {
                font-size: 2.5rem;
            }
        }
        @media (max-width: 576px) {
            .blog-grid-container {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <main style="padding-top: 80px;">
        <!-- Hero -->
        <section class="blog-hero">
            <div class="icon-sparkle"><i class="fas fa-sparkles"></i></div>
            <h1 class="blog-title">Biznesingiz<br>uchun qulay<br>yechimlar</h1>
            <p class="blog-subtitle">Ishlaringizni tez va oson bajaring. Hamkorlik qilish, buyurtma berish va boshqarish endi yanada soddaroq.</p>
        </section>

        <!-- Articles Section -->
        <section class="blog-section">
            <div class="blog-section-label">YANGI MAHSULOTLAR VA YANGILIKLAR</div>
            <h2 class="blog-section-title">Hammasi bir<br>joyda, tez toping</h2>
            <p class="blog-section-subtitle">Eng so'nggi yangiliklar va foydali tavsiyalar shu yerda</p>
            
            <a href="#" class="blog-btn-primary">Ko'rish</a>
            
            <div class="blog-grid-container">
                <!-- Card 1 -->
                <div class="b-card">
                    <img src="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=400&h=250" alt="Do'kon yangiliklari" class="b-card-img">
                    <div class="b-card-meta">
                        <span class="b-tag">SOTUV</span>
                        <span class="b-time">5 daqiqa o'qiladi</span>
                    </div>
                    <h3 class="b-title">Do'kon yangiliklari</h3>
                    <p class="b-desc">Yangi kelgan mahsulotlar va chegirmalar haqida bilib oling.</p>
                    <a href="#" class="b-link">Batafsil &rarr;</a>
                </div>
                
                <!-- Card 2 -->
                <div class="b-card">
                    <img src="https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&q=80&w=400&h=250" alt="Oson xarid qilish" class="b-card-img">
                    <div class="b-card-meta">
                        <span class="b-tag">JARAYONLAR</span>
                        <span class="b-time">5 daqiqa o'qiladi</span>
                    </div>
                    <h3 class="b-title">Oson xarid qilish</h3>
                    <p class="b-desc">Xarid qilish jarayoni va foydali maslahatlar.</p>
                    <a href="#" class="b-link">Batafsil &rarr;</a>
                </div>

                <!-- Card 3 -->
                <div class="b-card">
                    <img src="https://images.unsplash.com/photo-1588691503849-0d8c973a9032?auto=format&fit=crop&q=80&w=400&h=250" alt="Savollarga javoblar" class="b-card-img">
                    <div class="b-card-meta">
                        <span class="b-tag">YORDAM</span>
                        <span class="b-time">5 daqiqa o'qiladi</span>
                    </div>
                    <h3 class="b-title">Savollarga javoblar</h3>
                    <p class="b-desc">Ko'p so'raladigan savollar va yordam.</p>
                    <a href="#" class="b-link">Batafsil &rarr;</a>
                </div>

                <!-- Card 4 -->
                <div class="b-card">
                    <img src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&q=80&w=400&h=250" alt="Foydalanuvchi tajribasi" class="b-card-img">
                    <div class="b-card-meta">
                        <span class="b-tag">TADQIQOT</span>
                        <span class="b-time">5 daqiqa o'qiladi</span>
                    </div>
                    <h3 class="b-title">Foydalanuvchi tajribasi</h3>
                    <p class="b-desc">Xaridorlar fikri va tajribalari bilan tanishing.</p>
                    <a href="#" class="b-link">Batafsil &rarr;</a>
                </div>
            </div>
        </section>
    </main>
'''

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(header_str + blog_content + ''.join(footer))
