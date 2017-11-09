// setTimeout("location.reload()", 100);
var counter = 0;
window.setInterval("refreshDiv()", 100);
function refreshDiv() {
    // counter += 1
    // document.getElementById("status").innerHTML = "refresh "+counter;
    $.ajax({
        url: '{% url "judge:submission_status_ajax" 6 %}',
        // url: '/judge/submission/status/6/ajax/',
        dataType: 'json',
        success: function(result) {
            counter += 1;
            if (result) {
                document.getElementById("status").innerHTML = result.status + counter;
            } else {
                document.getElementById("status").innerHTML = "Error";
            }
        },
        error: function (error) {
            document.getElementById("status").innerHTML = "ErrorError"+counter;
        }
    });
}
