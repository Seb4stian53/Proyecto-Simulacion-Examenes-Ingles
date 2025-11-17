"""
Paquete database - Maneja toda la conexión y operaciones con la base de datos
"""

from .conn import db, DatabaseConnection
from .login import Login
from .registrar import Registrar
from .alumno_querys import Alumno_querys
from .validar_intentos import IntentosManager
from .formularioDB import FormularioManager
from .registrar_admin import RegistrarAdmin

# Esto permite importar directamente desde el paquete database
__all__ = ['db', 'DatabaseConnection', 'Login', 'Registrar', 'Alumno_querys', 'IntentosManager', 'FormularioManager', 'RegistrarAdmin']
