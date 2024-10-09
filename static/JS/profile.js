// profile.js

document.getElementById('edit-profile-btn').addEventListener('click', function() {
    document.getElementById('profile-pic-input').click();
});

document.getElementById('profile-pic-input').addEventListener('change', function() {
    const profilePicInput = document.getElementById('profile-pic-input');
    if (profilePicInput.files && profilePicInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-pic').src = e.target.result;
        }
        reader.readAsDataURL(profilePicInput.files[0]);
    }
});

document.getElementById('edit-profile-btn').addEventListener('click', function() {
    document.getElementById('edit-profile-modal').style.display = 'block';
});

document.getElementById('close-btn').addEventListener('click', function() {
    document.getElementById('edit-profile-modal').style.display = 'none';
});

document.getElementById('edit-profile-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe

    // Actualiza la información del perfil
    const profileNameInput = document.getElementById('profile-name-input').value;
    const profileEmailInput = document.getElementById('profile-email-input').value;
    const profilePhoneInput = document.getElementById('profile-phone-input').value;
    const profileReviewsInput = document.getElementById('profile-reviews-input').value;
    const profileServicesInput = document.getElementById('profile-services-input').value;

    document.getElementById('profile-name').textContent = profileNameInput;
    document.getElementById('profile-email').textContent = profileEmailInput;
    document.getElementById('profile-phone').textContent = profilePhoneInput;

    // Actualiza las reseñas
    document.querySelector('.reviews-section p').textContent = profileReviewsInput;

    // Actualiza los servicios
    const services = profileServicesInput.split('\n');
    const cardsContainer = document.getElementById('cards-container');
    cardsContainer.innerHTML = ''; // Limpia las tarjetas existentes

    services.forEach(service => {
        const [title, description] = service.split(':');
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <img src="{{ url_for('static', filename='images/default-service.jpg') }}" alt="${title.trim()}">
            <div class="card-content">
                <h3>${title.trim()}</h3>
                <p>${description.trim()}</p>
            </div>
        `;
        cardsContainer.appendChild(card);
    });

    // Cierra el modal
    document.getElementById('edit-profile-modal').style.display = 'none';
});

