function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrf_token = getCookie('csrftoken');


$(document).ready(function () {

  $('#rzp-button').click(function (e) {
    e.preventDefault();

    

    $.ajax({
      method: 'GET',
      url: '/orders/proceed-order',
      success: function (responsedata) {
        console.log(responsedata)

        var options = {
          "key": "rzp_test_U071hjpAOlEkCH", // Enter the Key ID generated from the Dashboard
          "amount": responsedata.total * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
          "currency": "INR",
          "name": "Readable Bookstore",
          "description": "Thank You for Shopping with us.",
          "image": "/Users/Jauhar/Web development/django/ecom project/static/images/readable-icon-black-1.jpg",
          // "order_id": responsedata.order_id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
          "handler": function (response_razorpay) {

            data = {
              "payment_method": "razorpay",
              "payment_id": response_razorpay.razorpay_payment_id,
              "payment_amount": responsedata.total,
            }
            console.log(data)
            $.ajax({
              method: "POST",
              url: "/orders/place-order/payment/",
              headers: {
                "X-CSRFToken": csrf_token
              },
              data: data,
              success: function (responsepayment) {
                swal("Congratulations!", responsepayment.status, "success").then((value) => {
                  window.location.href = '/orders/order-success/' +'?order_id='+responsepayment.order_id
                });
              }
            });
  
          },

          "prefill": {
            "name": responsedata.full_name,
            "email": responsedata.email,
            "contact": responsedata.mobile
          },
          "notes": {
            "address": "Razorpay Corporate Office"
          },
          "theme": {
            "color": "#3399cc"
          }
        };
        var rzp = new Razorpay(options);
        rzp.open();
      }
    });


  });


});

