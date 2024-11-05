document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signup-form');
    const signupMessage = document.getElementById('signup-message');

    signupForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Clear previous messages
        signupMessage.textContent = '';
        signupMessage.classList.remove('error', 'success');

        // Capture form data
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const verifyPassword = document.getElementById('verify-password').value;

        // Basic Frontend Validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const usernamePattern = /^[a-zA-Z0-9_]{3,20}$/;

        if (!usernamePattern.test(username)) {
            signupMessage.textContent = 'Username should be 3-20 characters and contain only letters, numbers, or underscores.';
            signupMessage.classList.add('error');
            return;
        }

        if (!emailPattern.test(email)) {
            signupMessage.textContent = 'Please enter a valid email address.';
            signupMessage.classList.add('error');
            return;
        }

        if (password !== verifyPassword) {
            signupMessage.textContent = 'Passwords do not match.';
            signupMessage.classList.add('error');
            return;
        }

        if (password.length < 6) {
            signupMessage.textContent = 'Password must be at least 6 characters long.';
            signupMessage.classList.add('error');
            return;
        }

        // Prepare data to send
        const data = {
            username: username,
            email: email,
            password: password
        };

        try {
            const csrfToken = getCookie('csrf_token');

            const response = await fetch('https://0xelectron.ir/signup.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                signupMessage.textContent = result.message || 'Signup successful!';
                signupMessage.classList.add('success');
                signupForm.reset();
            } else {
                signupMessage.textContent = result.error || 'An error occurred during signup.';
                signupMessage.classList.add('error');
            }
        } catch (error) {
            console.error('Error:', error);
            signupMessage.textContent = 'An unexpected error occurred.';
            signupMessage.classList.add('error');
        }
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
});
