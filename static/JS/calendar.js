const menu = document.querySelector('#mobile-menu') // Select the mobile menu element // Selecciona el elemento del menú móvil
const menuLinks = document.querySelector('.navbar__menu') // Select the navbar menu links // Selecciona los enlaces del menú de la barra de navegación

menu.addEventListener('click', function() {
    menu.classList.toggle('is-active'); // Toggle the 'is-active' class on the menu // Alterna la clase 'is-active' en el menú
    menuLinks.classList.toggle('active'); // Toggle the 'active' class on the menu links // Alterna la clase 'active' en los enlaces del menú
});

// calendar
const daysContainer = document.querySelector(".days"), // Select the container for the days // Selecciona el contenedor para los días
nextBtn = document.querySelector(".next-btn"), // Select the next button // Selecciona el botón de siguiente
prevBtn = document.querySelector(".prev-btn"), // Select the previous button // Selecciona el botón de anterior
month = document.querySelector(".month"); // Select the month display element // Selecciona el elemento de visualización del mes
todayBtn = document.querySelector(".today-btn"); // Select the today button // Selecciona el botón de hoy

const months = [
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
]; // Array of month names // Array de nombres de meses

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]; // Array of day names // Array de nombres de días

// get current date
const date = new Date(); // Get the current date // Obtiene la fecha actual

//get current month
let currentMonth = date.getMonth(); // Get the current month // Obtiene el mes actual

// get current year
let currentYear = date.getFullYear(); // Get the current year // Obtiene el año actual

console.log(date, currentMonth, currentYear) // Log the current date, month, and year // Registra la fecha, mes y año actuales

// function to render days
function renderCalendar() {
    //get previous month current month and next month days
    date.setDate(1); // Set the date to the first of the month // Establece la fecha al primero del mes
    const firstDay = new Date(currentYear, currentMonth, 1); // Get the first day of the current month // Obtiene el primer día del mes actual
    const lastDay = new Date(currentYear, currentMonth + 1, 0) // Get the last day of the current month // Obtiene el último día del mes actual
    const lastDayIndex = lastDay.getDay(); // Get the index of the last day // Obtiene el índice del último día
    const lastDayDate = lastDay.getDate(); // Get the date of the last day // Obtiene la fecha del último día
    const prevLastDay = new Date(currentYear, currentMonth, 0); // Get the last day of the previous month // Obtiene el último día del mes anterior
    const prevLastDayDate = prevLastDay.getDate(); // Get the date of the last day of the previous month // Obtiene la fecha del último día del mes anterior
    const nextDays = 7 - lastDayIndex - 1; // Calculate the number of days in the next month to display // Calcula el número de días del próximo mes a mostrar

    //update current year and month in header
    month.innerHTML = `${months[currentMonth]} ${currentYear}`; // Update the month and year display // Actualiza la visualización del mes y año

    // update days html
    let days = ""; // Initialize the days HTML // Inicializa el HTML de los días

    //prev days html
    for (let x = firstDay.getDay(); x > 0; x--) {
        days += `<div class="day prev">${prevLastDayDate - x + 1}</div>`; // Add the previous month's days // Agrega los días del mes anterior
    }

    // current month days
    for (let i = 1; i <= lastDayDate; i++) {
        //check if its today then add today class
        if (
            i === new Date().getDate() &&
            currentMonth === new Date().getMonth() &&
            currentYear === new Date().getFullYear()
        ) {
            // if date month year matches add today
            days += `<div class="day today">${i}</div>`; // Add the 'today' class if the date matches // Agrega la clase 'today' si la fecha coincide
        } else {
            // else don`t add today
            days += `<div class="day ">${i}</div>`; // Otherwise, just add the day // De lo contrario, solo agrega el día
        }
    }

    // next month days
    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="day next">${j}</div>`; // Add the next month's days // Agrega los días del próximo mes
    }

  // run this function with every calendar render
  hideTodayBtn(); // Hide the today button if it's today // Oculta el botón de hoy si es hoy
    daysContainer.innerHTML = days; // Update the days container with the new days // Actualiza el contenedor de días con los nuevos días
}

renderCalendar(); // Initial render of the calendar // Renderizado inicial del calendario

nextBtn.addEventListener("click", () => {
    // increase current month by one
    currentMonth++; // Increase the current month by one // Incrementa el mes actual en uno
    if (currentMonth > 11) {
        // if month gets greater than 11 make it 0 and increase year by one
        currentMonth = 0; // If the month is greater than 11, reset to 0 and increase the year // Si el mes es mayor que 11, restablece a 0 y aumenta el año
        currentYear++; // Increase the year by one // Incrementa el año en uno
    }
    //rerender calendar
    renderCalendar(); // Re-render the calendar // Vuelve a renderizar el calendario
});

// prev month button
prevBtn.addEventListener("click", () => {
  // increase by one
  currentMonth--; // Decrease the current month by one // Decrementa el mes actual en uno
  // check if let than 0 then make it 11 and decrease year by one
  if (currentMonth < 0) {
    currentMonth = 11; // If the month is less than 0, set to 11 and decrease the year // Si el mes es menor que 0, establece a 11 y disminuye el año
    currentYear--; // Decrease the year by one // Decrementa el año en uno
  }
  renderCalendar(); // Re-render the calendar // Vuelve a renderizar el calendario
})

todayBtn.addEventListener("click", () => {
  // set month and year to current day
  currentMonth = date.getMonth(); // Set the current month to today's month // Establece el mes actual al mes de hoy
  currentYear = date.getFullYear(); // Set the current year to today's year // Establece el año actual al año de hoy
  // rerender calendar
  renderCalendar(); // Re-render the calendar // Vuelve a renderizar el calendario
})

// hides today btn if its today
function hideTodayBtn() {
  if (
    currentMonth === new Date().getMonth() &&
    currentYear === new Date().getFullYear()
  ) {
    todayBtn.style.display = "none"; // Hide the today button if it's today // Oculta el botón de hoy si es hoy
  } else {
    todayBtn.style.display= "flex"; // Show the today button if it's not today // Muestra el botón de hoy si no es hoy
  }
}

document.querySelectorAll('.sidebar-nav a').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior // Previene el comportamiento predeterminado del enlace

        // Remover la clase 'active' de todos los enlaces
        document.querySelectorAll('.sidebar-nav a').forEach(nav => nav.classList.remove('active')); // Remove the 'active' class from all links // Elimina la clase 'active' de todos los enlaces

        // Añadir la clase 'active' al enlace clickeado
        this.classList.add('active'); // Add the 'active' class to the clicked link // Agrega la clase 'active' al enlace clicado

        // Mostrar la sección correspondiente
        const targetSection = this.getAttribute('href').substring(1); // Get the target section from the link's href attribute // Obtiene la sección objetivo del atributo href del enlace
        document.querySelectorAll('.section').forEach(section => section.classList.remove('active')); // Remove the 'active' class from all sections // Elimina la clase 'active' de todas las secciones
        document.getElementById(targetSection).classList.add('active'); // Add the 'active' class to the target section // Agrega la clase 'active' a la sección objetivo
    });
});