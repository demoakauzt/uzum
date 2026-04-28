const GOOGLE_CLIENT_ID = '937984856077-9uk43pn7ljstlpstp0261j95mnfmq6qi.apps.googleusercontent.com';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const submitBtn = document.getElementById('submitBtn');
    const successMsg = document.getElementById('successMsg');
    const overlay = document.getElementById('googleSuccessOverlay');
    // ===== GOOGLE SIGN-IN SETUP =====
    window.handleCredentialResponse = (response) => {
        // Decode JWT token to get user info
        const base64Url = response.credential.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        const userInfo = JSON.parse(jsonPayload);
        showGoogleSuccess(userInfo);
    };

    // Initialize Google Identity Services
    function initGoogle() {
        if (typeof google !== 'undefined') {
            google.accounts.id.initialize({
                client_id: GOOGLE_CLIENT_ID,
                callback: window.handleCredentialResponse,
                auto_select: false,
                cancel_on_tap_outside: true
            });

            const btnDiv = document.getElementById("g_id_signin");
            if (btnDiv) {
                google.accounts.id.renderButton(
                    btnDiv,
                    {
                        theme: "outline",
                        size: "large",
                        width: "350",
                        text: "signin_with",
                        shape: "rectangular",
                        logo_alignment: "left",
                        alignment: "center"
                    }
                );
            }
            google.accounts.id.prompt();
        } else {
            // Retry after 1 second if library not loaded yet
            setTimeout(initGoogle, 1000);
        }
    }

    initGoogle();

    function showGoogleSuccess(userInfo) {
        // Fill overlay data
        document.getElementById('googleName').textContent = 'Xush kelibsiz, ' + (userInfo.given_name || userInfo.name) + '!';
        document.getElementById('googleEmail').textContent = userInfo.email || '';

        const avatarEl = document.getElementById('googleAvatar');
        if (userInfo.picture) {
            avatarEl.innerHTML = `<img src="${userInfo.picture}" alt="avatar">`;
        } else {
            const initials = (userInfo.name || 'U').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
            avatarEl.innerHTML = initials;
        }

        // Show overlay
        overlay.style.display = 'flex';

        // Send to backend
        fetch('/api/google-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: userInfo.name,
                email: userInfo.email,
                picture: userInfo.picture || null
            })
        }).catch(e => console.log('Backend sync error')).finally(() => {
            // Save user info to localStorage (persists across pages)
            localStorage.setItem('google_user', JSON.stringify({
                name: userInfo.name,
                email: userInfo.email,
                picture: userInfo.picture || null
            }));

            // Redirect after loading bar (2.8s)
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2800);
        });
    }

    // ===== FORM VALIDATION =====
    function validateField(input) {
        const group = input.closest('.form-group');
        let valid = true;

        if (input.type === 'email') {
            valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
        } else if (input.tagName === 'INPUT') {
            valid = input.value.trim().length > 1;
        }

        if (!valid && input.value.trim() !== '') {
            group.classList.add('has-error');
            input.classList.add('error');
        } else {
            group.classList.remove('has-error');
            input.classList.remove('error');
        }

        return valid || input.value.trim() === '';
    }

    form.querySelectorAll('input').forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => {
            if (input.classList.contains('error')) validateField(input);
        });
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        let allValid = true;
        form.querySelectorAll('input[required]').forEach(input => {
            let valid = true;
            if (input.type === 'email') {
                valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
            } else {
                valid = input.value.trim().length > 1;
            }

            const group = input.closest('.form-group');
            if (!valid) {
                group.classList.add('has-error');
                input.classList.add('error');
                allValid = false;
            }
        });

        if (!allValid) return;

        // Loading state
        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').textContent = 'Yuborilmoqda...';
        submitBtn.querySelector('.btn-loader').style.display = 'inline';
        submitBtn.disabled = true;

        const formData = {
            firstName: document.getElementById('firstName').value,
            lastName: document.getElementById('sharifName').value,
            familyName: document.getElementById('familyName').value,
            email: document.getElementById('emailAddr').value,
            message: document.getElementById('message').value
        };

        fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
            .then(res => res.json())
            .then(data => {
                submitBtn.classList.remove('loading');
                submitBtn.classList.add('success');
                submitBtn.querySelector('.btn-text').textContent = "Jo'natildi ✓";
                submitBtn.querySelector('.btn-loader').style.display = 'none';
                successMsg.classList.add('show');

                // Redirect to main page
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1800);
            })
            .catch(err => {
                // Offline fallback: Pretend it succeeded so user isn't stuck
                submitBtn.classList.remove('loading');
                submitBtn.classList.add('success');
                submitBtn.querySelector('.btn-text').textContent = "Jo'natildi ✓";
                submitBtn.querySelector('.btn-loader').style.display = 'none';
                successMsg.classList.add('show');

                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1800);
            });
    });
});
