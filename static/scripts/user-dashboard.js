  function logoutConfirm(ev) {
    ev.preventDefault();
  var urlToRedirect = ev.currentTarget.getAttribute('href');
  console.log(urlToRedirect);
  swal({
    title: "Are you sure?",
  text: ("Are you sure that you want to logout?"),
  buttons: true,
  className : 'swal-custom'
      })
        .then((willDelete) => {
          if (willDelete) {
    window.location.href = urlToRedirect;
          }
        });
    }

  function deleteAddress(ev) {
    ev.preventDefault();
  var urlToRedirect = ev.currentTarget.getAttribute('href');
  console.log(urlToRedirect);
  swal({
    title: "Are you sure?",
  text: ("Are you sure that you want to delete this address?"),
  buttons: true,
  className : 'swal-custom'
      })
        .then((willDelete) => {
          if (willDelete) {
            window.location.href = urlToRedirect;
          }
        });
    }
