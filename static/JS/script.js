const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

menu.addEventListener('click', function() {
	menu.classList.toggle('is-active');
	menuLinks.classList.toggle('active');
});


// calendar
const daysContainer = document.querySelector(".days"),
nextBtn = document.querySelector(".next-btn"),
prevBtn = document.querySelector(".prev-btn"),
month = document.querySelector(".month");
todayBtn = document.querySelector(".today-btn");

const months = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
];

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// get current date
const date = new Date();

//get current month
let currentMonth = date.getMonth();

// get current year
let currentYear = date.getFullYear();

console.log(date, currentMonth, currentYear)

// function to render days
function renderCalendar() {

	//get previous month current month and next month days
	date.setDate(1);
	const firstDay = new Date(currentYear, currentMonth, 1);
	const lastDay = new Date(currentYear, currentMonth + 1, 0)
	const lastDayIndex = lastDay.getDay();
	const lastDayDate = lastDay.getDate();
	const prevLastDay = new Date(currentYear, currentMonth, 0);
	const prevLastDayDate = prevLastDay.getDate();
	const nextDays = 7 - lastDayIndex - 1;

	//update current year and month in header
	month.innerHTML = `${months[currentMonth]} ${currentYear}`;

	// update days html
	let days = "";

	//prev days html
	for (let x = firstDay.getDay(); x > 0; x--) {
		days += `<div class="day prev">${prevLastDayDate - x + 1}</div>`;
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
			days += `<div class="day today">${i}</div>`;
		} else {
			// else don`t add today
			days += `<div class="day ">${i}</div>`;
		}
	}

	// next month days
	for (let j = 1; j <= nextDays; j++) {
		days += `<div class="day next">${j}</div>`;
	}

  // run this function with every calendar render
  hideTodayBtn();
	daysContainer.innerHTML = days;

}

renderCalendar();

nextBtn.addEventListener("click", () => {
	// increase current month by one
	currentMonth++;
	if (currentMonth > 11) {
		// if month gets greater than 11 make it 0 and increase year by one
		currentMonth = 0;
		currentYear++;
	}
	//rerender calendar
	renderCalendar();
});


// prev month button
prevBtn.addEventListener("click", () => {
  // increase by one
  currentMonth--;
  // check if let than 0 then make it 11 and decrease year by one
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();
})

todayBtn.addEventListener("click", () => {
  // set month and year to current day
  currentMonth = date.getMonth();
  currentYear = date.getFullYear();
  // rerender calendar
  renderCalendar();
})


// hides today btn if its today


function hideTodayBtn() {
  if (
    currentMonth === new Date().getMonth() &&
    currentYear === new Date().getFullYear()
  ) {
    todayBtn.style.display = "none";
  } else {
    todayBtn.style.display= "flex";
  }
}