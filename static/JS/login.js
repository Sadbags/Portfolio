// Escucha el evento 'submit' del formulario de inicio de sesión
document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Evita que el formulario recargue la página por defecto

    // Obtén los valores de los campos de email y password
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        // Realiza una solicitud POST al endpoint de login en el servidor
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Define que el cuerpo es JSON
            },
            body: JSON.stringify({ email, password })  // Envía los datos como un objeto JSON
        });

        // Verifica si la respuesta es exitosa (status 200-299)
        if (response.ok) {
            const data = await response.json();  // Parsear la respuesta JSON

            // Guarda el token JWT en localStorage para futuras solicitudes autenticadas
            localStorage.setItem('token', data.access_token);

            // Redirige al usuario a la página de perfil u otra página de éxito
            window.location.href = '/dashboard';  // Redirige al perfil del usuario
        } else {
            // Si hay un error en la autenticación (por ejemplo, credenciales incorrectas)
            const error = await response.json();
            alert('Error de inicio de sesión: ' + error.description);  // Muestra un mensaje de error
        }
    } catch (error) {
        // Si ocurre un error de conexión (como cuando el servidor está caído)
        console.error('Error de conexión:', error);
        alert('Error al conectar con el servidor. Por favor, intenta nuevamente.');
    }
});


// este codigo es el q brega
// el q viene ahora es el q tiene al dash
