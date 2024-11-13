//Este código JavaScript gestiona la creación de una cita al enviar un formulario de manera asíncrona, usando fetch para enviar una solicitud POST al servidor. // This JavaScript code handles creating an appointment by submitting a form asynchronously, using fetch to send a POST request to the server.

document.getElementById('create-appointment-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the default form submission // Prevenir el envío predeterminado del formulario

    // Get form values // Obtener valores del formulario
    const service_id = document.getElementById('service_id').value;
    const appointment_date = document.getElementById('appointment_date').value;
    const appointment_time = document.getElementById('appointment_time').value;
    const status = document.getElementById('status').value;
    const payment_status = document.getElementById('payment_status').value;

    // Get token from localStorage // Obtener token de localStorage
    const token = localStorage.getItem('token');

    // Check if the token is present // Verificar si el token está presente
    if (!token) {
        alert('You are not authenticated. Please log in.');  // Alert if not authenticated // Alertar si no está autenticado
        return;
    }

    try {
        // Make a POST request to create the appointment // Realizar solicitud POST para crear la cita
        const response = await fetch('/create_appointments', {
            method: 'POST',  // HTTP method to use // Método HTTP a utilizar
            headers: {
                'Content-Type': 'application/json',  // Specify the content type as JSON // Especifica el tipo de contenido como JSON
                'Authorization': `Bearer ${token}`  // Include the token in the Authorization header // Incluye el token en el encabezado de Autorización
            },
            body: JSON.stringify({  // Convert the form data to JSON // Convertir los datos del formulario a JSON
                service_id: service_id,
                Appointment_date: appointment_date,
                Appointment_time: appointment_time,
                status: status,
                payment_status: payment_status
            })
        });

        // Check if the response is successful // Verificar si la respuesta es exitosa
        if (!response.ok) {
            const errorData = await response.json();  // Parse the error response // Analizar la respuesta de error
            throw new Error(errorData.description || 'Error creating the appointment');  // Throw an error if the request failed // Lanzar un error si la solicitud falló
        }

        // If everything is fine, display the server response // Si todo está bien, muestra la respuesta del servidor
        const data = await response.json();
        console.log('Appointment created successfully:', data);  // Log the success message // Registrar el mensaje de éxito
        alert('Appointment created successfully');  // Alert the success message // Alertar el mensaje de éxito
        window.location.href = '/dashboard';  // Redirect if necessary // Redirigir si es necesario

    } catch (error) {
        console.error('Error creating the appointment:', error);  // Log the error message // Registrar el mensaje de error
        alert('Error creating the appointment: ' + error.message);  // Alert the error message // Alertar el mensaje de error
    }
});