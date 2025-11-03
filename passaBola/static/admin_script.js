const btnHome = document.getElementById("btnHome");
const btnWriteEvent = document.getElementById("btnWriteEvent");
const btnMyEvent = document.getElementById("btnMyEvents");

btnHome.addEventListener('click', function () {
  btnHome.classList.add('bg-pb-primary');
  btnWriteEvent.classList.remove('bg-pb-primary');
  btnMyEvent.classList.remove('bg-pb-primary');
});

btnWriteEvent.addEventListener('click', function () {
  btnHome.classList.remove('bg-pb-primary');
  btnWriteEvent.classList.add('bg-pb-primary');
  btnMyEvent.classList.remove('bg-pb-primary');
});

btnMyEvent.addEventListener('click', function () {
  btnHome.classList.remove('bg-pb-primary');
  btnWriteEvent.classList.remove('bg-pb-primary');
  btnMyEvent.classList.add('bg-pb-primary');
});