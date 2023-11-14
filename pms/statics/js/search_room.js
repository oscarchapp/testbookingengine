Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

function onDateUpdate(checkin, checkout){
    const date1=new Date(checkin)
    const date2=new Date(checkout)
    document.querySelector("#total-days").innerHTML=(date2.getTime() - date1.getTime())/(1000*3600*24)

}

const idBookingCheckoutElement = document.querySelector("#id_booking-checkout");
if (idBookingCheckoutElement) {
    onDateUpdate(document.querySelector("#id_booking-checkin").value, idBookingCheckoutElement.value);
    idBookingCheckoutElement.addEventListener("change", (e) => {
        onDateUpdate(document.querySelector("#id_booking-checkin").value, idBookingCheckoutElement.value);
    });
}

const idCheckoutElement = document.querySelector("#id_checkout");
if (idCheckoutElement) {
  idCheckoutElement.addEventListener("change", (e) => {
      onDateUpdate(document.querySelector("#id_checkin").value, idCheckoutElement.value);
      document.querySelector("#id_guests").focus();
  });
}
// document.querySelector("#id_checkin").addEventListener("change",(e)=>{
//     const checkout=document.querySelector("#id_checkout")

//     const tomorrow=new Date(e.target.value).addDays(1).toISOString().split('T')[0]
//     if(e.target.value>checkout.value){
//         checkout.setAttribute("value",tomorrow)
        
//     }
//     onDateUpdate()
//     checkout.setAttribute("min",tomorrow)
//     checkout.focus()
// })
