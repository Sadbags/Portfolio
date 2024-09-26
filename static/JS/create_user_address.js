document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("register-form");

    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Evitar el envío del formulario por defecto

        const formData = new FormData(form);

        // Obtener los datos del formulario
        const data = {
            first_name: formData.get("first_name"),
            last_name: formData.get("last_name"),
            email: formData.get("email"),
            password: formData.get("password"),
            confirm_password: formData.get("confirm-password"),  // Cambia el nombre a "confirm_password"
			address: formData.get("address"),
            street: formData.get("street"),
            city: formData.get("city"),
            state: formData.get("state"),
            zip_code: formData.get("zip_code"),
            phone: formData.get("phone"),
            user_type: formData.get("user_type")
        };

        try {
            // Hacer la solicitud POST
            const response = await fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                document.querySelector('.error-message').textContent = errorData.error;
            } else {
                // Redirigir a una página de éxito o el dashboard, por ejemplo
                window.location.href = response.url; // Cambia esto según sea necesario
            }
        } catch (error) {
            console.error("Error en el registro:", error);
            document.querySelector('.error-message').textContent = "Error al registrar. Inténtalo de nuevo.";
        }
    });
});
