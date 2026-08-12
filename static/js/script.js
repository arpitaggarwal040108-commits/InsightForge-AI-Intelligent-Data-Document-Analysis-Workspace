
document.addEventListener("DOMContentLoaded", function () {

    console.log("🤖 Smart AI Assistant initialized");

    const currentPath = window.location.pathname;


    /* =====================================================
       GLOBAL UI INITIALIZATION
       ===================================================== */

    initializeAnimations();

    initializeButtons();

    initializeNavigation();

    initializeFileUpload();

    initializeForms();

    initializeChat();

    initializeTables();

    initializeCharts();

    initializePrediction();

    initializeDashboard();


    /* =====================================================
       PAGE SPECIFIC INITIALIZATION
       ===================================================== */

    if (currentPath === "/") {

        initializeHomePage();

    }

    if (currentPath === "/chat") {

        initializeChatPage();

    }

    if (currentPath.includes("predict")) {

        initializePredictionPage();

    }

});


/* =========================================================
   GLOBAL ANIMATIONS
   ========================================================= */

function initializeAnimations() {

    const elements = document.querySelectorAll(
        ".feature-card, " +
        ".summary-card, " +
        ".glass-section, " +
        ".stat-card, " +
        ".chart-card, " +
        ".glass-card"
    );


    elements.forEach(function (element, index) {

        element.style.opacity = "0";

        element.style.transform =
            "translateY(20px)";


        setTimeout(function () {

            element.style.transition =
                "opacity 0.6s ease, transform 0.6s ease";

            element.style.opacity = "1";

            element.style.transform =
                "translateY(0)";

        }, 80 + index * 45);

    });

}


/* =========================================================
   BUTTON INTERACTIONS
   ========================================================= */

function initializeButtons() {

    const buttons =
        document.querySelectorAll("button");


    buttons.forEach(function (button) {

        button.addEventListener(
            "click",
            function (event) {

                createRipple(
                    button,
                    event
                );

            }
        );

    });

}


/* =========================================================
   RIPPLE EFFECT
   ========================================================= */

function createRipple(button, event) {

    const ripple =
        document.createElement("span");


    const rect =
        button.getBoundingClientRect();


    const x =
        event.clientX - rect.left;


    const y =
        event.clientY - rect.top;


    ripple.style.position = "absolute";

    ripple.style.left = x + "px";

    ripple.style.top = y + "px";

    ripple.style.width = "10px";

    ripple.style.height = "10px";

    ripple.style.borderRadius = "50%";

    ripple.style.background =
        "rgba(255,255,255,0.35)";

    ripple.style.transform =
        "translate(-50%, -50%)";

    ripple.style.pointerEvents =
        "none";

    ripple.style.animation =
        "smartRipple 0.65s ease-out";


    button.style.position =
        "relative";

    button.style.overflow =
        "hidden";


    button.appendChild(ripple);


    setTimeout(function () {

        ripple.remove();

    }, 700);

}


/* =========================================================
   ADD RIPPLE CSS
   ========================================================= */

(function addRippleCSS() {

    const style =
        document.createElement("style");


    style.innerHTML = `

        @keyframes smartRipple {

            from {
                width: 10px;
                height: 10px;
                opacity: 0.8;
            }

            to {
                width: 300px;
                height: 300px;
                opacity: 0;
            }

        }

    `;


    document.head.appendChild(style);

})();


/* =========================================================
   NAVIGATION
   ========================================================= */

function initializeNavigation() {

    const links =
        document.querySelectorAll("nav a");


    links.forEach(function (link) {

        link.addEventListener(
            "click",
            function () {

                document.body.style.opacity =
                    "0.85";


                setTimeout(function () {

                    document.body.style.opacity =
                        "1";

                }, 150);

            }
        );

    });

}


/* =========================================================
   FILE UPLOAD
   ========================================================= */

