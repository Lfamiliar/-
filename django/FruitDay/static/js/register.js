
//点击跳转
$(function(){
    //声明一个变量
    var phoneStatus =1;

    $('#btnLogin').click(function () {
        location.href='{% url "login" %}';
    });
    //为name=uphone的框绑定的 blur 事件
    $('[name="uphone"]').blur(function () {
       if($(this).val().trim().length==0){
           return;
       }
        $.get('/check_uphone/',{
            'uphone':$(this).val()
            },function (data) {
                $("#uphone-show").html(data.msg);
                phoneStatus = data.status;
        },'json');
    });
    //为表单绑定submit事件
    $('#formReg').submit(function () {
        if(phoneStatus == 1){
            return false;
        }
        return true
    });
});
