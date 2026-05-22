AOS.init({
        duration: 900,
        once: true,
        offset: 80
    });

    const navbar = document.getElementById("navbar");

    window.addEventListener("scroll", () => {
        navbar.classList.toggle("scrolled", window.scrollY > 50);
    });

    document.addEventListener("DOMContentLoaded", () => {
        const currentPage = window.location.pathname.split("/").pop() || "index.html";
        
        document.querySelectorAll(".dropdown-item").forEach(item => {
            const href = item.getAttribute("href");
            if (href === currentPage) {
                item.classList.add("active");
            }
        });

        const navbarCollapse = document.getElementById("navbarNav");
        const navLinks = document.querySelectorAll(".navbar .nav-link:not(.dropdown-toggle), .dropdown-item");
        
        navLinks.forEach(link => {
            link.addEventListener("click", () => {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains("show")) {
                    const bsCollapse = bootstrap.Collapse.getOrCreateInstance(navbarCollapse);
                    bsCollapse.hide();
                }
            });
        });
    });
    
    document.documentElement.style.overflowX = "hidden";
    document.body.style.overflowX = "hidden";