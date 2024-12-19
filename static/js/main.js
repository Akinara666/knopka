// main.js

document.addEventListener('DOMContentLoaded', () => {
    const tokenKey = 'auth_token';

    // DOM Elements
    const intro = document.querySelector('.intro');
    const mainContent = document.querySelector('.main-content');
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const loginBtn = document.querySelector('.login-btn');
    const signupBtn = document.querySelector('.signup-btn');
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    const closeBtns = document.querySelectorAll('.close');
    const tabLinks = document.querySelectorAll('.sidebar-menu a');
    const tabContents = document.querySelectorAll('.tab-content');
    const searchBar = document.querySelector('.search-bar');
    const moviesContainer = document.querySelector('.movies-container');
    const reelsContainer = document.querySelector('.reels-container');
    const profileName = document.querySelector('.profile-name');
    const profileEmail = document.getElementById('profile-email');
    const profileRegDate = document.getElementById('profile-registration-date');
    const historyList = document.querySelector('.history-list');
    const likedList = document.querySelector('.liked-list');
    const watchLaterList = document.querySelector('.watch-later-list');
    const reels = document.querySelector('.reels');

    // Helper Functions

    if (searchBar) {
        searchBar.addEventListener('input', handleSearch); // Trigger search on input change
    }

    /**
     * Get auth token from localStorage
     */
    function getToken() {
        return localStorage.getItem(tokenKey);
    }

    /**
     * Set auth token to localStorage
     * @param {string} token
     */
    function setToken(token) {
        localStorage.setItem(tokenKey, token);
    }

    /**
     * Remove auth token from localStorage
     */
    function removeToken() {
        localStorage.removeItem(tokenKey);
    }

    /**
     * Make an authenticated fetch request
     * @param {string} url
     * @param {object} options
     */
    async function authFetch(url, options = {}) {
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
     * Show a modal
     * @param {HTMLElement} modal
     */
    function showModal(modal) {
        modal.style.display = 'block';
        overlay.style.display = 'block';
    }

    /**
     * Hide all modals
     */
    function hideModals() {
        loginModal.style.display = 'none';
        signupModal.style.display = 'none';
        overlay.style.display = 'none';
    }

    /**
     * Show a specific tab
     * @param {string} tabId
     */
    async function showTab(tabId) {
        // Hide all tabs
        tabContents.forEach(content => content.style.display = 'none');
        // Remove active class from all links
        tabLinks.forEach(link => link.classList.remove('active'));
        // Show the selected tab
        document.getElementById(tabId).style.display = 'block';
        // Add active class to the corresponding link
        document.querySelector(`.sidebar-menu a[data-tab="${tabId}"]`).classList.add('active');

        // Load content based on the tab
        switch (tabId) {
            case 'home':
                await loadHomePageMovies()
                break;
            case 'profile':
                await loadProfile();
                break;
            case 'history':
                await loadHistory();
                break;
            case 'liked':
                await loadLikedMovies();
                break;
            case 'watch-later':
                await loadWatchLater();
                break;
            case 'scroll-page':
                await loadScrollerContent();
                break;
            default:
                break;
        }
    }

    async function handleSearch(event) {
        const searchInput = event.target.value.trim(); // Get the search term
        const searchContainer = document.querySelector('[id="home"] .movies-container');

        if (searchInput === '') {
            // Reload default movies if the search input is empty
            await loadSearchPageMovies();
            return;
        }

        try {
            // Fetch search results from the backend
            const response = await authFetch(`/api/movies/search?query=${encodeURIComponent(searchInput)}`);
            if (!response.ok) {
                throw new Error('Failed to fetch search results.');
            }
            const movies = await response.json();

            // Clear existing content
            searchContainer.innerHTML = '';

            if (movies.length === 0) {
                // Display a "No Results" message if no movies are found
                const noResultsMessage = document.createElement('div');
                noResultsMessage.classList.add('no-results');
                noResultsMessage.textContent = 'Не найдено фильмов по Вашему запросу.';
                searchContainer.appendChild(noResultsMessage);
                return;
            }

            // Render the search results
            movies.forEach(movie => {
                // Create movie card
                const movieCard = document.createElement('div');
                movieCard.classList.add('movie-card');

                // Add movie image
                const movieImg = document.createElement('img');
                movieImg.src = movie.image_url;
                movieImg.alt = movie.title;

                // Add movie info
                const movieInfo = document.createElement('div');
                movieInfo.classList.add('movie-info');

                const movieTitle = document.createElement('h3');
                movieTitle.classList.add('movie-title');
                movieTitle.textContent = movie.title;

                const movieGenres = document.createElement('div');
                movieGenres.classList.add('movie-genre');
                movieGenres.textContent = movie.genres.replace(/,/g, ' • '); // Convert commas to bullets

                // Append info elements to movie card
                movieInfo.appendChild(movieTitle);
                movieInfo.appendChild(movieGenres);
                movieCard.appendChild(movieImg);
                movieCard.appendChild(movieInfo);

                // Add movie card to container
                searchContainer.appendChild(movieCard);
            });
        } catch (error) {
            console.error('Error during search:', error);
        }
    }


    async function loadHomePageMovies() {
        try {
            // Fetch 20 random movies from the backend
            const response = await authFetch('/api/movies/random-movies');
            if (!response.ok) {
                throw new Error('Failed to fetch random movies.');
            }
            const movies = await response.json();

            // Render the movies
            const homeContainer = document.querySelector('[id="home"] .movies-container');
            homeContainer.innerHTML = ''; // Clear existing content

            movies.forEach(movie => {
                // Create movie card
                const movieCard = document.createElement('div');
                movieCard.classList.add('movie-card');

                // Add movie image
                const movieImg = document.createElement('img');
                movieImg.src = movie.image_url;
                movieImg.alt = movie.title;

                // Add movie info
                const movieInfo = document.createElement('div');
                movieInfo.classList.add('movie-info');

                const movieTitle = document.createElement('h3');
                movieTitle.classList.add('movie-title');
                movieTitle.textContent = movie.title;

                const movieGenres = document.createElement('div');
                movieGenres.classList.add('movie-genre');
                movieGenres.textContent = movie.genres.replace(/,/g, ' • '); // Convert commas to bullets

                // Append info elements to movie card
                movieInfo.appendChild(movieTitle);
                movieInfo.appendChild(movieGenres);
                movieCard.appendChild(movieImg);
                movieCard.appendChild(movieInfo);

                // Add movie card to container
                homeContainer.appendChild(movieCard);
            });
        } catch (error) {
            console.error('Error loading search page movies:', error);
        }
    }


    /**
     * Dynamically render movies into the "Scroller".
     *
     * Each movie is added in the provided format with proper headers, trailers, ratings,
     * and other details.
     *
     * @param {HTMLElement} container - The HTML container for the scroller.
     * @param {Array} movies - An array of movie objects with properties:
     *  - title: string
     *  - description: string
     *  - genres: string (comma-separated genres)
     *  - image_url: string (poster image URL)
     *  - trailer_url: string (YouTube video URL)
     *  - rating: number (movie rating)
     */
    function renderMovies(container, movies) {
        const reels = container.querySelector('.reels');

        // Add each movie as a reel
        movies.forEach((movie, index) => {
            // Create the main reel container
            const reel = document.createElement('div');
            reel.classList.add('reel');

            // Reel header (movie title)
            const reelHeader = document.createElement('div');
            reelHeader.classList.add('reel-header');
            const title = document.createElement('h1');
            title.textContent = movie.title;
            reelHeader.appendChild(title);

            // Reel main content (poster, trailer, and rating)
            const reelMain = document.createElement('div');
            reelMain.classList.add('reel-main');

            // Poster
            const imgHolder = document.createElement('div');
            imgHolder.classList.add('img-holder');
            const img = document.createElement('img');
            img.src = movie.image_url || 'placeholder.jpg';
            img.alt = movie.title;
            imgHolder.appendChild(img);

            // Trailer
            const trailerHolder = document.createElement('div');
            trailerHolder.classList.add('trailer-holder');
            const video = document.createElement('iframe');
            video.id = `video${index + 1}`;
            video.src = movie.trailer_url
                ? `${movie.trailer_url.replace("watch?v=", "embed/")}?autoplay=1&mute=1`
                : '';
            video.width = "560";
            video.height = "315";
            video.setAttribute('frameborder', '0');
            video.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
            video.setAttribute('allowfullscreen', '');
            if (!movie.trailer_url) {
                video.textContent = 'Trailer unavailable';
            }
            trailerHolder.appendChild(video);

            // Rating and actions
            const rating = document.createElement('div');
            rating.classList.add('rating');

            const watchlistBtn = document.createElement('button');
            watchlistBtn.textContent = 'Add to Watchlist';

            const likeBtn = document.createElement('button');
            likeBtn.textContent = 'Like';

            const watchedBtn = document.createElement('button');
            watchedBtn.textContent = 'Watched';

            const metricScore = document.createElement('div');
            metricScore.classList.add('metric-score');
            const score = document.createElement('h1');
            score.textContent = `⭐ ${movie.rating}/10`;
            metricScore.appendChild(score);

            // Append buttons and rating to the rating section
            rating.appendChild(watchlistBtn);
            rating.appendChild(likeBtn);
            rating.appendChild(watchedBtn);
            rating.appendChild(metricScore);

            // Add poster, trailer, and rating to the main content
            reelMain.appendChild(imgHolder);
            reelMain.appendChild(trailerHolder);
            reelMain.appendChild(rating);

            // Reel footer (categories and description)
            const reelFooter = document.createElement('div');
            reelFooter.classList.add('reel-footer');

            // Categories
            const categories = document.createElement('div');
            categories.classList.add('categories');
            movie.genres.split(',').forEach(genre => {
                const category = document.createElement('div');
                category.classList.add('category');
                const genreText = document.createElement('h4');
                genreText.textContent = genre.trim();
                category.appendChild(genreText);
                categories.appendChild(category);
            });

            // Description
            const description = document.createElement('div');
            description.classList.add('description');
            const descriptionText = document.createElement('h4');
            descriptionText.textContent = movie.description;
            description.appendChild(descriptionText);

            // Append categories and description to the footer
            reelFooter.appendChild(categories);
            reelFooter.appendChild(description);

            // Assemble the reel
            reel.appendChild(reelHeader);
            reel.appendChild(reelMain);
            reel.appendChild(reelFooter);

            // Add the reel to the reels container
            reels.appendChild(reel);

            // Add event listener for the "Like" button
            likeBtn.addEventListener('click', async () => {
                try {
                    const response = await authFetch('/api/movies/like', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({movieId: movie.id}),
                    });

                    const result = await response.json();
                    if (response.ok) {
                        alert(result.message);
                    } else {
                        alert(result.error);
                    }
                } catch (error) {
                    console.error('Error liking the movie:', error);
                    alert('An error occurred while liking the movie.');
                }
            });
        });
    }


    /**
     * Load scroller content (recommended movies)
     * Adjust based on your HTML structure
     */
    async function loadScrollerContent() {
        const response = await authFetch('/api/movies/recommendations', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            const movies = await response.json();
            // Assuming reelsContainer is the scroller
            renderMovies(reelsContainer, movies);
        } else {
            console.error('Failed to fetch scroller content');
            renderMovies(reelsContainer, []);
        }

    }

    let isLoading = false; // To prevent duplicate fetch calls

    /**
     * Append new movies to the scroller dynamically.
     */
    async function loadMoreMovies() {
        if (isLoading) return;
        isLoading = true;

        try {
            const response = await authFetch('/api/movies/recommendations', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const movies = await response.json();
                renderMovies(reelsContainer, movies);
            } else {
                console.error('Failed to fetch additional movies');
            }
        } catch (error) {
            console.error('Error fetching more movies:', error);
        } finally {
            isLoading = false;
        }
    }

    /**
     * Check if user scrolled near the bottom of the scroller.
     */
    function handleScroll() {
        const {scrollTop, scrollHeight, clientHeight} = reels;
        console.log(`scrollTop: ${scrollTop}, scrollHeight: ${scrollHeight}, clientHeight: ${clientHeight}`);

        if (scrollTop + clientHeight >= scrollHeight) {
            console.log('Near bottom, loading more content...');
            loadMoreMovies();
        }
    }

    /**
     * Load user profile and render it
     */
    async function loadProfile() {
        const response = await authFetch('/api/user/profile', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            const profile = await response.json();
            profileName.textContent = profile.username;
            profileEmail.textContent = profile.email || 'Not provided';
            profileRegDate.textContent = profile.registration_date;
        } else {
            console.error('Failed to fetch profile');
        }
    }

    /**
     * Handle user registration
     * @param {Event} e
     */
    async function handleSignup(e) {
        e.preventDefault();
        const username = document.getElementById('signupUsername').value.trim();
        const login = document.getElementById('signupLogin').value.trim();
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('signupConfirmPassword').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return;
        }

        const payload = {username, login, password, email: ''}; // Adjust if you have email field

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
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
    async function handleLogin(e) {
        e.preventDefault();
        const login = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;

        const payload = {login, password};

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
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

    // Event Listeners

    // Handle window load to start intro animation
    window.addEventListener('load', () => {
        setTimeout(() => {
            intro.classList.add('hidden');
            mainContent.classList.add('visible');
            showTab('home');
        }, 3000);
    });

    // Handle menu toggle
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // Close menu when clicking on overlay
    overlay.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        hideModals();
    });

    // Close modals when clicking on close buttons
    closeBtns.forEach(btn => {
        btn.addEventListener('click', hideModals);
    });

    // Handle tab switching
    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = e.target.getAttribute('data-tab');
            showTab(targetTab);
            // Close the sidebar after selecting a tab
            menuToggle.classList.remove('active');
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    });

    // Handle login form submission
    loginModal.querySelector('form').addEventListener('submit', handleLogin);

    // Handle signup form submission
    signupModal.querySelector('form').addEventListener('submit', handleSignup);

    // Handle login button click
    loginBtn.addEventListener('click', () => {
        showModal(loginModal);
    });

    // Handle signup button click
    signupBtn.addEventListener('click', () => {
        showModal(signupModal);
    });

    // Handle search
    searchBar.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }

    });
    // Attach scroll event listener to the scroller
    reels.addEventListener('scroll', handleScroll);
});
