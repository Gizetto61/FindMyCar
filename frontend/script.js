document.querySelectorAll(".option").forEach(button => {
  button.addEventListener("click", () => {
    const value = button.dataset.value;
    alert(`Você selecionou: ${value}`);
  });
});
