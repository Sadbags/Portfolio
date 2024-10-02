document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');

    // Fetch services from the API and render them dynamically
    const fetchServices = async (query = '') => {
        try {
            let url = '/services';
            if (query) {
                url += `?name=${encodeURIComponent(query)}`; // Adjust as needed based on your API's query params
            }
            const response = await fetch(url);
            if (response.ok) {
                const services = await response.json();
                renderServices(services);
            } else {
                console.error('Error fetching services');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Render services dynamically
    const renderServices = (services) => {
        resultsContainer.innerHTML = ''; // Clear previous results
        if (services.length === 0) {
            resultsContainer.innerHTML = '<p>No services found</p>';
            return;
        }

        services.forEach(service => {
            const serviceElement = document.createElement('div');
            serviceElement.classList.add('service');
            serviceElement.innerHTML = `
                <h2>${service.name}</h2>
                <p>${service.description || 'No description available'}</p>
                <p>Price: $${service.aprox_price}</p>
                <p>Category: ${service.category}</p>
                <img src="${service.img_url || '/static/img/default-service.png'}" alt="${service.name}">
            `;
            resultsContainer.appendChild(serviceElement);
        });
    };

    // Handle form submission for searching services
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const query = searchInput.value.trim();
        fetchServices(query); // Fetch filtered services based on the query
    });

    // Initial fetch to display all services
    fetchServices();
});
