async function submitReview(serviceId) {
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Debes iniciar sesión para dejar una reseña.');
        window.location.href = '/login';  // Redirige al login si no hay token
        return;
    }

    const comment = document.getElementById(`comment-${serviceId}`).value;
    const rating = document.getElementById(`rating-${serviceId}`).value;

    try {
        const response = await fetch(`/services/${serviceId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Asegúrate de enviar el token JWT
            },
            body: JSON.stringify({ comment, rating })
        });

        if (response.ok) {
            alert('¡Reseña enviada con éxito!');
        } else {
            const error = await response.json();
            alert('Error al enviar la reseña: ' + error.msg);
        }
    } catch (error) {
        console.error('Error al enviar la reseña:', error);
    }
}

