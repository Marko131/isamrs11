function flight_detail(flight_id) {
    window.location.href = "/flight/"+flight_id;
    $("#seats").text(flight_id);
    $.ajax({
        type: "GET",
        url: "/flight_seats/"+flight_id,
        success: function(response){
            $("#seats").text(response.id);
        }
    })

}