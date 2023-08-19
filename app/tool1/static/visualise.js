$(document).ready(function() {
  
  function get_rsid() {
    $.ajax({
      type: 'GET',
      url : urlGetRsid,
      dataType: 'json',
      success: function (data) {
        print("chocolate")
      }
    })
  }

});