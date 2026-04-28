import os
import glob

files = glob.glob('*.html')

cart_html = '''<div class="cart-icon" id="cartIcon" style="margin-right: 15px; position: relative; cursor: pointer; display: flex; align-items: center;">
            <i class="fas fa-shopping-cart" style="font-size: 1.4rem; color: #004532;"></i>
            <span id="cartCount" style="position: absolute; top: -8px; right: -10px; background: #ff4757; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; font-weight: bold; border: 2px solid white;">0</span>
        </div>
        '''

cart_js = '''
<script>
document.addEventListener('DOMContentLoaded', () => {
    const cartIcon = document.getElementById('cartIcon');
    const cartCount = document.getElementById('cartCount');
    let count = 0;

    document.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', function(e) {
            count++;
            if(cartCount) cartCount.textContent = count;
            
            if(cartIcon) {
                cartIcon.style.transition = 'transform 0.2s';
                cartIcon.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    cartIcon.style.transform = 'scale(1)';
                }, 200);
            }
            
            // Flying element
            const flyingDot = document.createElement('div');
            flyingDot.style.position = 'fixed';
            flyingDot.style.width = '20px';
            flyingDot.style.height = '20px';
            flyingDot.style.background = '#ff4757';
            flyingDot.style.borderRadius = '50%';
            flyingDot.style.zIndex = '999999';
            
            const rect = this.getBoundingClientRect();
            flyingDot.style.left = rect.left + rect.width / 2 + 'px';
            flyingDot.style.top = rect.top + rect.height / 2 + 'px';
            
            document.body.appendChild(flyingDot);
            
            if(cartIcon) {
                const cartRect = cartIcon.getBoundingClientRect();
                
                flyingDot.animate([
                    { left: flyingDot.style.left, top: flyingDot.style.top, transform: 'scale(1)' },
                    { left: cartRect.left + 10 + 'px', top: cartRect.top + 10 + 'px', transform: 'scale(0.5)' }
                ], {
                    duration: 600,
                    easing: 'cubic-bezier(0.25, 1, 0.5, 1)'
                }).onfinish = () => {
                    flyingDot.remove();
                };
            } else {
                setTimeout(() => flyingDot.remove(), 600);
            }
            
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Qo\\'shildi';
            this.style.background = '#004532';
            this.style.color = 'white';
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.background = '';
                this.style.color = '';
            }, 2000);
        });
    });
});
</script>
'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject cart icon in header
    if 'id="cartIcon"' not in html:
        html = html.replace('<a href="register.html" class="btn btn-primary" id="openRegisterBtn"', cart_html + '<a href="register.html" class="btn btn-primary" id="openRegisterBtn"')
    
    # Inject cart JS in products.html
    if file == 'products.html' and 'flyingDot' not in html:
        html = html.replace('</body>', cart_js + '\n</body>')
        
        # Fix broken images in products.html
        replacements = {
            "1615486171545-9279a013f9c6": "1528659556-91e84a2c5a08",
            "1523049673857-eb18f1d7b546": "1518349586146-2cb634358a9e",
            "1555507036-ab1e4006aaeb": "1509440159596-0249088772ff",
            "1598373182133-d4d547f38497": "1509440159596-0249088772ff",
            "1603569283847-3295e910af0f": "1556881286-fc6915169721",
            "1528821128474-27f963b062b2": "1528825871115-3581a5387919"
        }
        for old, new in replacements.items():
            html = html.replace(old, new)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
