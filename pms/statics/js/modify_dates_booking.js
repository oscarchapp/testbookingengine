var $ = jQuery.noConflict();
// document.querySelector('#id_booking-checkin').addEventListener('change', checkDates)
document.querySelector('#id_booking-checkout').addEventListener('change', checkDates);
const submitButton$ = document.querySelector("#submit_button");
submitButton$.setAttribute("disabled",true);
function hideLoader(){
    const loader$ = document.querySelector('#loader');
    loader$.classList.add("hidden");
}
function showLoader(){
    const loader$ = document.querySelector('#loader');
    loader$.classList.remove("hidden");
}

async function checkDates(){
    showLoader();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var formData = new FormData();

    formData.append("checkin", document.querySelector('#id_booking-checkin').value);
    formData.append("checkout", document.querySelector('#id_booking-checkout').value);
    formData.append("code", document.querySelector('#booking_code').value);
    formData.append("guests", document.querySelector('#guests_booking').value);
    formData.append("room_id", document.querySelector('#id_booking-room').value);

    formData.append("csrfmiddlewaretoken", csrftoken);
    //remove hidden to not add unlimited hidden class
    document.querySelector('#error_message').classList.remove('hidden');
    $.ajax({
        url: `/dates/available`,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        error: function(error) {
            document.querySelector('#error_message').classList.remove('hidden')
            hideLoader();
        },
        success: function(data) {
            response = data;
            response.IsAvailable ? document.querySelector('#error_message').classList.add('hidden') : document.querySelector('#error_message').classList.remove('hidden');
            response.IsAvailable ? submitButton$.removeAttribute("disabled"):submitButton$.setAttribute("disabled",true);
            if(response.room_for_change !== 0 ){
                const selector$$ = document.querySelector('#id_booking-room');
                selector$$.value=response.room_for_change
            }
            hideLoader()
        }
    });

}

window.onload = function() {
}