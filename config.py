import os

class Config:
    """
    Configuración general de la aplicación Flask.
    Puede extenderse a diferentes entornos (Desarrollo, Producción, etc.).
    """

    # Clave secreta para proteger sesiones y formularios (CSRF)
    # ⚠️ En producción, se recomienda definir esta variable en el entorno
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-flask')

    # URI de conexión a la base de datos
    # Formato: dialecto+driver://usuario:contraseña@host/basededatos
    # Ejemplo para MySQL usando PyMySQL (puede adaptarse a PostgreSQL o SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/gestor_biblioteca'  # Valor por defecto para entorno local (MAMP/XAMPP)
    )

    # Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy (mejora el rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False