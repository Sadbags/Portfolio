//Este código JavaScript gestiona la creación de una cita al enviar un formulario de manera asíncrona, usando fetch para enviar una solicitud POST al servidor. // This JavaScript code handles creating an appointment by submitting a form asynchronously, using fetch to send a POST request to the server.
// ultimo code
document.getElementById('create-appointment-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Evitar el envío predeterminado del formulario

    // Obtener valores del formulario
    const service_id = document.getElementById('service_id').value;
    const appointment_date = document.getElementById('appointment_date').value;
    const appointment_time = document.getElementById('appointment_time').value;
    const status = document.getElementById('status').value;
    const payment_status = document.getElementById('payment_status').value;

    // Validar formato de hora HH:MM
    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(appointment_time)) {
        alert('Invalid time format. Please use HH:MM');
        return;
    }

    // Obtener el token desde localStorage o renovarlo si ha expirado
    const token = await getAccessToken();
    if (!token) {
        alert('Authentication error. Please log in again.');
        return;
    }

    // Crear el objeto de datos para la cita
    const appointmentData = {
        service_id: service_id,
        Appointment_date: appointment_date,
        Appointment_time: appointment_time,
        status: status,
        payment_status: payment_status
    };

    try {
        // Hacer la solicitud POST para crear la cita
        const response = await fetch('/create_appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(appointmentData)
        });

        // Verificar si la respuesta fue exitosa
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.description || 'Error creating the appointment');
        }

        // Mostrar éxito y redirigir si es necesario
        alert('Appointment created successfully');
        window.location.href = '/dashboard';

    } catch (error) {
        console.error('Error creating the appointment:', error);
        alert('Error creating the appointment: ' + error.message);
    }
});

// Función para obtener el token de acceso, con renovación si ha expirado
async function getAccessToken() {
    let token = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    if (!token) return null;

    // Verificar si el token ha expirado
    if (isTokenExpired(token)) {
        if (!refreshToken) {
            return null;
        }

        try {
            const response = await fetch('/api/refresh-token', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refreshToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                token = data.access_token;
                localStorage.setItem('access_token', token);
            } else {
                return null;
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            return null;
        }
    }
    return token;
}

// Función para verificar si el token ha expirado
function isTokenExpired(token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiry = payload.exp;
    const now = Math.floor(Date.now() / 1000);
    return now > expiry;
}
