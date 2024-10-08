document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        // Si la solicitud es exitosa
        if (response.ok) {
            const data = await response.json();

            // Guarda el token JWT en localStorage
            localStorage.setItem('token', data.access_token);

            // Redirige a la página de perfil o alguna otra URL si está disponible
            window.location.href = '/profile';  // Cambia la URL según lo que desees
        } else {
            const error = await response.json();
            alert('Error de inicio de sesión: ' + error.description);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        alert('Error al conectar con el servidor. Por favor, intenta nuevamente.');
    }
});
