const button = document.getElementById("follow-btn");
const followers_txt = document.getElementById("follow-count");

async function follow(username) {
    try {
        const response = await fetch("http://127.0.0.1:8001/follow/", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            return;
        }

        button.innerHTML = "unfollow";
        button.onclick = () => unfollow(username, button);
        let currentCount = parseInt(followers_txt.innerText);
        followers_txt.innerHTML = "<strong>" + (currentCount + 1) + " Followers</strong>";

    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function unfollow(username) {
    try {
        const response = await fetch("http://127.0.0.1:8001/follow/", {
            method: "DELETE",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error:", errorData);
            return;
        }

        button.innerHTML = "follow";
        button.onclick = () => follow(username, button);
        let currentCount = parseInt(followers_txt.innerText);
        followers_txt.innerHTML = "<strong>" + (currentCount - 1) + " Followers</strong>";

    } catch (error) {
        console.error("Error:", error.message);
    }
}