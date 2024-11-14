document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');  // Verificar si el formulario existe

    if (form) { // Verifica que el formulario existe antes de añadir el event listener
        form.addEventListener('submit', async function(event) {
            event.preventDefault();  // Evita que el formulario recargue la página

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',  // Define que el cuerpo es JSON
                    },
                    body: JSON.stringify({ email, password })  // Envía los datos como un objeto JSON
                });

                if (response.ok) {
                    const data = await response.json();  // Parsear la respuesta JSON
                    console.log(data);

                    // Guarda el access_token y el refresh_token en localStorage
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('refresh_token', data.refresh_token);

                    // Redirige al usuario a la página de éxito
                    window.location.href = '/dashboard';  // Cambia '/dashboard' por la URL deseada
                } else {
                    const error = await response.json();
                    alert('Error de inicio de sesión: ' + error.msg);  // Muestra un mensaje de error
                }
            } catch (error) {
                console.error('Error de conexión:', error);
                alert('Error al conectar con el servidor. Por favor, intenta nuevamente.');
            }
        });
    } else {
        console.error("El formulario no fue encontrado en el DOM."); // Mensaje de error si no se encuentra el formulario
    }
});
