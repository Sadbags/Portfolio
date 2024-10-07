document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    console.log("Email:", email);  // Agrega esto para depurar
    console.log("Password:", password);  // Agrega esto para depurar

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);  // Si estás utilizando tokens, esto es válido
            window.location.href = data.redirect_url;  // Redirige a la URL proporcionada por el backend
        } else {
            const error = await response.json();
            alert('Login failed: ' + error.msg);
        }
    } catch (error) {
        console.error('Error de conexión', error);
        alert('Error de conexión. Intenta nuevamente.');
    }
});
