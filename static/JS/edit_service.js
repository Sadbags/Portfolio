const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

menu.addEventListener('click', function() {
	menu.classList.toggle('is-active');
	menuLinks.classList.toggle('active');
});

document.getElementById('edit-service-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Evita que el formulario se envíe de forma normal

    // Captura los datos del formulario
    const serviceId = window.location.pathname.split('/').pop(); // Obtén el service_id de la URL
    const serviceName = document.getElementById('service_name').value;
    const serviceDescription = document.getElementById('service_description').value;
    const servicePrice = document.getElementById('service_price').value;
    const serviceCategory = document.getElementById('service_category').value;
    const serviceFee = document.getElementById('service_fee').value;

    // Construye el objeto que se enviará
    const serviceData = {
        name: serviceName,
        description: serviceDescription,
        aprox_price: servicePrice,
        category: serviceCategory,
        fee: serviceFee
    };

    // Realiza la solicitud PUT para actualizar el servicio
    fetch(`/edit_service/${serviceId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwt')}`  // Asegúrate de incluir el token si usas autenticación JWT
        },
        body: JSON.stringify(serviceData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar el servicio');
        }
        return response.json();  // Procesa la respuesta como JSON
    })
    .then(data => {
        console.log('Servicio actualizado:', data);
        alert('El servicio ha sido actualizado con éxito.');
        window.location.href = '/dashboard';  // Redirige al dashboard u otra página tras la actualización
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        alert('Hubo un error al actualizar el servicio.');
    });
});
