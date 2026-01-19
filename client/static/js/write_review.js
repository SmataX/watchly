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
            credentials: "include",
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
        window.location.reload(true);

    } catch (error) {
        console.error("Error:", error.message);
    }
}

text_area.addEventListener("input", (event) => { 
    counter.innerHTML = text_area.value.length + '/500';
})


function enable_edit(btn, reviewId) {
    const card = btn.closest('.review-card-item');
    const textContainer = card.querySelector('.review-card-text');
    const pTag = textContainer.querySelector('p');
    
    if (!pTag) return;

    const currentContent = pTag.innerText;
    
    const textArea = document.createElement('textarea');
    textArea.value = currentContent;
    textArea.className = 'review-textarea';
    textArea.style.width = '100%';
    textArea.style.minHeight = '100px';

    textContainer.replaceChild(textArea, pTag);

    btn.textContent = "Save";
    btn.onclick = () => submit_edit(reviewId, textArea.value);
}

async function submit_edit(reviewId, newContent) {
    if (newContent.length < 3) {
        alert("Review is too short.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8001/reviews/${reviewId}`, {
            method: "PUT",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                content: newContent
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            alert("Failed to update review.");
            return;
        }

        window.location.reload(true);

    } catch (error) {
        console.error("Error:", error.message);
    }
}