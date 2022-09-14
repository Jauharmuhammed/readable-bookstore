function removeconfirm(ev, name) {
  ev.preventDefault();
  var urlToRedirect = ev.currentTarget.getAttribute('href');
  console.log(urlToRedirect);
  swal({
    title: "Are you sure?",
    text: ("Are you sure that you want to remove " + name + " from cart?"),
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {
        swal("Poof! " + name + " has been deleted!", {
          icon: "success",
        });
        window.location.href = urlToRedirect;
      }
    });
}