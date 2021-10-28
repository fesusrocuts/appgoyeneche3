function createprocess(e){
  console.log("load to create process...");
  //debugger
  $(e.target).addClass("disabled")
  $(e.target).unbind("click")
  let _key = $(e.target).attr("uuid");
  let _path = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
  $.ajax({
    type: 'POST',
    crossDomain: true,
    datatype: 'jsonp',
    url: _path + $(".next").val(),
    data: JSON.stringify({
        "key": _key
    }),
    header: {
        "Access-Control-Allow-Headers" : "X-PINGOTHER"
    },
    contentType: 'application/json',
    success: function (data) {
        $(".cover-container").html(data);
        //setTimeout(function(){
          $(".btn_step1").bind("click",createprocess);
          $(".btn_save").bind("click",saveForm);
          $(".btn_step1_test").bind("click",settingConn);
          $(".upfile").bind("click", upload)

        //},2000)
        //console.log(data);
    }
  });

  /*[0, 1, 2, 3, 4].reduce(function(accumulator, currentValue, currentIndex, array) {
    console.log("accumulator " + accumulator);
    console.log("currentValue " + currentValue);
    console.log("currentIndex " + currentIndex);
    console.log("array ");
    console.log(array);
    return accumulator + currentValue;
  });*/
  console.log(_key);
}
function saveForm(e){
  console.log("saveForm...");
  //debugger
  let _key = $(e.target).attr("uuid");
  let _path = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
  $.ajax({
    type: 'POST',
    crossDomain: true,
    datatype: 'jsonp',
    url: _path + $(".act").val(),
    data: JSON.stringify({
        "key": _key,
        "data": $("form[class="+_key+"]").serializeArray()
    }),
    header: {
        "Access-Control-Allow-Headers" : "X-PINGOTHER"
    },
    contentType: 'application/json',
    success: function (data) {
        //$(".cover-container").html(data);
        //setTimeout(function(){
          //$(".btn_step1").bind("click",createprocess);
          //$(".btn_step1_test").bind("click",settingConn);
        //},2000)
        console.log("saving...");
        console.log(data);
        $(".setting").html("Save status: " + data.status);
    }
  });

  /*[0, 1, 2, 3, 4].reduce(function(accumulator, currentValue, currentIndex, array) {
    console.log("accumulator " + accumulator);
    console.log("currentValue " + currentValue);
    console.log("currentIndex " + currentIndex);
    console.log("array ");
    console.log(array);
    return accumulator + currentValue;
  });*/
  console.log(_key);
}
function settingConn(e){
  console.log("testing...");
  //debugger
  let _key = $(e.target).attr("uuid");
  let _path = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
  //let _path2 = window.location.protocol + "//" + window.location.hostname + ':5001' ;

  let __toEmail_verified = 0;
  let __toUrl_verified = 0;
  $(".__toEmail").filter(function(){
    if(this.value.length > 2 && this.value.indexOf("@") > -1){
      __toEmail_verified = 1
      $(".__toEmail").css("background","#ffffff");
    }else{
      $(".__toEmail").css("background","#ffcc00");
    }
  })

  /*$(".__toUrl").filter(function(){
    if(this.value.length > 10 && this.value.indexOf("://") > 3){
      __toUrl_verified = 1
      $(".__toUrl").css("background","#ffffff");
    }else{
      $(".__toUrl").css("background","#ffcc00");
    }
  })*/

  //if (__toUrl_verified === 1 && __toEmail_verified === 1) {
  if (__toEmail_verified === 1) {

    $.ajax({
      type: 'POST',
      crossDomain: true,
      datatype: 'jsonp',
      url: _path + "/api/v1/settingConn",
      data: JSON.stringify({
          "key": _key,
          "__toUrl": "",
          "__toEmail": $(".__toEmail").val(),
          "data": []
      }),
      header: {
          "Access-Control-Allow-Headers" : "X-PINGOTHER"
      },
      contentType: 'application/json',
      success: function (data) {
          $(".setting").html(data);
          //console.log(data);
      }
    });

    /*[0, 1, 2, 3, 4].reduce(function(accumulator, currentValue, currentIndex, array) {
      console.log("accumulator " + accumulator);
      console.log("currentValue " + currentValue);
      console.log("currentIndex " + currentIndex);
      console.log("array ");
      console.log(array);
      return accumulator + currentValue;
    });*/
    console.log(_key);
  }else{
    $(".setting").html("Missing fields to complete");
  }
}

function upload(){
  console.log("fn upload")
  var formData = new FormData();
  formData.append('file', $('input[type=file]')[0].files[0]);
  $.ajax({
     url: '/app1/form/debt_portfolio/file',
     type: 'POST',
     data: formData,
     async: false,
     cache: false,
     contentType: false,
     enctype: 'multipart/form-data',
     processData: false,
     success: function (response) {
       $(".setting").html(response);
     }
  });
  return false;
}

if (typeof jQuery === 'function') {
  $(document).ready(function () {
    $(".btn_step1").bind("click",createprocess);
    $(".btn_save").bind("click",saveForm);
    $(".upfile").bind("click", upload)
    //$(".btn_step1_test").bind("click",settingConn);
  })
}
