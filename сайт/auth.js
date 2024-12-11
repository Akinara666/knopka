// auth.js

const tokenKey = 'auth_token';

/**
 * Get auth token from localStorage
 */
export function getToken() {
    return localStorage.getItem(tokenKey);
}

/**
 * Set auth token to localStorage
 * @param {string} token
 */
export function setToken(token) {
    localStorage.setItem(tokenKey, token);
}

/**
 * Remove auth token from localStorage
 */
export function removeToken() {
    localStorage.removeItem(tokenKey);
}

/**
 * Make an authenticated fetch request
 * @param {string} url
 * @param {object} options
 */
export async function authFetch(url, options = {}) {
    const token = getToken();
    if (!options.headers) {
        options.headers = {};
    }
    if (token) {
        options.headers['Authorization'] = token;
    }
    const response = await fetch(url, options);
    return response;
}

/**
 * Handle user registration
 * @param {Event} e
 */
export async function handleSignup(e) {
    e.preventDefault();
    const username = document.getElementById('signupUsername').value.trim();
    const login = document.getElementById('signupLogin').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    const payload = { username, login, password, email: '' }; // Adjust if you have email field

    try {
        const response = await fetch('http://localhost:5000/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (response.ok) {
            alert('Registration successful! You can now log in.');
            hideModals();
        } else {
            alert(`Registration failed: ${data.error}`);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred. Please try again.');
    }
}

/**
 * Handle user login
 * @param {Event} e
 */
export async function handleLogin(e) {
    e.preventDefault();
    const login = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;

    const payload = { login, password };

    try {
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (response.ok) {
            setToken(data.token);
            alert(`Welcome, ${data.username}!`);
            hideModals();
            // Optionally, reload the page or fetch user-specific data
            showTab('home'); // Load home tab
        } else {
            alert(`Login failed: ${data.error}`);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
    }
}

// This function will be imported into main.js. It needs access to hideModals and showTab.
// We'll rely on these being available globally or imported in main.js.
// You can handle this by moving hideModals and showTab into a separate module and importing them here if you prefer.
