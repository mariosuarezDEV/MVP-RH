# Sistema de Gestión Empresarial

Un sistema integral de gestión empresarial desarrollado con Django que permite administrar empresas, sucursales, empleados, horarios, salarios e incidencias.

## 🚀 Características

- **Gestión de Empresas y Sucursales**: Administra múltiples empresas y sus respectivas sucursales
- **Gestión de Personal**: Control de empleados, puestos de trabajo y contratos
- **Sistema de Horarios**: Programación y seguimiento de horarios laborales
- **Control de Salarios**: Gestión de nóminas y compensaciones
- **Registro de Incidencias**: Sistema de tickets y seguimiento de problemas
- **Autenticación Avanzada**: Integración con AllAuth, MFA y login social con Google
- **Panel de Administración**: Interface moderna con Unfold
- **Procesamiento Asíncrono**: Integración con Celery y Redis
- **Editor de Markdown**: Integrado con Martor
- **Monitoreo**: Integración con Sentry para tracking de errores

## 🛠️ Stack Tecnológico

### Backend
- **Django 5.2** - Framework web principal
- **PostgreSQL** - Base de datos principal
- **Redis** - Cache y broker para Celery
- **Celery** - Procesamiento de tareas asíncronas

### Frontend
- **Bootstrap 5** - Framework CSS
- **Django Unicorn** - Componentes reactivos
- **Crispy Forms** - Formularios mejorados
- **FontAwesome** - Iconografía

### Autenticación y Seguridad
- **Django AllAuth** - Sistema de autenticación
- **Google OAuth** - Login social
- **MFA Support** - Autenticación multifactor
- **Guardian** - Permisos a nivel de objeto

### Monitoreo y Desarrollo
- **Sentry** - Monitoreo de errores
- **Django Debug Toolbar** - Herramientas de desarrollo
- **WhiteNoise** - Servir archivos estáticos

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- Redis
- Docker y Docker Compose (recomendado)

## 🔧 Instalación

### Con Docker (Recomendado)

1. **Clona el repositorio**
```bash
git clone <url-del-repositorio>
cd proyecto
```

2. **Crea el archivo de variables de entorno**
```bash
cp .env.example .env
```

3. **Configura las variables de entorno en `.env`**
```env
SECRET_KEY=tu_secret_key_muy_seguro_aqui
DEBUG=True
DATABASE_URL=postgres://usuario:password@db:5432/proyecto_db
REDIS_URL=redis://redis:6379/0
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
SENTRY_DSN=https://tu_dsn_de_sentry
```

4. **Levanta los servicios con Docker Compose**
```bash
docker-compose up -d
```

5. **Ejecuta las migraciones**
```bash
docker-compose exec web python manage.py migrate
```

6. **Crea un superusuario**
```bash
docker-compose exec web python manage.py createsuperuser
```

### Instalación Manual

1. **Clona el repositorio y crea un entorno virtual**
```bash
git clone <url-del-repositorio>
cd proyecto
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

3. **Configura la base de datos PostgreSQL y Redis**

4. **Crea y configura el archivo `.env`** (ver ejemplo arriba)

5. **Ejecuta las migraciones**
```bash
python manage.py migrate
```

6. **Crea un superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecuta el servidor de desarrollo**
```bash
python manage.py runserver
```

8. **En otra terminal, ejecuta Celery Worker**
```bash
celery -A proyecto worker --loglevel=info
```

## 🎯 Uso

### Acceso al Sistema
- **Aplicación Web**: http://localhost:8000
- **Panel de Admin**: http://localhost:8000/admin/
- **Documentación de API**: http://localhost:8000/api/docs/ (si está habilitado)

### Módulos Principales

#### 1. Gestión de Empresas (`/empresas/`)
- Crear y administrar empresas
- Configuración de parámetros empresariales
- Gestión de documentos corporativos

#### 2. Sucursales (`/sucursales/`)
- Administrar sucursales por empresa
- Configuración de ubicaciones
- Asignación de personal

#### 3. Puestos de Trabajo (`/puestos/`)
- Definir roles y responsabilidades
- Estructura organizacional
- Niveles jerárquicos

#### 4. Gestión de Horarios (`/horarios/`)
- Programación de turnos
- Control de asistencia
- Reportes de tiempo

#### 5. Sistema de Incidencias (`/incidencias/`)
- Registro de problemas
- Seguimiento de tickets
- Resolución de incidencias

### Funcionalidades de Autenticación
- Login con email/usuario y contraseña
- Login con Google OAuth
- Autenticación multifactor (MFA)
- Recuperación de contraseña
- Gestión de sesiones

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clave secreta de Django | - |
| `DEBUG` | Modo debug | `False` |
| `DATABASE_URL` | URL de conexión a PostgreSQL | - |
| `REDIS_URL` | URL de conexión a Redis | `redis://localhost:6379/0` |
| `EMAIL_HOST_USER` | Email para notificaciones | - |
| `EMAIL_HOST_PASSWORD` | Contraseña del email | - |
| `SENTRY_DSN` | DSN de Sentry para monitoreo | - |

### Configuración de Celery

Para procesamiento asíncrono, asegúrate de tener Redis ejecutándose y ejecuta:

```bash
# Worker
celery -A proyecto worker --loglevel=info

# Monitor (opcional)
celery -A proyecto flower
```

### Configuración de Cache

El sistema utiliza Redis para cache y sesiones. La configuración está optimizada con:
- Compresión zlib
- Pool de conexiones
- Health checks automáticos

## 📊 Base de Datos

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar estado
python manage.py showmigrations
```

### Backup y Restauración

```bash
# Backup
python manage.py dbbackup

# Restaurar
python manage.py dbrestore
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Tests con cobertura
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📦 Despliegue

### Preparación para Producción

1. **Configurar variables de entorno de producción**
```env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
SECRET_KEY=clave_super_segura_para_produccion
```

2. **Recopilar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

3. **Ejecutar migraciones**
```bash
python manage.py migrate
```

### Con Docker en Producción

```bash
# Build de imagen de producción
docker build -t proyecto-prod .

# Ejecutar con configuración de producción
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Monitoreo y Logs

### Logs
Los logs se almacenan en `logs/django.log` con rotación automática:
- Tamaño máximo: 5MB por archivo
- Archivos de respaldo: 10
- Formato: `[NIVEL] timestamp nombre mensaje`

### Sentry
Configurado para capturar:
- Errores de aplicación
- Performance monitoring
- Información de usuarios (si está habilitado)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estilo de Código
- Seguir PEP 8
- Usar Black para formateo
- Documentar funciones complejas
- Escribir tests para nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🎖️ Agradecimientos

- Django Community
- Bootstrap Team
- Todos los contribuidores del proyecto

---

**Desarrollado con ❤️ usando Django**