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