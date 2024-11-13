const token = localStorage.getItem('jwt'); // Retrieve the token from localStorage // Recupera el token de localStorage
console.log('Token enviado:', token); // Verify that the token is being retrieved correctly // Verifica que el token se esté obteniendo correctamente

fetch('/dashboard', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,  // Add a comma after this line // Agrega una coma después de esta línea
        'Content-Type': 'application/json'  // Specify that the data is JSON for the POST request to the dashboard // Especifica que los datos son JSON para la solicitud POST al dashboard
    }
})
.then(response => {
    if (!response.ok) {
        console.error('Error:', response); // Log the error if the response is not ok // Registra el error si la respuesta no es correcta
        if (response.status === 401) {
            window.location.href = '/login'; // Redirect to login if not authorized // Redirige al login si no está autorizado
        }
        return;
    }
    return response.text();
})
.then(data => {
    console.log(data);  // Process the dashboard data here // Procesa los datos del dashboard aquí
})
.catch(error => {
    console.error('There was a problem with your fetch operation:', error); // Log any errors that occur during the fetch // Registra cualquier error que ocurra durante la solicitud
});

//sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar'); // Select the sidebar element // Selecciona el elemento de la barra lateral
    const mainContent = document.querySelector('.main-content'); // Select the main content element // Selecciona el elemento del contenido principal
    sidebar.classList.toggle('open'); // Toggle the 'open' class on the sidebar // Alterna la clase 'open' en la barra lateral
    mainContent.classList.toggle('open'); // Toggle the 'open' class on the main content // Alterna la clase 'open' en el contenido principal
}