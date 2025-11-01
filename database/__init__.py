"""
Paquete database - Maneja toda la conexión y operaciones con la base de datos
"""

from .conn import db, DatabaseConnection
from .login import Login
from .registrar import Registrar
from .alumno_querys import alumnos_querys

# Esto permite importar directamente desde el paquete database
__all__ = ['db', 'DatabaseConnection', 'Login', 'Registrar', 'alumnos_querys']