document.addEventListener('DOMContentLoaded', (event) => {
    const shareButton = document.querySelector('.share-profile-btn');

    shareButton.addEventListener('click', () => {
        // Obtén la URL actual
        const profileUrl = window.location.href;

        // Crea un elemento de texto temporal
        const tempInput = document.createElement('input');
        tempInput.value = profileUrl;
        document.body.appendChild(tempInput);

        // Selecciona y copia el texto
        tempInput.select();
        document.execCommand('copy');

        // Elimina el elemento de texto temporal
        document.body.removeChild(tempInput);

        // Muestra una notificación o alerta
        alert('Profile URL copied to clipboard!');
    });
});
