document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-appointment-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Evita que el formulario se envíe de forma tradicional

        // Captura los datos del formulario
        const formData = {
            service_id: document.getElementById('service_id').value,
            Appointment_date: document.getElementById('appointment_date').value,  // El input ya tiene formato "YYYY-MM-DD"
            Appointment_time: document.getElementById('appointment_time').value,  // El input de time
            status: document.getElementById('status').value,
            payment_status: document.getElementById('payment_status').value
        };

        // Enviar la solicitud POST al backend
        fetch('/create_appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`  // Obtén el token JWT del localStorage
            },
            body: JSON.stringify(formData)  // Convierte los datos a JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Procesa la respuesta exitosa
            console.log('Appointment created successfully:', data);
            alert('Appointment created successfully!');
        })
        .catch(error => {
            console.error('Error creating appointment:', error);
            alert('Error creating appointment: ' + error.message);
        });
    });
});