const chkPassword = document.getElementById('isPasswordVisible');
const inputPassword = document.getElementById('inputPassword');
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

chkPassword.addEventListener('change', function() {
  if (this.checked)
    inputPassword.type = 'text';
  else
    inputPassword.type = 'password';
}) 
