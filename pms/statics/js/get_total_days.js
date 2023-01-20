Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

function onDateUpdate(){
    const date1=new Date(document.querySelector("#id_booking-checkin").value)
    const date2=new Date(document.querySelector("#id_booking-checkout").value)
    document.querySelector("#total-days").innerHTML=(date2.getTime() - date1.getTime())/(1000*3600*24)

}

document.querySelector("#id_booking-checkout").addEventListener("change",(e)=>{
    onDateUpdate()
})
onDateUpdate()