document.getElementById('profilePictureForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe de la manera tradicional
        const formData = new FormData(this); // Crea un objeto FormData

        fetch('/users/<user_id>/profile_picture', { // Cambia <user_id> al ID del usuario correspondiente
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('message');
            const errorElement = document.getElementById('error');
            errorElement.textContent = ''; // Limpiar mensajes de error

            if (data.message) {
                messageElement.textContent = data.message; // Mostrar mensaje de éxito
            } else {
                errorElement.textContent = 'Error al subir la foto: ' + data.error; // Mostrar mensaje de error
            }
        })
        .catch(error => {
            document.getElementById('error').textContent = 'Error en la solicitud: ' + error;
        });
    });