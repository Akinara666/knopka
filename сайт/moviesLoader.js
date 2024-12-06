const popularMovies = [
    'The Godfather', 'The Shawshank Redemption', 'The Dark Knight', 'Pulp Fiction',
    'Forrest Gump', 'Inception', 'Fight Club', 'The Matrix', 'Goodfellas',
    'The Silence of the Lambs', 'Schindler\'s List', 'Star Wars: Episode IV',
    'Casablanca', 'Gladiator', 'The Green Mile', 'Saving Private Ryan', 'Interstellar',
    'The Prestige', 'The Lion King', 'Django Unchained', 'The Avengers', 'Titanic',
    'The Wolf of Wall Street', 'Back to the Future', 'Mad Max: Fury Road', 'Jurassic Park',
    'The Terminator', 'Alien', 'Blade Runner', 'The Lord of the Rings','blade runner 2049','american psycho'
];
const OMDB_API_KEY = '73dcd6c0';

async function fetchMovieDetails(movieIdOrTitle) {
    try {
        let url;
        if (movieIdOrTitle.startsWith('tt')) {
            // Если передан ID фильма
            url = `https://www.omdbapi.com/?i=${encodeURIComponent(movieIdOrTitle)}&apikey=${OMDB_API_KEY}`;
        } else {
            // Если передано название фильма
            url = `https://www.omdbapi.com/?t=${encodeURIComponent(movieIdOrTitle)}&apikey=${OMDB_API_KEY}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (data.Response === 'True') {
            return {
                title: data.Title,
                poster: data.Poster,
                genre: data.Genre,
                rating: data.imdbRating,
            };
        } else {
            console.error(`Фильм "${movieIdOrTitle}" не найден.`);
            return null;
        }
    } catch (error) {
        console.error(`Ошибка при загрузке данных для "${movieIdOrTitle}":`, error);
        return null;
    }
}

async function updateMovies() {
    const movieContainers = document.querySelectorAll('.movies-container');
    const moviePromises = popularMovies.map(fetchMovieDetails);

    const movies = await Promise.all(moviePromises);

    movies.forEach((movie, index) => {
        if (movie) {
            movieContainers.forEach(container => {
                const card = document.createElement('div');
                card.className = 'movie-card';

                const img = document.createElement('img');
                img.src = movie.poster;
                img.alt = movie.title;

                const info = document.createElement('div');
                info.className = 'movie-info';

                const title = document.createElement('h3');
                title.className = 'movie-title';
                title.textContent = movie.title;

                const genre = document.createElement('div');
                genre.className = 'movie-genre';
                genre.textContent = movie.genre;

                info.appendChild(title);
                info.appendChild(genre);
                card.appendChild(img);
                card.appendChild(info);
                container.appendChild(card);
            });
        }
    });
}

async function updateRecommendations() {
    const recommendationsContainer = document.querySelector('.recommendations-container');
    const moviePromises = popularMovies.slice(0, 10).map(fetchMovieDetails);

    const movies = await Promise.all(moviePromises);

    movies.forEach((movie, index) => {
        if (movie) {
            const card = document.createElement('div');
            card.className = 'movie-card';

            const img = document.createElement('img');
            img.src = movie.poster;
            img.alt = movie.title;

            const info = document.createElement('div');
            info.className = 'movie-info';

            const title = document.createElement('h3');
            title.className = 'movie-title';
            title.textContent = movie.title;

            const genre = document.createElement('div');
            genre.className = 'movie-genre';
            genre.textContent = movie.genre;

            info.appendChild(title);
            info.appendChild(genre);
            card.appendChild(img);
            card.appendChild(info);
            recommendationsContainer.appendChild(card);
        }
    });
}

// Обновляем данные фильмов и рекомендаций при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    updateMovies();
    updateRecommendations();
});