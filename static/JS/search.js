// script.js

document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe

    const query = document.getElementById('search-input').value.toLowerCase();
    const resultsContainer = document.getElementById('results-container');

    // Simula una lista de servicios
    const services = [
        'Web Development',
        'Graphic Design',
        'SEO Optimization',
        'Digital Marketing',
        'Content Writing',
        'App Development',
        'Social Media Management'
    ];

    // Filtra los servicios que coinciden con la consulta
    const filteredServices = services.filter(service => service.toLowerCase().includes(query));

    // Limpia los resultados anteriores
    resultsContainer.innerHTML = '';

    // Muestra los resultados filtrados
    if (filteredServices.length > 0) {
        filteredServices.forEach(service => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.textContent = service;
            resultsContainer.appendChild(div);
        });
    } else {
        resultsContainer.textContent = 'No services found.';
    }
});