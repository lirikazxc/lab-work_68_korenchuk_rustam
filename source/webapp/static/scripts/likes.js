async function makeRequest(url, method="GET") {
    let response = await fetch(url, { "method": method });
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(await response.text());
        console.log(error);
        throw error;
    }
}

function onLoad() {
    let likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        console.log(button)
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            let a = event.target
            let url = a.href;
            try {
                let response = await makeRequest(url);
                let likeCountElem = button.nextElementSibling.querySelector('.like-count');
                let icon = button.querySelector('i');
                if (response.liked) {
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill');
                } else {
                    icon.classList.remove('bi-heart-fill');
                    icon.classList.add('bi-heart');
                }

                likeCountElem.textContent = response.like_count;
            } catch (error) {
                console.error('oшибка:', error);
            }
        });
    });
}

window.addEventListener("load", onLoad);
