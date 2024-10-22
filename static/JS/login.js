document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Evita que el formulario recargue la página por defecto
    console.log("Formulario enviado");  // Confirma que el evento se dispara

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    console.log("Datos enviados:", { email, password }); // Verifica los datos que se envían

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        console.log('Estado de la respuesta:', response.status); // Verifica el estado de la respuesta

        if (response.ok) {
            const data = await response.json();
            console.log('Datos de respuesta:', data);
            if (data.access_token) {
                console.log('Token recibido:', data.access_token);
                localStorage.setItem('token', data.access_token);
                window.location.href = data.redirect_url;
            } else {
                console.error('Token no encontrado en la respuesta:', data);
            }
        } else {
            const errorData = await response.json();
            console.error('Error en la autenticación:', errorData);
            alert('Error de inicio de sesión: ' + errorData.msg);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        alert('Error al conectar con el servidor.');
    }
});
