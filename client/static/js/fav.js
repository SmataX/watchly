const fav_btn = document.getElementById('fav-btn');

async function add_fav(movie_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8001/movies/${movie_id}/fav`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: movie_id
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            return;
        }

        fav_btn.style.color = 'orange';
        fav_btn.onclick = () => remove_fav(movie_id, fav_btn);

    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function remove_fav(movie_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8001/movies/${movie_id}/fav`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: movie_id
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            return;
        }

        fav_btn.removeAttribute('style');
        fav_btn.onclick = () => add_fav(movie_id, fav_btn);

    } catch (error) {
        console.error("Error:", error.message);
    }
}