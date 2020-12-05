function createTable(sortedResult){
  var table_body = $("#table-body");

  for (var i = 1; i <= sortedResult.length; i++){
    var tr = $('<tr><th scope="row">' + i + '</th><td>' + sortedResult[i-1][0] + '</td><td>' + sortedResult[i-1][1] + '</td></tr>');
    table_body.append(tr[0]);
  }
}

$("#image-form").submit(function(event) {

    var formData = new FormData(this);
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
      url: window.location.href.slice(0,-1) + $(this).attr("action"),
      data: formData,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function(data) {
        if(data['result'] == "Empty File!"){
          alert("Invalid file");
        }else if(data['result'] == "Recognition task failed!"){
          alert("Recognition task failed!");
        }else{
          result = data['result'];
          var arrayToBeSorted = [];
          for (const type in result){
            arrayToBeSorted.push([type, result[type]]);
          }
          arrayToBeSorted.sort(function(a,b){
            return b[1] - a[1];
          });
          $("#result-text").text(arrayToBeSorted[0][0]);
          $("#result").show();
          $("#result-table").show();
          createTable(arrayToBeSorted);
        }
      }
    });
    return false;
  });

$("#file-chooser").change(function(){
  if(this.files && this.files[0]){
    var reader = new FileReader();
    $("#result-text").text("");
    $("#table-body").empty();
    $("#result-table").hide();
    reader.onload = function (e) {
          $('#img-previewer').attr('src', e.target.result);
    }
    $("#file-name").text(this.files[0].name);

    reader.readAsDataURL(this.files[0]);
  }
})
