document.addEventListener('DOMContentLoaded', () => {

    // ===== CHECK GOOGLE LOGIN STATE =====
    const headerActions = document.getElementById('headerActions');
    const savedUser = localStorage.getItem('google_user');
    const GOOGLE_CLIENT_ID = '937984856077-9uk43pn7ljstlpstp0261j95mnfmq6qi.apps.googleusercontent.com';

    // Global callback for Google Sign-In
    window.handleCredentialResponse = (response) => {
        const base64Url = response.credential.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        const userInfo = JSON.parse(jsonPayload);
        
        // Save and sync
        localStorage.setItem('google_user', JSON.stringify({
            name: userInfo.name,
            email: userInfo.email,
            picture: userInfo.picture || null
        }));

        fetch('/api/google-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: userInfo.name,
                email: userInfo.email,
                picture: userInfo.picture || null
            })
        }).finally(() => window.location.reload());
    };

    if (savedUser && headerActions) {
        const user = JSON.parse(savedUser);

        // Build avatar HTML
        let avatarHtml;
        if (user.picture) {
            avatarHtml = `<img src="${user.picture}" alt="${user.name}" class="user-pill-avatar">`;
        } else {
            const initials = (user.name || 'U').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
            avatarHtml = `<span class="user-pill-initials">${initials}</span>`;
        }

        // Replace ONLY the register button with user pill
        const regBtn = document.getElementById('openRegisterBtn');
        if (regBtn) {
            const pillDiv = document.createElement('div');
            pillDiv.className = 'user-pill';
            pillDiv.innerHTML = `
                ${avatarHtml}
                <span class="user-pill-name">${user.name}</span>
                <button class="user-pill-logout" id="logoutBtn" title="Chiqish">
                    <i class="fas fa-sign-out-alt"></i>
                </button>
            `;
            regBtn.parentNode.replaceChild(pillDiv, regBtn);
        }

        // Logout button
        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('google_user');
            window.location.reload();
        });
    } else if (headerActions) {
        // Initialize Google for Header
        function initGoogleHeader() {
            if (typeof google !== 'undefined') {
                google.accounts.id.initialize({
                    client_id: GOOGLE_CLIENT_ID,
                    callback: window.handleCredentialResponse
                });
                const btnHeader = document.getElementById("g_id_signin_header");
                if (btnHeader) {
                    google.accounts.id.renderButton(
                        btnHeader,
                        { theme: "outline", size: "medium", text: "signin" } 
                    );
                }
            } else {
                setTimeout(initGoogleHeader, 1000);
            }
        }
        initGoogleHeader();
    }

    // ===== FEATURES FILTERING =====
    const tabBtns = document.querySelectorAll('.tab-btn');
    const featureCards = document.querySelectorAll('.feature-card');
    const featuresGrid = document.getElementById('featuresGrid');

    function showCards(filter) {
        featureCards.forEach(card => {
            const category = card.getAttribute('data-category');
            const shouldShow = (filter === 'all' && category === 'all') || category === filter;

            if (shouldShow) {
                card.classList.remove('hide');
                card.style.opacity = '0';
                card.style.transform = 'translateY(16px)';
                // Staggered animation
                const idx = Array.from(featureCards).filter(c => !c.classList.contains('hide')).indexOf(card);
                setTimeout(() => {
                    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, idx * 60);
            } else {
                card.style.opacity = '0';
                card.style.transform = 'translateY(8px)';
                setTimeout(() => {
                    card.classList.add('hide');
                    card.style.transform = '';
                    card.style.transition = '';
                }, 250);
            }
        });
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');
            showCards(filter);
        });
    });

    // Initialize — show "all" cards on load with animation
    setTimeout(() => showCards('all'), 100);


    // ===== SCROLL TO TOP =====
    const scrollToTopBtn = document.getElementById('scrollToTopBtn');
    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ===== HEADER SHRINK ON SCROLL =====
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.08)';
        } else {
            header.style.boxShadow = 'none';
        }
    });

    // ===== REGISTER MODAL =====
    const openBtn = document.getElementById('openRegisterBtn');
    const modal = document.getElementById('registerModal');
    const closeBtn = document.getElementById('closeRegisterBtn');
    const registerForm = document.getElementById('registerForm');

    function openModal() {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);

    // Close on overlay click
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }

    // ===== CART FUNCTIONALITY =====
    const cartIcon = document.getElementById('cartIcon');
    const cartCount = document.getElementById('cartCount');

    if (cartIcon) {
        cartIcon.addEventListener('click', () => {
            window.location.href = 'cart.html';
        });

        // Initialize cart badge
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        if (cart.length > 0 && cartCount) {
            cartCount.style.display = 'block';
        }
    }

    // Close on Escape key or Admin shortcut (Alt + Shift + Ctrl)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
        if (e.altKey && e.shiftKey && e.ctrlKey) {
            window.location.href = 'admin.html';
        }
    });

    // Form submit
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = registerForm.querySelector('.submit-btn');
            submitBtn.textContent = "Jo'natildi ✓";
            submitBtn.style.background = '#4ade80';
            setTimeout(() => {
                closeModal();
                registerForm.reset();
                submitBtn.textContent = 'Submit';
                submitBtn.style.background = '';
            }, 1800);
        });
    }
});
