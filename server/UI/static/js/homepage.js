$(document).ready(function(){
var timeOptions = {hour:"2-digit", minute:"2-digit", hour12: false};
function runClock() {
    var fullDate = new Date();
    var time = fullDate.toLocaleTimeString("en-us", timeOptions);
    var clkTime = document.getElementById("time");
    clkTime.innerHTML = time;
    setTimeout(runClock, 1000);
}
window.onload = runClock;

});