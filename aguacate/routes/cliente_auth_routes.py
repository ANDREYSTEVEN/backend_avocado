from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from aguacate.models.cliente import Cliente
from aguacate import db

cliente_auth_bp = Blueprint('cliente_auth', __name__, url_prefix='/cliente')


# ---------------- LOGIN CLIENTE ----------------
@cliente_auth_bp.route('/login', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        cliente = Cliente.query.filter_by(correo=correo).first()

        if cliente and cliente.check_password(password):
            session['cliente_id'] = cliente.id
            flash("Inicio de sesión exitoso. ¡Bienvenido!", "success")
            return redirect(url_for('tienda.index'))
        else:
            flash("Correo o contraseña incorrectos.", "danger")

    return render_template('clientes/login.html')


# ---------------- REGISTRO CLIENTE ----------------
@cliente_auth_bp.route('/registro', methods=['GET', 'POST'])
def registrar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        password = request.form['password']
        confirmar = request.form['confirmar']

        if password != confirmar:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('cliente_auth.registrar_cliente'))

        if Cliente.query.filter_by(correo=correo).first():
            flash("El correo ya está registrado.", "warning")
            return redirect(url_for('cliente_auth.registrar_cliente'))

        nuevo_cliente = Cliente(
            nombre=nombre,
            correo=correo,
            direccion=direccion,
            telefono=telefono
        )
        nuevo_cliente.set_password(password)

        db.session.add(nuevo_cliente)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('cliente_auth.login_cliente'))

    return render_template('clientes/registro.html')


# ---------------- LOGOUT CLIENTE ----------------
@cliente_auth_bp.route('/logout')
def logout_cliente():
    session.pop('cliente_id', None)
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('cliente_auth.login_cliente'))
