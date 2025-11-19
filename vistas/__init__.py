"""
Paquete views - Contiene todas las interfaces de usuario con Tkinter
"""

from .login_view import LoginView
from .register_view import RegisterView
from .admin_view import AdminView
from .user_view import AlumnoView
from .prueba_view_og import PruebaViewOriginal
from .register_admin_view import RegisterAdminView
from .dashboard_alumno_view import DashboardAlumnoView
from .dashboard_admin_view import DashboardAdminView
from .revision_view import RevisionView
from .historial_view import HistorialView

__all__ = ['LoginView', 'RegisterView', 'AdminView', 'AlumnoView', 'PruebaViewOriginal', 'RegisterAdminView', 'DashboardAlumnoView', 'DashboardAdminView', 'RevisionView', 'HistorialView']