function initializeFileUpload() {

    const fileInput =
        document.querySelector(
            'input[type="file"]'
        );


    if (!fileInput) {
        return;
    }


    fileInput.addEventListener(
        "change",
        function () {

            if (!this.files.length) {
                return;
            }


            const file =
                this.files[0];


            console.log(
                "Selected file:",
                file.name
            );


            console.log(
                "File size:",
                formatFileSize(file.size)
            );


            /* ---------------------------------------------
               FILE TYPE VALIDATION
               --------------------------------------------- */

            const allowedTypes = [
                ".csv",
                ".pdf"
            ];


            const fileName =
                file.name.toLowerCase();


            const valid =
                allowedTypes.some(
                    function (extension) {

                        return fileName.endsWith(
                            extension
                        );

                    }
                );


            if (!valid) {

                alert(
                    "Please upload a CSV or PDF file."
                );

                this.value = "";

                return;

            }


            /* ---------------------------------------------
               FILE SIZE WARNING
               --------------------------------------------- */

            const maxSize =
                20 * 1024 * 1024;


            if (file.size > maxSize) {

                alert(
                    "File size is larger than 20 MB."
                );

                this.value = "";

                return;

            }


            /* ---------------------------------------------
               VISUAL FEEDBACK
               --------------------------------------------- */

            const parent =
                fileInput.closest(
                    ".upload-box"
                );


            if (parent) {

                parent.style.borderColor =
                    "rgba(34,211,238,0.45)";

                parent.style.boxShadow =
                    "0 0 25px rgba(34,211,238,0.08)";

            }

        }
    );

}


/* =========================================================
   FILE SIZE FORMAT
   ========================================================= */

function formatFileSize(bytes) {

    if (bytes === 0) {
        return "0 Bytes";
    }


    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];


    const index =
        Math.floor(
            Math.log(bytes) /
            Math.log(1024)
        );


    return (
        parseFloat(
            (
                bytes /
                Math.pow(1024, index)
            ).toFixed(2)
        )
        +
        " " +
        units[index]
    );

}


/* =========================================================
   FORM INITIALIZATION
   ========================================================= */

function initializeForms() {

    /* -----------------------------------------------------
       UPLOAD FORM
       ----------------------------------------------------- */

    const uploadForm =
        document.querySelector(
            'form[action="/upload"]'
        );


    if (uploadForm) {

        uploadForm.addEventListener(
            "submit",
            function () {

                const button =
                    uploadForm.querySelector(
                        'button[type="submit"]'
                    );


                if (!button) {
                    return;
                }


                button.disabled = true;


                button.innerHTML =
                    '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';


                button.style.opacity =
                    "0.8";

            }
        );

    }


    /* -----------------------------------------------------
       TRAINING FORM
       ----------------------------------------------------- */

    const trainForm =
        document.querySelector(
            'form[action="/train"]'
        );


    if (trainForm) {

        trainForm.addEventListener(
            "submit",
            function () {

                const button =
                    trainForm.querySelector(
                        'button[type="submit"]'
                    );


                if (!button) {
                    return;
                }


                button.disabled = true;


                button.innerHTML =
                    '<i class="fa-solid fa-spinner fa-spin"></i> Training Model...';


                button.style.opacity =
                    "0.8";

            }
        );

    }


    /* -----------------------------------------------------
       PREDICTION FORM
       ----------------------------------------------------- */

    const forms =
        document.querySelectorAll(
            "form.modern-form"
        );


    forms.forEach(function (form) {

        const action =
            form.getAttribute("action");


        if (
            window.location.pathname.includes(
                "predict"
            )
            ||
            !action
        ) {

            if (
                window.location.pathname.includes(
                    "predict"
                )
            ) {

                form.addEventListener(
                    "submit",
                    function () {

                        const button =
                            form.querySelector(
                                'button[type="submit"]'
                            );


                        if (!button) {
                            return;
                        }


                        button.disabled =
                            true;


                        button.innerHTML =
                            '<i class="fa-solid fa-spinner fa-spin"></i> Predicting...';

                    }
                );

            }

        }

    });

}


/* =========================================================
   CHAT SYSTEM
   ========================================================= */

