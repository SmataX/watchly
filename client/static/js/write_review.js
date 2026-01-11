let text_area = document.getElementById('user-review-textarea');
let counter = document.getElementById('user-review-counter');

async function submit_review(movieId) {
    let content = text_area.value;
    
    if (content.length < 3) {
        console.log("Review is too short.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8001/reviews/", {
            method: "POST",
            credentials: "include", // <--- ADD THIS LINE!
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_id: movieId,
                content: content
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            return;
        }

        const result = await response.json();
        console.log("Review added:", result);
        text_area.value = '';
        // Update counter manually after clear
        counter.innerHTML = '0/500'; 

    } catch (error) {
        console.error("Error:", error.message);
    }
}

text_area.addEventListener("input", (event) => { 
    counter.innerHTML = text_area.value.length + '/500';
})