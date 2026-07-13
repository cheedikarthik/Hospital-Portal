document.addEventListener("DOMContentLoaded",()=>{

const date=document.getElementById("appointment-date");

if(!date)return;

const days=document.body.dataset.days||"Monday,Tuesday,Wednesday,Thursday,Friday";

const allowed=days.split(",");

date.min=new Date().toISOString().split("T")[0];

date.addEventListener("change",()=>{

const selected=new Date(date.value);

const names=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];

const day=names[selected.getDay()];

if(!allowed.includes(day)){

alert("Doctor is unavailable on "+day);

date.value="";

}

});

});