function initializeChat() {

    const chatForm =
        document.querySelector(
            ".chat-form"
        );


    const textarea =
        document.querySelector(
            ".chat-form textarea"
        );


    if (!chatForm) {
        return;
    }


    /* -----------------------------------------------------
       CHAT FORM SUBMISSION
       ----------------------------------------------------- */

    chatForm.addEventListener(
        "submit",
        function () {

            const button =
                chatForm.querySelector(
                    'button[type="submit"]'
                );


            if (!button) {
                return;
            }


            if (
                textarea &&
                textarea.value.trim() === ""
            ) {

                return;

            }


            button.disabled = true;


            button.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Thinking...';

        }
    );


    /* -----------------------------------------------------
       CTRL + ENTER
       ----------------------------------------------------- */

    if (textarea) {

        textarea.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.ctrlKey &&
                    event.key === "Enter"
                ) {

                    event.preventDefault();

                    chatForm.requestSubmit();

                }

            }
        );


        /* -------------------------------------------------
           TEXTAREA AUTO HEIGHT
           ------------------------------------------------- */

        textarea.addEventListener(
            "input",
            function () {

                this.style.height =
                    "auto";


                this.style.height =
                    Math.min(
                        this.scrollHeight,
                        350
                    )
                    +
                    "px";

            }
        );

    }


    /* -----------------------------------------------------
       RESPONSE SCROLL
       ----------------------------------------------------- */

    const response =
        document.querySelector(
            ".response-message"
        );


    if (response) {

        setTimeout(function () {

            response.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 300);

    }

}


/* =========================================================
   CHAT PAGE
   ========================================================= */

function initializeChatPage() {

    const chatWindow =
        document.querySelector(
            ".chat-window"
        );


    if (!chatWindow) {
        return;
    }


    /* Add subtle glow */

    chatWindow.addEventListener(
        "mouseenter",
        function () {

            chatWindow.style.boxShadow =
                "0 25px 70px rgba(99,102,241,0.16)";

        }
    );


    chatWindow.addEventListener(
        "mouseleave",
        function () {

            chatWindow.style.boxShadow =
                "";

        }
    );

}


/* =========================================================
   TABLE INTERACTIONS
   ========================================================= */

function initializeTables() {

    const tables =
        document.querySelectorAll(
            ".modern-table"
        );


    tables.forEach(function (table) {

        const rows =
            table.querySelectorAll(
                "tbody tr"
            );


        rows.forEach(function (row) {

            row.addEventListener(
                "mouseenter",
                function () {

                    this.style.transition =
                        "background 0.2s ease";

                }
            );

        });

    });

}


/* =========================================================
   CHART INTERACTIONS
   ========================================================= */

function initializeCharts() {

    const charts =
        document.querySelectorAll(
            ".chart-card"
        );


    charts.forEach(function (chart) {

        chart.addEventListener(
            "click",
            function () {

                const image =
                    chart.querySelector(
                        ".chart-image"
                    );


                if (!image) {
                    return;
                }


                /* ------------------------------------------------
                   SIMPLE FULLSCREEN CHART VIEW
                   ------------------------------------------------ */

                const overlay =
                    document.createElement(
                        "div"
                    );


                overlay.style.position =
                    "fixed";

                overlay.style.inset =
                    "0";

                overlay.style.zIndex =
                    "9999";

                overlay.style.background =
                    "rgba(2,4,12,0.92)";

                overlay.style.backdropFilter =
                    "blur(15px)";

                overlay.style.display =
                    "flex";

                overlay.style.alignItems =
                    "center";

                overlay.style.justifyContent =
                    "center";

                overlay.style.padding =
                    "30px";

                overlay.style.cursor =
                    "zoom-out";


                const largeImage =
                    document.createElement(
                        "img"
                    );


                largeImage.src =
                    image.src;


                largeImage.style.maxWidth =
                    "95%";

                largeImage.style.maxHeight =
                    "90vh";

                largeImage.style.objectFit =
                    "contain";

                largeImage.style.borderRadius =
                    "16px";

                largeImage.style.boxShadow =
                    "0 0 80px rgba(99,102,241,0.25)";


                overlay.appendChild(
                    largeImage
                );


                document.body.appendChild(
                    overlay
                );


                overlay.addEventListener(
                    "click",
                    function () {

                        overlay.remove();

                    }
                );

            }
        );

    });

}


/* =========================================================
   PREDICTION PAGE
   ========================================================= */

function initializePrediction() {

    const predictionBox =
        document.querySelector(
            ".prediction-box"
        );


    if (!predictionBox) {
        return;
    }


    predictionBox.style.opacity =
        "0";


    predictionBox.style.transform =
        "scale(0.96)";


    setTimeout(function () {

        predictionBox.style.transition =
            "all 0.6s ease";

        predictionBox.style.opacity =
            "1";

        predictionBox.style.transform =
            "scale(1)";

    }, 200);

}


