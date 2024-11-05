document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const loginMessage = document.getElementById('login-message');

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Clear previous messages
        loginMessage.textContent = '';
        loginMessage.classList.remove('error', 'success');

        // Capture form data
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value;

        // Basic Frontend Validation
        if (username === '' || password === '') {
            loginMessage.textContent = 'Both fields are required.';
            loginMessage.classList.add('error');
            return;
        }

        // Prepare data to send
        const data = {
            username: username,
            password: password
        };

        try {
            const csrfToken = getCookie('csrf_token');

            const response = await fetch('https://0xelectron.ir/login.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                loginMessage.textContent = result.message || 'Login successful!';
                loginMessage.classList.add('success');
                loginForm.reset();

                // Redirect the user to a dashboard page
                window.location.href = '/dashboard';
            } else {
                loginMessage.textContent = result.error || 'Invalid username or password.';
                loginMessage.classList.add('error');
            }
        } catch (error) {
            console.error('Error:', error);
            loginMessage.textContent = 'An unexpected error occurred.';
            loginMessage.classList.add('error');
        }
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
});
