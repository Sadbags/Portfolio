document.getElementById('create-service-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Evitar que el formulario recargue la página

    // Obtener los valores del formulario
    const name = document.getElementById('service_name').value;
    const description = document.getElementById('service_description').value;
    const aprox_price = document.getElementById('service_price').value;
    const category = document.getElementById('service_category').value;
    const fee = document.getElementById('service_fee').value;

    // Asegúrate de que el token JWT esté disponible
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Error: Please log in first.');
        return;
    }

    // Crear el objeto de datos del servicio
    const serviceData = {
        name: name,
        description: description,
        aprox_price: aprox_price,
        category: category,
        fee: fee
    };

    try {
        // Enviar la solicitud POST al servidor con el token JWT en los encabezados
        const response = await fetch('/api/services', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,  // Incluir el token JWT
                'Content-Type': 'application/json'   // Especificar que los datos son JSON
            },
            body: JSON.stringify(serviceData)  // Convertir los datos del formulario a JSON
        });

        // Manejar la respuesta
        if (response.ok) {
            alert('Service created successfully!');
            window.location.href = '/dashboard';  // Redirigir al dashboard o donde prefieras
        } else {
            const errorData = await response.json();
            alert('Error creating service: ' + (errorData.description || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while creating the service.');
    }
});
