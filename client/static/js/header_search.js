const searchInput = document.getElementById('movie-search-input-nav');
const resultsList = document.getElementById('search-results-list-nav');
    let debounceTimer;

    searchInput.addEventListener('input', function() {
        const query = this.value.trim();

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            resultsList.style.display = 'none';
            resultsList.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(() => {
            console.log(`Wysyłam zapytanie o: ${query}`);

            fetch(`/api/search_movies?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(items => {
                    resultsList.innerHTML = '';
                    console.log('Otrzymane elementy:', items);
                    if (items.length > 0) {
                        resultsList.style.display = 'block';
                        items.forEach(item => {
                            console.log('Otrzymany element:', item);
                            const li = document.createElement('li');
                            
                            // Dodajemy ikonkę lub tekst w zależności od typu
                            let badge = '';
                            if (item.type === 'movie') {
                                badge = '<span style="font-size: 0.8em; color: #aaa; float: right;">🎬 Film</span>';
                            } else if (item.type === 'user') {
                                badge = '<span style="font-size: 0.8em; color: #4CAF50; float: right;">👤 User</span>';
                            }

                            // Używamy item.url przygotowanego przez Python
                            li.innerHTML = `<a href="${item.url}" style="display: block; width: 100%;">${item.title} ${badge}</a>`;
                            resultsList.appendChild(li);
                        });
                    } else {
                        resultsList.style.display = 'none';
                    }
                })
                .catch(error => console.error('Błąd pobierania:', error));
        }, 300);
    });

    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !resultsList.contains(e.target)) {
            resultsList.style.display = 'none';
        }
    });