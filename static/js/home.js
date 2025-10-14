// Dark Mode Toggle
const toggle = document.getElementById("darkToggle");
toggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
});

// Live Counter Animation
function countUp(id, end) {
  let start = 0;
  const el = document.getElementById(id);
  const duration = 2000;
  const step = Math.ceil(end / (duration / 16));
  const counter = setInterval(() => {
    start += step;
    if (start >= end) {
      el.textContent = end;
      clearInterval(counter);
    } else {
      el.textContent = start;
    }
  }, 16);
}

window.onload = () => {
  countUp("years", 15);
  countUp("customers", 5000);
  countUp("cars", 3400);
};