/* =========================================================
   PREDICTION PAGE INPUTS
   ========================================================= */

function initializePredictionPage() {

    const inputs =
        document.querySelectorAll(
            ".modern-form input"
        );


    inputs.forEach(function (input) {

        input.addEventListener(
            "focus",
            function () {

                this.parentElement
                    .classList
                    .add("input-focused");

            }
        );


        input.addEventListener(
            "blur",
            function () {

                this.parentElement
                    .classList
                    .remove("input-focused");

            }
        );

    });

}


/* =========================================================
   DASHBOARD
   ========================================================= */

function initializeDashboard() {

    const dashboard =
        document.querySelector(
            ".dashboard-container"
        );


    if (!dashboard) {
        return;
    }


    /* -----------------------------------------------------
       NUMBER ANIMATION
       ----------------------------------------------------- */

    const numbers =
        document.querySelectorAll(
            ".summary-card h2"
        );


    numbers.forEach(function (element) {

        animateNumber(element);

    });

}


/* =========================================================
   NUMBER ANIMATION
   ========================================================= */

function animateNumber(element) {

    const text =
        element.textContent.trim();


    const number =
        parseFloat(text);


    if (
        isNaN(number) ||
        number < 1 ||
        number > 1000000
    ) {

        return;

    }


    let current = 0;

    const duration = 700;

    const startTime =
        performance.now();


    function update(currentTime) {

        const elapsed =
            currentTime - startTime;


        const progress =
            Math.min(
                elapsed / duration,
                1
            );


        const eased =
            1 -
            Math.pow(
                1 - progress,
                3
            );


        current =
            Math.floor(
                number * eased
            );


        element.textContent =
            current.toLocaleString();


        if (progress < 1) {

            requestAnimationFrame(
                update
            );

        } else {

            element.textContent =
                number.toLocaleString();

        }

    }


    requestAnimationFrame(
        update
    );

}


/* =========================================================
   HOME PAGE
   ========================================================= */

function initializeHomePage() {

    console.log(
        "🏠 Home page loaded"
    );


    /* -----------------------------------------------------
       HERO PARALLAX EFFECT
       ----------------------------------------------------- */

    const heroCard =
        document.querySelector(
            ".glass-card"
        );


    if (heroCard) {

        document.addEventListener(
            "mousemove",
            function (event) {

                const x =
                    (
                        event.clientX /
                        window.innerWidth
                    ) - 0.5;


                const y =
                    (
                        event.clientY /
                        window.innerHeight
                    ) - 0.5;


                heroCard.style.transform =
                    `
                    translateY(${y * -8}px)
                    rotateY(${x * 4}deg)
                    rotateX(${y * -3}deg)
                    `;

            }
        );

    }

}


/* =========================================================
   KEYBOARD SHORTCUTS
   ========================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        /* -------------------------------------------------
           ESCAPE CLOSES CHART OVERLAY
           ------------------------------------------------- */

        if (event.key === "Escape") {

            const overlays =
                document.querySelectorAll(
                    "body > div"
                );


            overlays.forEach(
                function (overlay) {

                    if (
                        overlay.style.position ===
                        "fixed" &&
                        overlay.style.zIndex ===
                        "9999"
                    ) {

                        overlay.remove();

                    }

                }
            );

        }

    }
);


/* =========================================================
   PREVENT DOUBLE CLICK FORM SUBMISSION
   ========================================================= */

document.addEventListener(
    "submit",
    function (event) {

        const form =
            event.target;


        if (
            form.dataset.submitted ===
            "true"
        ) {

            event.preventDefault();

            return;

        }


        form.dataset.submitted =
            "true";

    },
    true
);


/* =========================================================
   ONLINE / OFFLINE STATUS
   ========================================================= */

window.addEventListener(
    "offline",
    function () {

        console.warn(
            "⚠️ Internet connection lost."
        );

    }
);


window.addEventListener(
    "online",
    function () {

        console.log(
            "✅ Internet connection restored."
        );

    }
);


/* =========================================================
   FINAL INITIALIZATION MESSAGE
   ========================================================= */

console.log(
    "%c Smart AI Assistant ",
    "background:#7c3aed;color:white;padding:6px 12px;border-radius:6px;font-weight:bold;"
);

console.log(
    "%c Complete JavaScript loaded successfully.",
    "color:#22d3ee;font-weight:bold;"
);