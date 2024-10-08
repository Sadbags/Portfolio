async function submitReview(serviceId) {
    const comment = document.getElementById(`comment-${serviceId}`).value;
    const rating = parseInt(document.getElementById(`rating-${serviceId}`).value);

    // Depuración: Muestra los valores en la consola
    console.log('Comentario:', comment);
    console.log('Calificación:', rating);

    if (!comment || !rating || rating < 1 || rating > 5) {
        alert("Por favor, ingresa un comentario válido y una calificación entre 1 y 5.");
        return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
        alert("Debes estar logueado para enviar una reseña.");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                service_id: serviceId,
                rating: rating,
                comment: comment
            })
        });

        console.log("Response status:", response.status);

        if (response.ok) {
            const data = await response.json();
            alert("Reseña enviada con éxito.");
            console.log("Respuesta del servidor:", data);
        } else {
            const errorResponse = await response.json();
            alert(`Error al enviar la reseña: ${errorResponse.description || "Error desconocido."}`);
            console.error("Error de respuesta del servidor:", errorResponse);
        }
    } catch (error) {
        console.error('Error en la solicitud:', error);
        alert("Error al enviar la reseña. Por favor, inténtalo de nuevo más tarde.");
    }
}
