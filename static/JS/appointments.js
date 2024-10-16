document.getElementById('create-appointment-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Obtener valores del formulario
    const service_id = document.getElementById('service_id').value;
    const appointment_date = document.getElementById('appointment_date').value;
    const appointment_time = document.getElementById('appointment_time').value;
    const status = document.getElementById('status').value;
    const payment_status = document.getElementById('payment_status').value;

    // Obtener token de localStorage
    const token = localStorage.getItem('token');

    // Verificar si el token está presente
    if (!token) {
        alert('No estás autenticado. Por favor, inicia sesión.');
        return;
    }

    try {
        // Realizar solicitud POST para crear la cita
        const response = await fetch('/create_appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                service_id: service_id,
                Appointment_date: appointment_date,
                Appointment_time: appointment_time,
                status: status,
                payment_status: payment_status
            })
        });

        // Verificar si la respuesta es exitosa
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.description || 'Error creando la cita');
        }

        // Si todo está bien, muestra la respuesta del servidor
        const data = await response.json();
        console.log('Cita creada con éxito:', data);
        alert('Cita creada con éxito');
        window.location.href = '/dashboard'; // Redirigir si es necesario

    } catch (error) {
        console.error('Error creando la cita:', error);
        alert('Error creando la cita: ' + error.message);
    }
});
