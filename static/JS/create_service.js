// nuevo codigo de script crear servicio con el refresh token
document.getElementById('create-service-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Obtener valores del formulario
    const name = document.getElementById('service_name').value;
    const description = document.getElementById('service_description').value;
    const aprox_price = document.getElementById('service_price').value;
    const category = document.getElementById('service_category').value;
    const fee = document.getElementById('service_fee').value;
    const pictureFile = document.getElementById('service_picture').files[0];

    // Lector de archivos para convertir imagen a Base64
    const reader = new FileReader();
    reader.onloadend = async function() {
        const pictureData = reader.result.split(',')[1];

        const serviceData = {
            name: name,
            description: description,
            aprox_price: aprox_price,
            category: category,
            fee: fee,
            picture: pictureData
        };

        // Obtener el token
        const token = await getAccessToken();
        if (!token) {
            alert('Error: Please log in first.');
            return;
        }

        try {
            const response = await fetch('/api/services', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(serviceData)
            });

            if (response.ok) {
                alert('Service created successfully!');
                window.location.href = '/dashboard';
            } else {
                const errorData = await response.json();
                alert('Error creating service: ' + (errorData.description || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while creating the service.');
        }
    };

    reader.readAsDataURL(pictureFile);
});

// Función para obtener el access token, renovándolo si es necesario
async function getAccessToken() {
    let token = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    if (!token) return null;

    // Verificar si el token ha expirado
    if (isTokenExpired(token)) {
        if (!refreshToken) {
            return null;  // No hay refresh token, el usuario debe volver a iniciar sesión
        }

        // Renovar el access token usando el refresh token
        try {
            const response = await fetch('/api/refresh-token', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refreshToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                token = data.access_token;
                localStorage.setItem('access_token', token);  // Actualizar el access token en localStorage
            } else {
                return null;  // Falló la renovación del token
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            return null;
        }
    }
    return token;
}

// Función para verificar si el token ha expirado
function isTokenExpired(token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiry = payload.exp;
    const now = Math.floor(Date.now() / 1000);
    return now > expiry;
}
