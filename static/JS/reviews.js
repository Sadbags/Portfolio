document.getElementById('reviewForm').addEventListener('submit', function(event) {
	event.preventDefault(); // Evita el comportamiento predeterminado del formulario

	// Obtener los datos del formulario
	const serviceId = "{{ service.id }}"; // Obtener el ID del servicio
	const rating = document.getElementById('rating').value;
	const comment = document.getElementById('comment').value;

	// Enviar los datos en formato JSON
	fetch('{{ url_for("submit_review") }}', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			service_id: serviceId,
			rating: rating,
			comment: comment
		})
	})
	.then(response => response.json())
	.then(data => {
		console.log('Review submitted:', data);
		// Mostrar un mensaje de éxito o actualizar la página
	})
	.catch((error) => {
		console.error('Error:', error);
	});
});