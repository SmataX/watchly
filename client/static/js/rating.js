const rating_stars = document.querySelectorAll(".rating-star")

async function rate_movie(movie_id, value) {
    try {
        const response = await fetch("http://127.0.0.1:8001/rating/", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_id: movie_id,
                rating: value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            return;
        }

        rating_stars.forEach((star, index) => {
            if (index < value) {
                star.style.color = 'orange';
            } else {
                star.removeAttribute('style');
            }
        });

    } catch (error) {
        console.error("Error:", error.message);
    }
}