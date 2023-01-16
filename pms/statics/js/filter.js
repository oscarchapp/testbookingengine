$(document).ready(function() {
  $("#search-form").submit(function(event) {
    event.preventDefault();

    var searchValue = $("#search-input").val();

    $.ajax({
      url: '/search/room/ajax/',
      type: 'GET',
      data: { 'query': searchValue },
      success: function(data) {
        $("#rooms-container").html(data);
      }
    });
  });
});
