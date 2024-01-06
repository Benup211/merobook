// $(document).ready(function() {
//     $('#postbtn').click(function() {
//         // Get the CSRF token value from the cookie
//         const csrfCookie = document.cookie.match(/csrftoken=([^;]+)/);
//         const csrftoken = csrfCookie ? csrfCookie[1] : '';
//         $.ajax({
//             url: '/',
//             type: 'POST',
//             beforeSend: function(xhr) {
//                 xhr.setRequestHeader('X-CSRFToken', csrftoken);
//             },
//             success: function(response) {
//                 $('#change').text(response.msg);
//                 alert("Value changed:"+(response.msg))
//             },
//             error:function(xhr,status,error){
//                 alert("error:"+error+",status:"+status)
//             }
//         });
//     });
// });
$('#wishlist_id').click(function(){
    const csrfCookie = document.cookie.match(/csrftoken=([^;]+)/);
    const csrftoken = csrfCookie ? csrfCookie[1] : '';
    const book=$('#wishlist_id').data('book')
    $.ajax({
        url: '/wishlist/',
        type: 'POST',
        data:{
            'book':book
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(response) {
            alert("Value changed:"+(response.msg))
        },
        error:function(xhr,status,error){
            alert("error:"+error+",status:"+status)
        }
    });
});