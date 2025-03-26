document.addEventListener('DOMContentLoaded', function() {
    // Manejo de pestañas en la página de perfil
    if (document.getElementById('tab-upload') && document.getElementById('tab-album')) {
        document.getElementById('tab-upload').addEventListener('click', function() {
            document.getElementById('upload-section').style.display = 'block';
            document.getElementById('album-section').style.display = 'none';
            this.classList.add('is-active');
            document.getElementById('tab-album').classList.remove('is-active');
        });

        document.getElementById('tab-album').addEventListener('click', function() {
            document.getElementById('upload-section').style.display = 'none';
            document.getElementById('album-section').style.display = 'block';
            this.classList.add('is-active');
            document.getElementById('tab-upload').classList.remove('is-active');
        });
    }

    // Manejo de cierre de notificaciones flash
    const modal = document.getElementById("flash-modal");
    const closeModalButtons = modal.querySelectorAll(".delete, .button.is-success");

    // Abre automáticamente el modal si hay mensajes flash
    const messages = modal.querySelectorAll(".message");
    if (messages.length > 0) {
        modal.classList.add("is-active");
    }

    // Cierra el modal al hacer clic en los botones de cierre
    closeModalButtons.forEach(button => {
        button.addEventListener("click", () => {
            modal.classList.remove("is-active");
        });
    });

    // Constantes para detectar el boton de cambio de theme
    const themeToggle = document.getElementById("theme-toggle");
    const htmlElement = document.documentElement;

    // Leer el tema inicial desde localStorage
    const currentTheme = localStorage.getItem("theme") || "light";
    htmlElement.setAttribute("data-theme", currentTheme);

    // Función para actualizar el ícono del botón
    const updateIcon = () => {
        const activeTheme = htmlElement.getAttribute("data-theme");
        themeToggle.innerHTML = activeTheme === "dark" 
            ? '<i class="fa-solid fa-sun"></i>' 
            : '<i class="fa-solid fa-moon"></i>';
    };

    // Actualizar ícono según el tema inicial
    updateIcon();

    // Manejar el clic en el botón para cambiar el tema
    themeToggle.addEventListener("click", () => {
        const activeTheme = htmlElement.getAttribute("data-theme");
        const newTheme = activeTheme === "light" ? "dark" : "light";

        // Cambiar el tema en el atributo y guardar en localStorage
        htmlElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);

        // Actualizar el ícono dinámicamente
        updateIcon();
    });

    // Manejo de pestañas en la página de editar perfil
    const tabSecurity = document.getElementById('tab-security');
    const tabEdit = document.getElementById('tab-edit');
    const securitySection = document.getElementById('security-section');
    const editSection = document.getElementById('edit-section');

    if (tabSecurity && tabEdit && securitySection && editSection) {
        tabSecurity.addEventListener('click', function() {
            tabSecurity.classList.add('is-active');
            tabEdit.classList.remove('is-active');
            securitySection.style.display = 'block';
            editSection.style.display = 'none';
        });

        tabEdit.addEventListener('click', function() {
            tabEdit.classList.add('is-active');
            tabSecurity.classList.remove('is-active');
            securitySection.style.display = 'none';
            editSection.style.display = 'block';
        });
    }

    // Selector de Tema
    const themeSelector = document.querySelector('select[name="theme_preference"]');
    if (themeSelector) {
        themeSelector.addEventListener('change', function () {
            const selectedTheme = this.value;
            document.documentElement.setAttribute('data-theme', selectedTheme);
            document.documentElement.className = 'theme-' + selectedTheme;
        });
    }
});

// Script para OpenStreetMap
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('map')) {
        console.log('Map element found, initializing map...');
        initMap();
    } else {
        console.log('Map element not found');
    }
});

function initMap() {
    console.log('Initializing map...');
    var map = L.map('map').setView([0, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var markers = [];

    var photosElement = document.getElementById('map');
    if (photosElement) {
        var photos = JSON.parse(photosElement.dataset.photos);
        photos.forEach(function(photo) {
            var lat = parseFloat(photo.gps_latitude);
            var lng = parseFloat(photo.gps_longitude);
            if (!isNaN(lat) && !isNaN(lng)) {
                console.log(`Adding marker for photo at (${lat}, ${lng})`);
                var marker = L.marker([lat, lng]).addTo(map)
                    .bindPopup("<b>" + photo.original_filename + "</b><br>" + photo.date_taken);
                markers.push(marker);
            }
        });
    } else {
        console.log('Photos element not found');
    }

    if (markers.length > 0) {
        var group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds());
        console.log('Map bounds set to fit markers');
    } else {
        console.log('No markers to display');
    }
}
