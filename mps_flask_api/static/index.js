let callendarBox = document.getElementById("callendar-box");
let days = callendarBox.children
let currentMonth = new Date().getUTCMonth();
console.log(days);

for (let i=0; i < days.length; i++){
    let month =  new Date (days[i].innerText).getUTCMonth();
    let obj = {
        "month":month, 
        "current-month": currentMonth,

    }
    console.log(obj);
    if (month !=  currentMonth){
        days[i].style.backgroundColor = 'lightslategray';
    }
}