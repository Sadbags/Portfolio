document.getElementById('create-service-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the form from reloading the page // Evitar que el formulario recargue la página

    // Get the form values // Obtener los valores del formulario
    const name = document.getElementById('service_name').value;
    const description = document.getElementById('service_description').value;
    const aprox_price = document.getElementById('service_price').value;
    const category = document.getElementById('service_category').value;
    const fee = document.getElementById('service_fee').value;
    const pictureFile = document.getElementById('service_picture').files[0];  // Get the image file // Obtener el archivo de imagen

    // Ensure the JWT token is available // Asegúrate de que el token JWT esté disponible
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Error: Please log in first.'); // Alert if no token is found // Alerta si no se encuentra el token
        return;
    }

    // Create a file reader to convert the image to Base64 // Crear un lector de archivos para convertir la imagen a Base64
    const reader = new FileReader();
    reader.onloadend = async function() {
        const pictureData = reader.result.split(',')[1];  // Get only the base64 part of the URL // Obtener solo la parte base64 de la URL

        // Create the service data object // Crear el objeto de datos del servicio
        const serviceData = {
            name: name,
            description: description,
            aprox_price: aprox_price,
            category: category,
            fee: fee,
            picture: pictureData  // Add the image in Base64 format // Agregar la imagen en formato Base64
        };

        try {
            // Send the POST request to the server with the JWT token in the headers // Enviar la solicitud POST al servidor con el token JWT en los encabezados
            const response = await fetch('/api/services', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,  // Include the JWT token // Incluir el token JWT
                    'Content-Type': 'application/json'   // Specify that the data is JSON // Especificar que los datos son JSON
                },
                body: JSON.stringify(serviceData)  // Convert the form data to JSON // Convertir los datos del formulario a JSON
            });

            // Handle the response // Manejar la respuesta
            if (response.ok) {
                alert('Service created successfully!'); // Alert success // Alerta de éxito
                window.location.href = '/dashboard';  // Redirect to the dashboard or preferred location // Redirigir al dashboard o donde prefieras
            } else {
                const errorData = await response.json();
                alert('Error creating service: ' + (errorData.description || 'Unknown error')); // Alert error // Alerta de error
            }
        } catch (error) {
            console.error('Error:', error); // Log any errors // Registra cualquier error
            alert('An error occurred while creating the service.'); // Alert error // Alerta de error
        }
    };

    // Read the image file as a data URL // Leer el archivo de imagen como URL de datos
    reader.readAsDataURL(pictureFile);
});