function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
$(document).ready(function(){
	const video = document.querySelector('video');
	const captureVideoButton =document.querySelector('#captureVideo');
	// const stopVideoButton =document.querySelector('#stopVideo');
    const VIDEO_TIME = 5;
	const constraints = {
	   video: {width: 400, height: 240}
	};

	captureVideoButton.onclick = function() {
	  navigator.mediaDevices.getUserMedia(constraints).
	  then(handleSuccess).catch(handleError);
    };
	function handleSuccess(camera) {
	  // stopVideoButton.disabled = false;

	  video.srcObject = camera;

	  // recording configuration/hints/parameters
        let recordingHints = {
            type: 'video',
            disableLogs: true
        };
        // initiating the recorder
        let recorder = RecordRTC(camera, recordingHints);
        // starting recording here
        recorder.startRecording();
        // auto stop recording after 5 seconds
        let milliSeconds = VIDEO_TIME * 1000;
        setTimeout(function(){
        	// stop recording
            recorder.stopRecording(function () {
            	 // get recorded blob
                let blob = recorder.getBlob();
                console.log(document.querySelector('#Username').value);

                // let id = $(self).data()['id'];
                let fileName = document.querySelector('#Username').value + ".webm";

                let fileObject = new File([blob], fileName, {
                    type: 'video/webm'
                });
                let formData = new FormData();

                formData.append('id', document.querySelector('#Username').value);

                // recorded data
                formData.append('video-train', fileObject);

                // file name
                formData.append('video-filename', fileObject.name);
                console.log(formData);
                console.log("Video size upload: " + bytesToSize(fileObject.size));

                // upload using jQuery
                $.ajax({
                    url: '/register', // replace with your own server URL
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    type: 'POST',
                    success: function (response) {
                        console.log('out put of post video');
                        console.log(response);
                        if (response.status === 'success') {
                            $('#captureVideo').attr('disabled', 'disabled');
                            toastr.success(response.message, 'Success');
                        } else if (response.status === 'warning') {
                            toastr.warning(response.message, 'Warning');
                        }
                    }
                });

                // release camera
                video.srcObject = null;
                camera.getTracks().forEach(function (track) {
                    track.stop();
                });
                 // you can preview recorded data on this page as well
                video.src = URL.createObjectURL(blob);   
            })

        }, milliSeconds);
	};
	function handleError(error) {
	  console.error('Error: ', error);
	};
	// stopVideoButton.onclick = function () {
	// 	video.pause();
	// }

});