// Seleciona os botões e os formulários
const btnIndividual = document.getElementById("btn-individual");
const btnTime = document.getElementById("btn-time");
const formIndividual = document.getElementById("form-individual");
const formTime = document.getElementById("form-time");

// Função para mostrar o formulário Individual
btnIndividual.addEventListener("click", function () {
  formIndividual.style.display = "block";
  formTime.style.display = "none";

  btnIndividual.classList.add("active");
  btnTime.classList.remove("active");
});

// Função para mostrar o formulário de Time
btnTime.addEventListener("click", function () {
  formIndividual.style.display = "none";
  formTime.style.display = "block";

  btnTime.classList.add("active");
  btnIndividual.classList.remove("active");
});

function styleAlert(element) {
  const category = element.dataset.category;
  if (!category) {
    return;
  }
  element.style.backgroundColor = `var(--${category})`;
}
const alerts = document.querySelectorAll(".alert");
alerts.forEach((alert) => {
  styleAlert(alert);

  const close_btn = alert.querySelector(".close-btn");
  if (close_btn) {
    close_btn.addEventListener("click", () => {
      alert.style.display = "none";
    });
  }
});
