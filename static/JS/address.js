// Function to fetch addresses from the server // Función para obtener direcciones del servidor
async function fetchAddresses() {
    // Retrieve the token from local storage (or wherever you are storing the JWT) // Recupera el token del almacenamiento local (o donde estés guardando el JWT)
    const token = localStorage.getItem('token');  

    // Make a GET request to the server to fetch addresses // Realiza una solicitud GET al servidor para obtener direcciones
    const response = await fetch('/addresses/<address_id>', {
        method: 'GET',  // HTTP method to use // Método HTTP a utilizar
        headers: {
            'Authorization': `Bearer ${token}`,  // Include the token in the Authorization header // Incluye el token en el encabezado de Autorización
            'Content-Type': 'application/json'  // Specify the content type as JSON // Especifica el tipo de contenido como JSON
        }
    });

    // Check if the response is OK (status code 200-299) // Verifica si la respuesta es OK (código de estado 200-299)
    if (response.ok) {
        // Parse the JSON response // Analiza la respuesta JSON
        const addresses = await response.json();
        // Display the addresses using a custom function // Muestra las direcciones usando una función personalizada
        displayAddresses(addresses);
    } else {
        // Log an error message if the request failed // Registra un mensaje de error si la solicitud falló
        console.error('Error fetching addresses:', response.status);
    }
}