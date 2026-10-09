"""Genera las páginas HTML de esa.com.bo a partir de una plantilla común.

Uso:  python3 tools/build.py   (desde la raíz del repositorio)
Cabecera, menú, pie, WhatsApp y metadatos se escriben una sola vez aquí;
el contenido de cada página está en tools/paginas/*.html.
"""
import json, pathlib, datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOM = "https://esa.com.bo/"

MENU = [
    ("index.html", "Inicio"),
    ("hogar.html", "Hogar"),
    ("empresas.html", "Empresas"),
    ("grandes-proyectos.html", "Grandes proyectos"),
    ("nosotros.html", "Nosotros"),
    ("contacto.html", "Contacto"),
]

PAGINAS = {
    "index.html": ("Paneles solares en Santa Cruz, Bolivia | ESA Energía Solar",
                   "Paneles solares para casas, empresas e industrias en Santa Cruz de la Sierra, conectados a la red de CRE. Diseño, instalación y mantenimiento. Cotiza gratis."),
    "hogar.html": ("Paneles solares para tu casa en Santa Cruz, Bolivia | ESA",
                   "Genera tu propia energía y baja tu factura de luz. Sistemas solares para hogares conectados a la red de CRE, con 7 años de mantenimiento preventivo gratuito."),
    "empresas.html": ("Energía solar para empresas en Santa Cruz, Bolivia | ESA",
                      "Reduce los costos de energía de tu empresa con un sistema solar diseñado según tu consumo real. Estudio energético, instalación, operación y mantenimiento."),
    "grandes-proyectos.html": ("Plantas solares e ingeniería eléctrica a gran escala | ESA",
                               "Plantas solares e ingeniería eléctrica para industrias e instituciones en Bolivia. Estudio, construcción, operación y mantenimiento con un mismo equipo."),
    "nosotros.html": ("Nosotros | ESA Energía Solar Accesible",
                      "ESA es una empresa cruceña de energía solar e ingeniería eléctrica. Conoce a nuestro equipo de ingenieros, nuestra misión, valores y forma de trabajar."),
    "contacto.html": ("Contacto | ESA Energía Solar Accesible",
                      "Escríbenos por WhatsApp al +591 776-66653, a comercial@esa.com.bo o visítanos en el Tercer Anillo Externo N° 3040, Santa Cruz de la Sierra."),
}

PORTADA = {"hogar.html": "img/hogar-portada.jpg"}

EMPRESA = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": DOM + "#empresa",
    "name": "ESA - Energía Solar Accesible",
    "alternateName": "ESA",
    "slogan": "Mejorando tu presente",
    "description": "Empresa de soluciones energéticas e ingeniería eléctrica en Santa Cruz de la Sierra, Bolivia: energía solar fotovoltaica para hogares, empresas e industrias, eficiencia y gestión energética, y electromovilidad.",
    "url": DOM,
    "logo": DOM + "img/logo.png",
    "image": DOM + "img/og.jpg",
    "telephone": "+591 77666653",
    "email": "comercial@esa.com.bo",
    "address": {"@type": "PostalAddress",
                "streetAddress": "Tercer Anillo Externo N° 3040, entre Beni y Alemana",
                "addressLocality": "Santa Cruz de la Sierra", "addressRegion": "Santa Cruz", "addressCountry": "BO"},
    "areaServed": [{"@type": "AdministrativeArea", "name": "Santa Cruz, Bolivia"}, {"@type": "Country", "name": "Bolivia"}],
    "knowsAbout": ["Energía solar fotovoltaica", "Generación distribuida", "Ingeniería eléctrica",
                   "Eficiencia energética", "Electromovilidad"],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Soluciones ESA", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": DOM + u}} for n, u in [
            ("Energía solar para el hogar", "hogar.html"),
            ("Energía solar para empresas", "empresas.html"),
            ("Plantas solares e ingeniería eléctrica a gran escala", "grandes-proyectos.html"),
            ("Mantenimiento y monitoreo de sistemas solares", "index.html#mantenimiento"),
            ("Infraestructura de carga para vehículos eléctricos", "nosotros.html#ecosistema")]]},
}

ICONO_WA = '<svg width="{t}" height="{t}" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.4c-2.1 0-4.1-.6-5.9-1.7l-.4-.3-3.8 1.2 1.2-3.7-.3-.4a10.5 10.5 0 0 1-1.7-5.7C5.1 10 10 5.2 16 5.2S26.9 10 26.9 15.9 22 26.4 16 26.4zm6-7.8c-.3-.2-1.9-1-2.2-1.1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6.3-.5c.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.2 1.4 3.4c.2.2 2.4 3.6 5.7 5 .8.3 1.4.5 1.9.7.8.3 1.5.2 2.1.1.6-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
ICONO_TEL = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
ICONO_MAIL = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'


