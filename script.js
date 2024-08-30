const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

menu.addEventListener('click', function() {
	menu.classList.toggle('is-active');
	menuLinks.classList.toggle('active');
});


document.addEventListener('DOMContentLoaded', function() {
    const mesElemento = document.getElementById('mes-año');
    const diasElemento = document.getElementById('dias-del-mes');

    const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    let fecha = new Date();
    let mesActual = fecha.getMonth();
    let añoActual = fecha.getFullYear();

    function cargarCalendario(mes, año) {
        mesElemento.textContent = `${meses[mes]} ${año}`;
        diasElemento.innerHTML = '';

        const primerDíaMes = new Date(año, mes, 1).getDay();
        const díasEnMes = new Date(año, mes + 1, 0).getDate();

        const primerDía = primerDíaMes === 0 ? 6 : primerDíaMes - 1;

        for (let i = 0; i < primerDía; i++) {
            diasElemento.innerHTML += `<li></li>`;
        }

        for (let i = 1; i <= díasEnMes; i++) {
            const diaElemento = document.createElement('li');
            diaElemento.textContent = i;

            const fechaStr = `${i}/${mes + 1}/${año}`;
            const reserva = localStorage.getItem(fechaStr);

            if (reserva) {
                diaElemento.classList.add('reservado'); // Marcar como reservado
                diaElemento.title = 'Este día ya está reservado';
            } else {
                diaElemento.addEventListener('click', () => {
                    mostrarFormularioReserva(fechaStr);
                });
            }

            if (i === fecha.getDate() && mes === mesActual && año === añoActual) {
                diaElemento.classList.add('hoy'); // Marcar el día actual
            }

            diasElemento.appendChild(diaElemento);
        }
    }

    function mostrarFormularioReserva(fecha) {
        const nombre = prompt("Ingrese su nombre para reservar el día:");
        if (nombre) {
            const descripcion = prompt("Ingrese una descripción para la reserva:");
            const reserva = {
                fecha: fecha,
                nombre: nombre,
                descripcion: descripcion
            };
            localStorage.setItem(fecha, JSON.stringify(reserva));
            alert(`¡Reserva realizada para el ${fecha}!`);
            cargarCalendario(mesActual, añoActual); // Recargar el calendario para actualizar el estado
        }
    }

    cargarCalendario(mesActual, añoActual);
});

