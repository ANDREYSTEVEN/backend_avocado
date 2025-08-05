from flask import render_template, request, redirect, url_for, flash
from aguacate.models.user import User
from flask_login import login_user
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from aguacate import db

# ------------------ INICIO DE SESIÓN ------------------
def login_logic(email, password):
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return None, "Credenciales inválidas"

    if not check_password_hash(user.password, password):
        return None, "Contraseña incorrecta"

    if not user.is_active:
        return None, "Tu cuenta aún no está activada"

    login_user(user)
    return user, None


# ------------------ REGISTRO ------------------
def register_logic(nombre, email, password, confirmar):
    if password != confirmar:
        return False, "Las contraseñas no coinciden"

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False, "El correo ya está registrado"

    hashed_password = generate_password_hash(password)

    new_user = User(
        nombre=nombre,
        email=email,
        password=hashed_password,
        fecha_activacion=datetime.utcnow()  # o puede ser None si requiere activación
    )

    db.session.add(new_user)
    db.session.commit()

    return True, "Usuario registrado exitosamente"

# Renderiza formulario de registro
def show_register_form():
    return render_template('auth/register.html')


# Procesa datos del formulario de registro
def register_user():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([nombre, email, password, confirm_password]):
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for('auth.register'))

    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "danger")
        return redirect(url_for('auth.register'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("El correo ya está registrado.", "danger")
        return redirect(url_for('auth.register'))

    hashed_password = generate_password_hash(password)

    new_user = User(nombre=nombre, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    flash("Cuenta creada con éxito. ¡Bienvenido!", "success")
    return redirect(url_for('dashboard.dashboard'))
