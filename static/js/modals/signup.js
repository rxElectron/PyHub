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
            // Fetch CSRF token from cookie (if using Flask-WTF)
            const csrfToken = getCookie('csrf_token'); // Ensure the CSRF token is set as a cookie

            const response = await fetch('/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Include CSRF token in headers
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                // Success
                signupMessage.textContent = result.message || 'Signup successful!';
                signupMessage.classList.add('success');
                signupForm.reset(); // Clear the form

                // Optionally, redirect the user
                // window.location.href = '/dashboard';
            } else {
                // Server returned an error
                signupMessage.textContent = result.error || 'An error occurred during signup.';
                signupMessage.classList.add('error');
            }
        } catch (error) {
            console.error('Error:', error);
            signupMessage.textContent = 'An unexpected error occurred.';
            signupMessage.classList.add('error');
        }
    });

    /**
     * Helper function to get a cookie's value by name.
     * @param {string} name - The name of the cookie.
     * @returns {string|null} - The cookie's value or null if not found.
     */
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
});
