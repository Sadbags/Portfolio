const menu = document.querySelector('#mobile-menu') // Select the mobile menu element // Selecciona el elemento del menú móvil
const menuLinks = document.querySelector('.navbar__menu') // Select the navbar menu links // Selecciona los enlaces del menú de la barra de navegación

menu.addEventListener('click', function() {
    menu.classList.toggle('is-active'); // Toggle the 'is-active' class on the menu // Alterna la clase 'is-active' en el menú
    menuLinks.classList.toggle('active'); // Toggle the 'active' class on the menu links // Alterna la clase 'active' en los enlaces del menú
});

document.getElementById('edit-service-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting normally // Evita que el formulario se envíe de forma normal

    // Capture the form data // Captura los datos del formulario
    const serviceId = window.location.pathname.split('/').pop(); // Get the service_id from the URL // Obtén el service_id de la URL
    const serviceName = document.getElementById('service_name').value;
    const serviceDescription = document.getElementById('service_description').value;
    const servicePrice = document.getElementById('service_price').value;
    const serviceCategory = document.getElementById('service_category').value;
    const serviceFee = document.getElementById('service_fee').value;

    // Build the object to be sent // Construye el objeto que se enviará
    const serviceData = {
        name: serviceName,
        description: serviceDescription,
        aprox_price: servicePrice,
        category: serviceCategory,
        fee: serviceFee
    };

    // Make the PUT request to update the service // Realiza la solicitud PUT para actualizar el servicio
    fetch(`/edit_service/${serviceId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwt')}`  // Ensure to include the token if using JWT authentication // Asegúrate de incluir el token si usas autenticación JWT
        },
        body: JSON.stringify(serviceData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar el servicio'); // Throw an error if the response is not ok // Lanza un error si la respuesta no es correcta
        }
        return response.json();  // Process the response as JSON // Procesa la respuesta como JSON
    })
    .then(data => {
        console.log('Servicio actualizado:', data); // Log the updated service data // Registra los datos del servicio actualizado
        alert('El servicio ha sido actualizado con éxito.'); // Alert success // Alerta de éxito
        window.location.href = '/dashboard';  // Redirect to the dashboard or another page after the update // Redirige al dashboard u otra página tras la actualización
    })
    .catch(error => {
        console.error('Error en la solicitud:', error); // Log any errors in the request // Registra cualquier error en la solicitud
        alert('Hubo un error al actualizar el servicio.'); // Alert error // Alerta de error
    });
});