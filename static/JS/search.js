document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-input");
    const servicesList = document.getElementById("results-container");

    // Filtrar servicios según el texto de búsqueda
    searchInput.addEventListener("input", function() {
        const query = searchInput.value.toLowerCase();

        // Obtener todos los servicios
        const services = servicesList.getElementsByClassName("service");

        // Mostrar/ocultar servicios basados en la búsqueda
        Array.from(services).forEach(function(service) {
            const serviceName = service.querySelector("h2").textContent.toLowerCase();
            if (serviceName.includes(query)) {
                service.style.display = "";
            } else {
                service.style.display = "none";
            }
        });
    });
});
