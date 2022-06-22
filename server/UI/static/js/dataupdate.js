setInterval("updateData()",1000)
function updateData(){
    $.ajax({
        url:"data",
        type:"POST",
        dataType:"json",
        success: function(data){
            var heartrate_value=document.getElementById('heartrate_value');
            var spo2_value=document.getElementById('spo2_value')
            heartrate_value.innerHTML=data.heartrate
            spo2_value.innerHTML=data.spo2;
        }

    })
}