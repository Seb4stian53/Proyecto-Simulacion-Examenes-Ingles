"""
Paquete views - Contiene todas las interfaces de usuario con Tkinter
"""

from .login_view import LoginView
from .register_view import RegisterView
from .admin_view import AdminView
from .user_view import AlumnoView

__all__ = ['LoginView', 'RegisterView', 'AdminView', 'AlumnoView']