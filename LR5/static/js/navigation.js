document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector(".navbar");

    navbar.addEventListener("click", e => {
        if (e.target.classList.contains("tab")) {
            e.preventDefault();
            window.location.href = `/${e.target.id}`
        }
    });
});