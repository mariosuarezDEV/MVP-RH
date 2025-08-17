# 🐍 Plantilla Completa para Inicializar Proyectos Django

Esta plantilla sirve como guía rápida para configurar un proyecto Django moderno con **buenas prácticas**, seguridad, formularios avanzados, administración mejorada, soporte full stack y preparación para producción.

---

## 🔗 Recursos Recomendados

* [Django Packages](https://djangopackages.org/) – Encuentra paquetes útiles para Django.
* [Awesome Django](https://awesomedjango.org/) – Repositorio curado de herramientas, paquetes y tutoriales.

---

## 1️⃣ Instalación Inicial

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

2. Instalar Django:

```bash
pip install django==5.2.5
```

3. Crear proyecto:

```bash
django-admin startproject proyecto .
```

---

## 🖥️ Administración Mejorada

### Django Unfold

* Mejora el admin estándar con funciones avanzadas como filtros, inlines, historial, ubicación, import/export y compatibilidad con Guardian.
* Instalación: `pip install unfold`
* Documentación: [Unfold Admin](https://unfoldadmin.com/?utm_medium=github&utm_source=unfold)

### Django Import Export

* Permite exportar e importar datos desde el admin en formatos como CSV, JSON o Excel.
* Instalación: `pip install django-import-export`
* Documentación: [Import Export](https://github.com/django-import-export/django-import-export)

---

## 🔒 Seguridad y Autenticación

### Django AllAuth

* Permite autenticación social, registro y login.
* Instalación: `pip install django-allauth`
* Documentación: [AllAuth Docs](https://docs.allauth.org/en/latest/)
* Configuración: soporte para Google OAuth2 y modelo de usuario personalizado (`AUTH_USER_MODEL = "base.User"`).

### Django Guardian (opcional con Unfold)

* Control de permisos por objeto.
* Instalación: `pip install django-guardian`
* Documentación: [Guardian Docs](https://django-guardian.readthedocs.io/)

---

## ⚡ Canales y Funcionalidades Asíncronas

### Daphne (Servidor ASGI)

* Instalación: `pip install daphne`
* Permite servir aplicaciones Django con soporte ASGI para WebSockets y async.

---

## 📝 Formularios Avanzados

### Django Crispy Forms + Bootstrap 5

* Mejora la apariencia y estructura de los formularios.
* Instalación:

```bash
pip install django-crispy-forms crispy-bootstrap5
```

* Documentación: [Crispy Forms](https://github.com/django-crispy-forms/crispy-bootstrap5)

### Formularios Multistep

* Paquete: `django-formtools`
* Ideal para formularios largos o procesos por pasos.
* Instalación: `pip install django-formtools`
* Documentación: [Formtools Docs](https://django-formtools.readthedocs.io/en/latest/)

### Martor (Markdown Editor)

* Editor Markdown en formularios con soporte para imagen, emojis y código.
* Instalación: `pip install martor`
* Configuración: toolbar personalizable, tema Bootstrap.
* Documentación: [Martor](https://pypi.org/project/django-martor/)

---

## 🌐 Full Stack Sin JavaScript

### Django Unicorn

* Permite interactividad en tiempo real sin escribir JS.
* Instalación: `pip install django-unicorn`
* Documentación: [Django Unicorn Docs](https://www.django-unicorn.com/docs/)

---

## 💰 Campos Especiales para Modelos

### Django Money

* Campos de moneda para modelos Django.
* Instalación: `pip install djmoney`
* Documentación: [Django Money](https://github.com/django-money/django-money)

---

## 🌍 Localización e Internacionalización

* Idioma: Español México (`LANGUAGE_CODE = "es-mx"`)
* Zona horaria: `America/Mexico_City`

---

## 🚀 Preparación para Producción

### WhiteNoise

* Gestiona archivos estáticos en producción de manera eficiente.
* Instalación: `pip install whitenoise`
* Configuración: `CompressedManifestStaticFilesStorage`
* Documentación: [WhiteNoise Docs](https://whitenoise.readthedocs.io/en/stable/)

---

## 🗂️ Estructura Base de Carpetas

```
proyecto/
├─ base/                  # App base con modelos y lógica principal
├─ templates/             # Templates globales
├─ staticfiles/           # Archivos estáticos recopilados
├─ db.sqlite3             # Base de datos SQLite (desarrollo)
├─ manage.py
├─ proyecto/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
```

---

## ✅ Buenas Prácticas Incluidas

* Modelo de usuario personalizado (`base.User`)
* Backends de autenticación configurados para AllAuth
* Admin potente con Unfold y filtros avanzados
* Formularios bonitos y multistep con Crispy y Formtools
* Markdown editor con Martor
* Producción lista con WhiteNoise
* Preparado para async / WebSockets con Daphne
