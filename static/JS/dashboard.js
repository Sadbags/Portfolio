const token = localStorage.getItem('jwt'); // Recupera el token de localStorage
console.log('Token enviado:', token); // Verifica que el token se esté obteniendo correctamente

fetch('/dashboard', {
	method: 'GET',
	headers: {
		'Authorization': `Bearer ${token}`,  // Add a comma after this line
		'Content-Type': 'application/json'  // Especifica que los datos son JSON para la solicitud POST al dashboard
	}
})
.then(response => {
    if (!response.ok) {
        console.error('Error:', response);
        if (response.status === 401) {
            window.location.href = '/login'; // Redirige al login si no está autorizado
        }
        return;
    }
    return response.text();
})
.then(data => {
    console.log(data);  // Procesa los datos del dashboard aquí
})
.catch(error => {
    console.error('There was a problem with your fetch operation:', error);
});
