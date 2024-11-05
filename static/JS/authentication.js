async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refresh_token'); // O donde estés almacenando el token

    if (!refreshToken) {
        console.error("No refresh token found!");
        return;
    }

    try {
        const response = await fetch('/token/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${refreshToken}` // Incluye el refresh token en el header
            }
        });

        if (response.ok) {
            const data = await response.json();
            const newAccessToken = data.access_token;
            localStorage.setItem('access_token', newAccessToken); // Almacena el nuevo access token
            console.log("Access token refreshed successfully!");
        } else {
            console.error("Failed to refresh access token", response.status);
        }
    } catch (error) {
        console.error("Error refreshing access token", error);
    }
}

// Llama a esta función cuando detectes que el token de acceso ha expirado
