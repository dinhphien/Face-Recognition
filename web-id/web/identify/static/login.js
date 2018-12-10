$(document).ready(function () {

	const captureVideoButton =document.querySelector('#captureVideo');
	const screenshotButton = document.querySelector('#takePicture');
	const loginButton = document.querySelector('#login_button');
	const video = document.querySelector('#screenshot video');

	const canvas = document.querySelector('#screenshot canvas');
	const context = canvas.getContext('2d');
	const constraints = {
		video: {width:400, height:120}
	};
	captureVideoButton.onclick = function() {
	  navigator.mediaDevices.getUserMedia(constraints).
	  then(handleSuccess).catch(handleError);
    };
	function handleSuccess(camera) {
	  screenshotButton.disabled = false;
	  loginButton.disabled = false;
	  video.srcObject = camera;

	  document.getElementById("takePicture").addEventListener("click", function() {
			context.drawImage(video, 0, 0, 380, 120);

	  });
	  
	};
	function handleError(error) {
	  console.error('Error: ', error);
	};


	function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

        var blob = new Blob(byteArrays, {type: contentType});
        return blob;
    };





	loginButton.onclick = function () {
		// console.log(canvas.toDataURL());
		// alert(document.getElementById("Userlogin").value);
		// var imag = canvas.toDataURL("image/png");
		// imag = imag.replace(/^data:image\/(png|jpg);base64,/, "");
        console.log(document.getElementById("Userlogin").value);
        var ImageURL = canvas.toDataURL("image/png");
        // Split the base64 string in data and contentType
		var block = ImageURL.split(";");
		// Get the content type of the image
		var contentType = block[0].split(":")[1];// In this case "image/gif"
		// get the real base64 content of the file
		var realData = block[1].split(",")[1];// In this case "R0lGODlhPQBEAPeoAJosM...."

		// Convert it to a blob to upload
		var blob = b64toBlob(realData, contentType);
        console.log(blob);
		// upload using jQuery
		let formData = new FormData();
		console.log()
		formData.append('id',document.getElementById("Userlogin").value);
		formData.append('image', blob);


        $.ajax({
            url: '/api/upload_video/', // replace with your own server URL
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function (response) {
                console.log('out put of post image');
                console.log(response);
                if (response.status === 'success') {
                    // $('#captureVideo').attr('disabled', 'disabled');
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
	}

});