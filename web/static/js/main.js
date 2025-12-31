const upperButtons = document.querySelectorAll(".used-nav");

upperButtons.forEach(button => {
    const originalColor = window.getComputedStyle(button).color;
    button.addEventListener("mouseenter", () => {
        button.style.color = "#B1BD00";
    });

    button.addEventListener("mouseleave", () => {
        button.style.color = originalColor;
    });
});

const sideButtons = document.querySelectorAll(".opt-bar");
sideButtons.forEach(button => {
    const originalColor = window.getComputedStyle(button).color;
    const originalBackgroundColor = window.getComputedStyle(button).backgroundColor;
    button.addEventListener("mouseenter", () => {
        button.style.color = "#B1BD00";
        button.style.backgroundColor ="#FFFFFF";
    });

    button.addEventListener("mouseleave", () => {
        button.style.color = originalColor;
        button.style.backgroundColor = originalBackgroundColor;
    });
});

