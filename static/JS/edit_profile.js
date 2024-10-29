const modal = document.getElementById('edit-profile-modal');
    const openBtn = document.getElementById('edit-profile-open-btn'); // Este sería el botón que abre el modal
    const closeBtn = document.getElementById('close-btn');
    const form = document.getElementById('edit-profile-form');

    // Función para abrir el modal
    openBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    // Función para cerrar el modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Cerrar modal si se hace clic fuera de la ventana modal
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Manejo del envío del formulario
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevenimos el comportamiento por defecto del formulario

        // Crear un objeto FormData para manejar archivos
        const formData = new FormData(form);

        // Opcional: Añadir manualmente los valores al FormData si no está obteniéndolos correctamente
        formData.append('name', document.getElementById('profile-name-input').value);
        formData.append('email', document.getElementById('profile-email-input').value);
        formData.append('phone', document.getElementById('profile-phone-input').value);
        formData.append('reviews', document.getElementById('profile-reviews-input').value);

        // Para manejar la imagen de perfil
        const profilePic = document.getElementById('profile-pic-input').files[0];
        if (profilePic) {
            formData.append('profile_pic', profilePic);
        }

        // Realizar la solicitud AJAX para enviar los datos al servidor
        fetch('/profile', { // Asegúrate de que la URL coincida con tu ruta de edición
            method: 'PUT', // O 'PUT', si tienes un middleware que maneje el método _method como PUT
            body: formData,
        })
        .then(response => response.json()) // Suponiendo que el servidor devuelve JSON
        .then(data => {
            if (data.success) {
                // Si la actualización fue exitosa, cierra el modal
                modal.style.display = 'none';
                alert('Profile updated successfully!');
                // Aquí podrías también actualizar la vista sin recargar la página
                // Por ejemplo, actualizar el nombre, el email o la imagen en la página actual
            } else {
                alert('Failed to update profile: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the profile.');
        });
    });


// script para cerrar edit form
// Espera a que todo el contenido de la página se cargue
document.addEventListener('DOMContentLoaded', function () {
	const closeButton = document.getElementById('close-btn');
	const modal = document.getElementById('edit-profile-modal');

	closeButton.addEventListener('click', function () {
		modal.style.display = 'none'; // Oculta el modal
	});

	window.addEventListener('click', function (event) {
		if (event.target === modal) {
			modal.style.display = 'none'; // Oculta el modal si se hace clic fuera del contenido
		}
	});

	document.getElementById('edit-profile-btn').addEventListener('click', function() {
		modal.style.display = 'block'; // Muestra el modal
	});
});
