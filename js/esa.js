/* ========= CONFIGURACIÓN ESA: datos de contacto en un solo lugar ========= */
const ESA = {
  whatsapp: "59177666653",          // código 591 + número, sin espacios ni "+"
  correo:   "comercial@esa.com.bo",
  mensajeWA:"Hola ESA, quiero más información sobre energía solar."
};

const waURL = (txt) => "https://wa.me/" + ESA.whatsapp + "?text=" + encodeURIComponent(txt || ESA.mensajeWA);

document.querySelectorAll(".js-wa").forEach(a => { a.href = waURL(); a.target = "_blank"; a.rel = "noopener"; });
document.querySelectorAll(".js-mail").forEach(a => { a.href = "mailto:" + ESA.correo; });
document.querySelectorAll(".js-anio").forEach(e => e.textContent = new Date().getFullYear());

/* Menú en celular */
const burger = document.querySelector(".burger"), menu = document.querySelector(".menu");
if (burger) burger.addEventListener("click", () => {
  const abierto = menu.classList.toggle("abierto");
  burger.setAttribute("aria-expanded", abierto);
  burger.setAttribute("aria-label", abierto ? "Cerrar menú" : "Abrir menú");
});

/* Formularios: arman el mensaje y abren WhatsApp (no necesitan servidor) */
document.querySelectorAll("form[data-asunto]").forEach(form => {
  form.addEventListener("submit", e => {
    e.preventDefault();
    const lineas = ["Hola ESA, " + form.dataset.asunto + "."];
    form.querySelectorAll("input, select, textarea").forEach(c => {
      if (!c.name || !c.value.trim()) return;
      const etiqueta = c.closest("label") ? c.closest("label").firstChild.textContent.trim() : c.name;
      lineas.push(etiqueta + ": " + c.value.trim());
    });
    if (typeof gtag === "function") gtag("event", "generate_lead", { form_type: form.dataset.asunto, page: location.pathname });
    window.open(waURL(lineas.join("\n")), "_blank");
  });
});

/* Fotos: si el archivo existe en /img se muestra; si no, queda el fondo provisional */
document.querySelectorAll("[data-foto]").forEach(el => {
  const src = new URL(el.dataset.foto, location.href).href, img = new Image();
  img.onload = () => { el.style.setProperty("--img", `url("${src}")`); el.classList.add("ok"); };
  img.src = src;
});

/* Carrusel de la portada (Inicio) */
const carrusel = document.querySelector(".carrusel");
if (carrusel) {
  const slides = [...carrusel.querySelectorAll(".slide")];
  const botones = [...carrusel.querySelectorAll(".puntos button:not(.pausa)")];
  const pausa = carrusel.querySelector(".pausa");
  let pausado = false;
  let actual = 0, timer = null;
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mostrar = i => {
    actual = (i + slides.length) % slides.length;
    slides.forEach((s, k) => { s.classList.toggle("activa", k === actual); s.setAttribute("aria-hidden", k !== actual); s.inert = k !== actual; });
    botones.forEach((b, k) => b.setAttribute("aria-pressed", k === actual));
  };
  const iniciar = () => { clearInterval(timer); if (!quieto && !pausado) timer = setInterval(() => mostrar(actual + 1), 7000); };
  if (pausa) {
    if (quieto) pausa.hidden = true;
    pausa.addEventListener("click", () => {
      pausado = !pausado;
      pausa.setAttribute("aria-pressed", pausado);
      pausa.setAttribute("aria-label", pausado ? "Reanudar el carrusel" : "Pausar el carrusel");
      pausa.textContent = pausado ? "▶" : "❚❚";
      iniciar();
    });
  }
  botones.forEach((b, k) => b.addEventListener("click", () => { mostrar(k); iniciar(); }));
  carrusel.addEventListener("mouseenter", () => clearInterval(timer));
  carrusel.addEventListener("mouseleave", iniciar);
  carrusel.addEventListener("focusin", () => clearInterval(timer));
  mostrar(0); iniciar();
}

/* Flechas de los carruseles de tarjetas */
document.querySelectorAll(".deslizar").forEach(d => {
  const pista = d.querySelector(".pista");
  d.querySelectorAll(".flecha").forEach(b => b.addEventListener("click", () => {
    const paso = pista.clientWidth * 0.8 * (b.classList.contains("izq") ? -1 : 1);
    pista.scrollBy({ left: paso, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }));
});

/* Medición: clics a WhatsApp y a llamadas (solo si Google Analytics está activo) */
document.addEventListener("click", e => {
  const a = e.target.closest("a");
  if (!a || typeof gtag !== "function") return;
  const lugar = a.classList.contains("wa") ? "boton_flotante"
    : a.closest(".franja-atencion") ? "franja_celular"
    : a.closest("header") ? "menu"
    : a.closest("footer") ? "pie"
    : a.closest(".contacto-final") ? "contacto_final"
    : a.closest("section")?.id || "pagina";
  if (a.href.includes("wa.me")) gtag("event", "whatsapp_clicked", { location: lugar, page: location.pathname });
  else if (a.href.startsWith("tel:")) gtag("event", "phone_clicked", { location: lugar, page: location.pathname });
});
