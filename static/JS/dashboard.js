

fetch('/dashboard', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})
.then(response => {
    if (!response.ok) {
        console.error('Error:', response);
        if (response.status === 401) {
            window.location.href = '/login';
        }
        return;
    }
    return response.text();
})
.then(data => {
    // Reemplazar solo el contenido del dashboard sin sobrescribir todo el body
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.innerHTML = data;
    } else {
        console.error('No se encontró el contenedor .main-content');
    }
})
.catch(error => {
    console.error('Error:', error);
});
