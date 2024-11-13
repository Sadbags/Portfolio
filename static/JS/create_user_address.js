document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("register-form"); // Select the registration form // Selecciona el formulario de registro

    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent the default form submission // Evitar el envío del formulario por defecto

        const formData = new FormData(form); // Create a FormData object from the form // Crear un objeto FormData a partir del formulario

        // Get the form data // Obtener los datos del formulario
        const data = {
            first_name: formData.get("first_name"), // Get the first name // Obtener el nombre
            last_name: formData.get("last_name"), // Get the last name // Obtener el apellido
            email: formData.get("email"), // Get the email // Obtener el correo electrónico
            password: formData.get("password"), // Get the password // Obtener la contraseña
            confirm_password: formData.get("confirm-password"), // Get the confirm password // Obtener la confirmación de la contraseña
            address: formData.get("address"), // Get the address // Obtener la dirección
            street: formData.get("street"), // Get the street // Obtener la calle
            city: formData.get("city"), // Get the city // Obtener la ciudad
            state: formData.get("state"), // Get the state // Obtener el estado
            zip_code: formData.get("zip_code"), // Get the zip code // Obtener el código postal
            phone: formData.get("phone"), // Get the phone number // Obtener el número de teléfono
            user_type: formData.get("user_type") // Get the user type // Obtener el tipo de usuario
        };

        try {
            // Make the POST request // Hacer la solicitud POST
            const response = await fetch("/register", {
                method: "POST", // Use the POST method // Usar el método POST
                headers: {
                    "Content-Type": "application/json" // Set the content type to JSON // Establecer el tipo de contenido a JSON
                },
                body: JSON.stringify(data) // Convert the form data to JSON // Convertir los datos del formulario a JSON
            });

            if (!response.ok) {
                const errorData = await response.json(); // Parse the error response // Analizar la respuesta de error
                document.querySelector('.error-message').textContent = errorData.error; // Display the error message // Mostrar el mensaje de error
            } else {
                // Redirect to a success page or the dashboard // Redirigir a una página de éxito o al dashboard
                window.location.href = response.url; // Change this as needed // Cambia esto según sea necesario
            }
        } catch (error) {
            console.error("Error en el registro:", error); // Log the error // Registrar el error
            document.querySelector('.error-message').textContent = "Error al registrar. Inténtalo de nuevo."; // Display a generic error message // Mostrar un mensaje de error genérico
        }
    });
});