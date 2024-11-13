//This JavaScript code is designed to update an access token using a refresh token. // Este código JavaScript está diseñado para actualizar un token de acceso utilizando un token de actualización.

async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refresh_token'); // Or where you are storing the token
    // O donde estés almacenando el token

    // Check if the refresh token is available
    // Verifica si el refresh token está disponible
    if (!refreshToken) {
        console.error("No refresh token found!");
        return;
    }

    try {
        // Send a request to refresh the access token
        // Envía una solicitud para actualizar el token de acceso
        const response = await fetch('/token/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${refreshToken}` // Include the refresh token in the header
                // Incluye el refresh token en el header
            }
        });

        if (response.ok) {
            // Parse the JSON response and extract the new access token
            // Parsea la respuesta JSON y extrae el nuevo access token
            const data = await response.json();
            const newAccessToken = data.access_token;

            // Store the new access token in local storage
            // Almacena el nuevo access token en localStorage
            localStorage.setItem('access_token', newAccessToken);
            console.log("Access token refreshed successfully!");
        } else {
            console.error("Failed to refresh access token", response.status);
        }
    } catch (error) {
        console.error("Error refreshing access token", error);
    }
}

// Call this function when you detect that the access token has expired
// Llama a esta función cuando detectes que el token de acceso ha expirado
