function blockconfirm(ev, name) {
  ev.preventDefault();
  var urlToRedirect = ev.currentTarget.getAttribute('href'); 
  console.log(urlToRedirect);
  swal({
    title: "Are you sure?",
    text: ("Are you sure that you want to block " + name + "?"),
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {
        swal("Poof! User " + name + " has been blocked!", {
          icon: "success",
        });
        window.location.href = urlToRedirect;
      }
    });
}

function unblockconfirm(ev, name) {
  ev.preventDefault();
  var urlToRedirect = ev.currentTarget.getAttribute('href'); 
  console.log(urlToRedirect);
  swal({
    title: "Are you sure?",
    text: ("Are you sure that you want to unblock " + name + "?"),
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {
        swal("Poof! User " + name + " has been unblocked!", {
          icon: "success",
        });
        window.location.href = urlToRedirect;
      }
    });
}

function deleteconfirm(ev, name) {
  ev.preventDefault();
  var urlToRedirect = ev.currentTarget.getAttribute('href'); 
  console.log(urlToRedirect);
  swal({
    title: "Are you sure?",
    text: ("Are you sure that you want to delete " + name + "?, All data related to " + name + " will be also deleted!"),
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

