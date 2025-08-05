from functools import wraps
from flask import session, redirect, url_for, flash, g
from aguacate.models.cliente import Cliente


def cliente_actual():
    """
    Retorna el objeto Cliente autenticado actualmente o None.
    """
    cliente_id = session.get('cliente_id')
    if cliente_id:
        return Cliente.query.get(cliente_id)
    return None


def cliente_login_required(f):
    """
    Decorador para rutas que requieren autenticación del cliente.
    Redirige al login si no hay sesión activa.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'cliente_id' not in session:
            flash("Debes iniciar sesión como cliente para continuar.", "warning")
            return redirect(url_for('cliente_auth.login'))
        return f(*args, **kwargs)
    return decorated_function
