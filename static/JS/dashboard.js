// Función para acceder al dashboard
function accessDashboard() {
    const token = localStorage.getItem('jwt_token'); // Asegúrate de que estás guardando el token después de iniciar sesión

    fetch('/dashboard', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Access denied: ' + response.statusText);
        }
        return response.text(); // o response.json() si esperas un JSON
    })
    .then(data => {
        document.getElementById('dashboardContainer').innerHTML = data; // Muestra el contenido del dashboard
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
