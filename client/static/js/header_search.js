(() => {
    const searchInput = document.getElementById('movie-search-input-nav');
    const resultsList = document.getElementById('search-results-list-nav');
    let debounceTimer;

    if (!searchInput || !resultsList) return;

    searchInput.addEventListener('input', function () {
        const query = this.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            resultsList.style.display = 'none';
            resultsList.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/api/search_movies?query=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(movies => {
                    resultsList.innerHTML = '';

                    if (movies.length) {
                        resultsList.style.display = 'block';
                        movies.forEach(movie => {
                            const li = document.createElement('li');
                            li.innerHTML = <a href="http://127.0.0.1:8001/movies/${movie.id}">${movie.title}</a>;
                            resultsList.appendChild(li);
                        });
                    } else {
                        resultsList.style.display = 'none';
                    }
                });
        }, 300);
    });

    document.addEventListener('click', e => {
        if (!searchInput.contains(e.target) && !resultsList.contains(e.target)) {
            resultsList.style.display = 'none';
        }
    });
})();