function postTimeline(){
    var form = document.getElementById("timeline-form");
    var formData = new FormData(form);
    $.ajax({
        url: "/api/time_line_post",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(data, status, xhr){
            if (xhr.status == 200){
                Swal.fire({
                    icon: 'success',
                    title: 'Timeline Posted',
                    text: 'Your timeline has been posted successfully',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        location.reload();
                    }
                });
                setTimeout(function() {
                    location.reload();
                }, 2000);
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        location.reload();
                    }
                });
                console.log(data, xhr.status);
            }
        },
        error: function(data, status, xhr){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong!',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    location.reload();
                }
            });
            console.log(data, xhr.status);
        }
    })
}

function getTimeline(){
    var timelineContainer = document.getElementById("timeline-container");
    $.ajax({
        url: '/api/time_line_post',
        type: 'GET',
        success: function(data, status, xhr) {
            if (xhr.status == 200){
                var timeline = data["time_line_posts"]
                console.log(timeline);
                var timeline_html = '<p class="fw-bold sect mb-4"><i class="fa regular fa-code-fork"></i> Timeline</p>';
                for (var i = 0; i < timeline.length; i++){
                    if (i % 2 == 0) {
                        timeline_html += 
                        "<div class='row'>\
                            <div class='col-lg-6 col-md-6 py-2' data-aos='fade-up' data-aos-duration='1000'>\
                                <div class='card'>\
                                    <div class='card-body'>\
                                        <h5 class='card-title'>" + timeline[i]["content"] + "</h5>\
                                        <p class='card-text'>" + timeline[i]["name"] + " - " + timeline[i]["email"] + "</p>\
                                        <p class='card-subtitle mb-2'>" + timeline[i]["created_at"] + "</p>\
                                    </div>\
                                </div>\
                            </div><div class='col'></div>\
                        </div>"
                        
                    } else {
                        timeline_html += 
                        "<div class='row'>\
                            <div class='col'></div>\
                            <div class='col-lg-6 col-md-6 py-2' data-aos='fade-up' data-aos-duration='1000'>\
                                <div class='card'>\
                                    <div class='card-body'>\
                                    <h5 class='card-title'>" + timeline[i]["content"] + "</h5>\
                                    <p class='card-text'>" + timeline[i]["name"] + " - " + timeline[i]["email"] + "</p>\
                                    <p class='card-subtitle mb-2'>" + timeline[i]["created_at"] + "</p>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>"
                    }
                }
                timelineContainer.innerHTML = timeline_html;
            }
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
}