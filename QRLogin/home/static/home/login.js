$(document).on('submit', '.login', function (e) {
  e.preventDefault();

  var data = $('.login').serializeArray()
  var username = data[1]["value"]
  var password = data[2]["value"]
  $('.login').remove();
  $.ajax({
    type: "GET",
    url: "attempt_login",
    data: {
      "username": username, "password": password
    },
    success: function (data) {
      if (data["twofa"]) {
        count = data["twofa"]
        // We need to handle 2fa
        if(count == -1){
            alert("Your account has been locked")
            window.location.replace("/")
            return
        }
        $("<h1 class='text-center'>Scan Your Two Factor Code</h1>").insertBefore(".scanner")

        handle_2fa(username, password, count);
        return;
      } else {
        window.location.replace("/")
      }
    },
    error: function (data) {
      alert("Invalid Username or Password")
      window.location.replace("")
    },
  });

});

function handle_2fa(username, password, count) {

  let scanner = new Instascan.Scanner({ video: document.getElementById('preview'), mirror:false });
  var qrs = [];
  scanner.addListener('scan', function (content) {
    qrs.push(content)
    count--;
    if (count!=0){
        alert("Scan next qr")
    }else{
        scanner.stop();
        submit_2fa(qrs, username, password);
    }
    //submit_2fa(content, username, password);


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

function submit_2fa(content, username, password) {
  $.ajax({
    type: "GET",
    url: "attempt_2fa_login",
    traditional:true,
    data: {
      "qr": content, "username": username, "password": password
    },
    success: function (data) {
      if (data["error"]) {
        alert("Invalid Code")

      }
      window.location.replace("/")

    },
    error: function (data) {
      alert("Invalid Code")
      //window.location.replace("/")

    },
  });

}