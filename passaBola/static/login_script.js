const chkPassword = document.getElementById('isPasswordVisible');
const inputPassword = document.getElementById('inputPassword');

chkPassword.addEventListener('change', function() {
  if (this.checked)
    inputPassword.type = 'text';
  else
    inputPassword.type = 'password';
}) 