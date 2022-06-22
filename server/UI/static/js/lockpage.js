var timeOptions = {hour:"2-digit", minute:"2-digit", hour12: false};
var dateOptions = {weekday:"long", month:"short", day:"numeric"};

function runClock() {
    var fullDate = new Date();
    var time = fullDate.toLocaleTimeString("en-us", timeOptions);
    var date = fullDate.toLocaleDateString("en-us", dateOptions);
    var clkTime = document.getElementById("time");
    var clkDate = document.getElementById("date");
    clkTime.innerHTML = time;
    clkDate.innerHTML = date;
    setTimeout(runClock, 1000);
}
window.onload = runClock;
