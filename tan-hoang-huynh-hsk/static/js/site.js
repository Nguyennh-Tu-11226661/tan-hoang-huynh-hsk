document.addEventListener("DOMContentLoaded", () => {
    const filterButtons = document.querySelectorAll("[data-filter]");
    const courseItems = document.querySelectorAll(".course-item");

    filterButtons.forEach((button) => {
        button.addEventListener("click", () => {
            filterButtons.forEach((item) => item.classList.remove("active"));
            button.classList.add("active");
            const filter = button.dataset.filter;

            courseItems.forEach((item) => {
                const text = item.dataset.search || "";
                const aliases = {
                    hsk: "hsk",
                    "giao-tiep": "giao tiếp",
                    "nguoi-moi": "người mới",
                };
                item.hidden = filter !== "all" && !text.includes(aliases[filter]);
            });
        });
    });

    const dateInput = document.querySelector('input[type="date"]');
    if (dateInput && !dateInput.min) {
        dateInput.min = new Date().toISOString().split("T")[0];
    }
});