def cabecera(archivo):
    items = []
    for href, nombre in MENU:
        actual = ' aria-current="page"' if href == archivo else ""
        items.append(f'      <li><a href="{href}"{actual}>{nombre}</a></li>')
    items.append('      <li><a href="contacto.html#cotizar" class="btn btn-borde">Cotiza ahora</a></li>')
    return f'''<a href="#contenido" class="saltar">Saltar al contenido</a>
<header>
  <div class="wrap nav">
    <a href="index.html" class="logo" translate="no"><img src="img/logo.png" alt="ESA Energía Solar Accesible, ir al inicio" width="117" height="22"></a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">☰</button>
    <ul class="menu" id="menu">
{chr(10).join(items)}
    </ul>
  </div>
</header>
<div class="franja-atencion">
  <p>Escríbenos o llámanos: te responde un ingeniero de ESA.</p>
  <a class="pastilla" href="tel:+59177666653">{ICONO_TEL.replace('width="26" height="26"','width="18" height="18"')}Llámanos al 776-66653</a>
  <a class="pastilla js-wa" href="#">{ICONO_WA.format(t=18)}WhatsApp +591 776-66653</a>
</div>'''


CONTACTO_FINAL = f'''<section class="contacto-final">
  <div class="wrap">
    <h2 class="titulo-linea">¿No encontraste lo que buscabas?</h2>
    <p class="lead">Escríbenos o llámanos. Un ingeniero de ESA te responde.</p>
    <div class="canales">
      <a class="canal js-wa" href="#">{ICONO_WA.format(t=30)}<div><b>WhatsApp</b><span>+591 776-66653</span></div></a>
      <a class="canal" href="tel:+59177666653">{ICONO_TEL}<div><b>Llámanos</b><span>(591) 776-66653</span></div></a>
      <a class="canal js-mail" href="mailto:comercial@esa.com.bo">{ICONO_MAIL}<div><b>Correo</b><span>comercial@esa.com.bo</span></div></a>
    </div>
  </div>
</section>'''

PIE = '''<footer>
  <div class="wrap">
    <div class="pie">
      <div class="contacto-pie">
        <img src="img/logo-blanco.png" alt="ESA Energía Solar Accesible" width="213" height="40" style="margin-bottom:1.3rem">
        <p>Llámanos al <a href="tel:+59177666653">(591) 776-66653</a></p>
        <p>WhatsApp <a href="#" class="js-wa">+591 776-66653</a></p>
        <p>Correo <a class="js-mail" href="mailto:comercial@esa.com.bo">comercial@esa.com.bo</a></p>
        <p>Dirección: Tercer Anillo Externo N° 3040, entre Beni y Alemana, Santa Cruz de la Sierra, Bolivia</p>
        <div class="redes" title="Redes sociales pendientes"><span>FB</span><span>IG</span><span>TT</span><span>IN</span></div>
      </div>
      <div><h4>Compañía</h4><ul><li><a href="nosotros.html">Nosotros</a></li><li><a href="nosotros.html#ecosistema">Nuestro ecosistema</a></li><li><a href="contacto.html">Trabaja con nosotros</a></li></ul></div>
      <div><h4>Soluciones energéticas</h4><ul><li><a href="hogar.html">Hogar</a></li><li><a href="empresas.html">Empresas</a></li><li><a href="grandes-proyectos.html">Grandes proyectos</a></li><li><a href="index.html#mantenimiento">Mantenimiento</a></li></ul></div>
      <div><h4>Centro de ayuda</h4><ul><li><a href="contacto.html">Contáctanos</a></li><li><a href="contacto.html#cotizar">Cotiza tu sistema</a></li></ul></div>
    </div>
    <div class="legal"><span>© <span class="js-anio">2026</span> ESA Energía Solar Accesible. Todos los derechos reservados.</span><span class="lema" translate="no">MEJORANDO TU PRESENTE</span></div>
  </div>
</footer>'''

WA_FLOTANTE = f'<a href="#" class="wa js-wa" aria-label="Escríbenos por WhatsApp">{ICONO_WA.format(t=34)}</a>'


def pagina(archivo, cuerpo):
    titulo, desc = PAGINAS[archivo]
    url = DOM if archivo == "index.html" else DOM + archivo
    ld = ""
    if archivo in ("index.html", "contacto.html"):
        ld = '\n<script type="application/ld+json">\n' + json.dumps(EMPRESA, ensure_ascii=False, indent=1) + "\n</script>"
    return f'''<!doctype html>
<html lang="es-BO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_BO">
<meta property="og:site_name" content="ESA Energía Solar Accesible">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOM}img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" href="fonts/android.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/outfit-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{PORTADA.get(archivo, "img/hero.jpg")}" as="image" fetchpriority="high">
<link rel="stylesheet" href="css/esa.css">{ld}
</head>
<body>
{cabecera(archivo)}

<main id="contenido">
{cuerpo.strip()}

{"" if archivo == "contacto.html" else CONTACTO_FINAL}
</main>

{PIE}

{WA_FLOTANTE}
<script src="js/esa.js"></script>
</body>
</html>
'''


def main():
    hoy = datetime.date.today().isoformat()
    for archivo, _ in MENU:
        cuerpo = (RAIZ / "tools" / "paginas" / archivo).read_text(encoding="utf-8")
        (RAIZ / archivo).write_text(pagina(archivo, cuerpo), encoding="utf-8")
        print("ok", archivo)
    urls = "\n".join(f"  <url>\n    <loc>{DOM if a == 'index.html' else DOM + a}</loc>\n    <lastmod>{hoy}</lastmod>\n  </url>" for a, _ in MENU)
    (RAIZ / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf-8")
    print("ok sitemap.xml")


if __name__ == "__main__":
    main()
