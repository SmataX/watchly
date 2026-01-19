/* --- OBSŁUGA WYSZUKIWARKI --- */
const searchInput = document.getElementById('movie-search-input-nav');
const resultsList = document.getElementById('search-results-list-nav');
let debounceTimer;

if (searchInput && resultsList) {
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
}

/* --- OBSŁUGA ROZWIJANEGO MENU UŻYTKOWNIKA --- */
function toggleUserMenu() {
    const dropdown = document.getElementById("userDropdown");
    if (dropdown) {
        dropdown.classList.toggle("show");
    }
}

/* --- ZAMYKANIE ELEMENTÓW PO KLIKNIĘCIU NA ZEWNĄTRZ --- */
document.addEventListener('click', function(e) {
    if (searchInput && resultsList) {
        if (!searchInput.contains(e.target) && !resultsList.contains(e.target)) {
            resultsList.style.display = 'none';
        }
    }

    if (!e.target.closest('.user-menu-container')) {
        const dropdown = document.getElementById("userDropdown");
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
});

/* --- AUTOMATYCZNE GENEROWANIE AWATARÓW  --- */
document.addEventListener("DOMContentLoaded", function() {
    const avatarImages = document.querySelectorAll('.auto-avatar');

    avatarImages.forEach(img => {
        const username = img.getAttribute('data-username');
        
        if (username) {
            // 1. Sumujemy kody ASCII liter w nazwie (np. k+a+r+o)
            let charSum = 0;
            for (let i = 0; i < username.length; i++) {
                charSum += username.charCodeAt(i);
            }

            // 2. Obliczamy numer obrazka (modulo 34 + 1)
            const avatarNum = (charSum % 34) + 1;

            // 3. Ustawiamy źródło obrazka :)
            img.src = `/static/images/avatars/${avatarNum}.png`;
        }
    });
});