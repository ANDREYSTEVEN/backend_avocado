from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required

from aguacate.controllers.auth_controller import login_logic, register_logic

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ------------------ INICIO DE SESIÓN ------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user, error = login_logic(email, password)

        if user:
            flash("Inicio de sesión exitoso", 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(error, 'danger')

    return render_template('auth/login.html')


# ------------------ REGISTRO ------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        confirmar = request.form['confirmar']

        success, message = register_logic(nombre, email, password, confirmar)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')

    # Este return debe estar siempre
    return render_template('auth/register.html')

# ------------------ CERRAR SESION ------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", 'info')
    return redirect(url_for('auth.login'))