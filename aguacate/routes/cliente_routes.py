from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from aguacate import db
from aguacate.models.cliente import Cliente

client_bp = Blueprint('clients', __name__, url_prefix='/clientes')

@client_bp.route('/clientes')
@login_required
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template('clientes/listar.html', clientes=clientes)


@client_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        nuevo = Cliente(nombre=nombre, correo=correo, direccion=direccion, telefono=telefono)
        db.session.add(nuevo)
        db.session.commit()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('clients.listar_clientes'))

    return render_template('clientes/crear.html')

@client_bp.route('/editar/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.correo = request.form['correo']
        cliente.direccion = request.form['direccion']
        cliente.telefono = request.form['telefono']

        db.session.commit()
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clients.listar_clientes'))

    return render_template('clientes/editar.html', cliente=cliente)

@client_bp.route('/eliminar/<int:cliente_id>', methods=['POST'])
@login_required
def eliminar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado correctamente', 'success')
    return redirect(url_for('clients.listar_clientes'))