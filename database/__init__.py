"""
Paquete database - Maneja toda la conexión y operaciones con la base de datos
"""

from .conn import db, DatabaseConnection
from .login import Login
from .registrar import Registrar

# Esto permite importar directamente desde el paquete database
__all__ = ['db', 'DatabaseConnection', 'Login', 'Registrar']