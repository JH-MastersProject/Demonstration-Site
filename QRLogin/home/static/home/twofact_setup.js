$( document ).ready(function() {
    startScanning();
});


function startScanning() {
  $("<h1>Scan Your Two-Factor Code</h1>").insertBefore(".scanner")
  $(".initial-options").remove();


  let scanner = new Instascan.Scanner({ video: document.getElementById('preview'), mirror:false });
  scanner.addListener('scan', function (content) {
    submitQR(content);
    scanner.stop();
  });
  Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
      scanner.start(cameras[0]);
    } else {
      console.error('No cameras found.');
    }
  }).catch(function (e) {
    console.error(e);
  });
}

function submitQR(content) {
  $('.preview').remove();

  $.ajax({
    type: "GET",
    url: "add_existing_2fa_code",
    data: {
      "qr": content
    },
    success: function (data) {
      alert("QR Code has been added to your account")
      window.location.replace("/")
    },
    error: function (data) {
      alert("Invalid QR code")
      window.location.replace("")
    },
  });

}
