from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from aguacate import db
from aguacate.models.order import Pedido
from aguacate.models.repartidor import Repartidor
from aguacate.controllers.order_controller import create_order_from_cart

order_bp = Blueprint('orders', __name__, url_prefix='/pedidos')

# ------------------ LISTAR PEDIDOS ------------------
@order_bp.route('/')
@login_required
def listar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).all()
    return render_template('pedidos/listar.html', pedidos=pedidos)

# ------------------ CREAR PEDIDO ------------------
@order_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_pedido():
    if request.method == 'POST':
        cliente_nombre = request.form['cliente_nombre']
        direccion = request.form['direccion']
        total = float(request.form['total'])

        nuevo_pedido = Pedido(cliente_nombre=cliente_nombre, direccion=direccion, total=total)
        db.session.add(nuevo_pedido)
        db.session.commit()
        flash('Pedido creado exitosamente', 'success')
        return redirect(url_for('orders.listar_pedidos'))

    return render_template('pedidos/crear.html')

# ------------------ EDITAR PEDIDO ------------------
@order_bp.route('/editar/<int:pedido_id>', methods=['GET', 'POST'])
@login_required
def editar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)

    if request.method == 'POST':
        pedido.cliente_nombre = request.form['cliente_nombre']
        pedido.direccion = request.form['direccion']
        pedido.total = float(request.form['total'])
        pedido.estado = request.form['estado']

        db.session.commit()
        flash('Pedido actualizado correctamente', 'success')
        return redirect(url_for('orders.listar_pedidos'))

    return render_template('pedidos/editar.html', pedido=pedido)

# ------------------ ELIMINAR PEDIDO ------------------
@order_bp.route('/eliminar/<int:pedido_id>', methods=['POST'])
@login_required
def eliminar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    db.session.delete(pedido)
    db.session.commit()
    flash('Pedido eliminado correctamente', 'success')
    return redirect(url_for('orders.listar_pedidos'))

# ------------------ ASIGNAR REPARTIDOR ------------------
@order_bp.route('/<int:pedido_id>/asignar', methods=['GET', 'POST'])
@login_required
def asignar_repartidor(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    repartidores = Repartidor.query.all()

    if request.method == 'POST':
        repartidor_id = request.form.get('repartidor_id')
        if repartidor_id:
            pedido.repartidor_id = repartidor_id
            db.session.commit()
            flash('Repartidor asignado con éxito.', 'success')
            return redirect(url_for('orders.listar_pedidos'))

    return render_template('pedidos/asignar_repartidor.html', pedido=pedido, repartidores=repartidores)

# ------------------ CAMBIAR ESTADO ------------------
@order_bp.route('/<int:pedido_id>/estado', methods=['POST'])
@login_required
def cambiar_estado(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    nuevo_estado = request.form.get('estado')
    if nuevo_estado:
        pedido.estado = nuevo_estado
        db.session.commit()
        flash('Estado del pedido actualizado.', 'info')
    return redirect(url_for('orders.listar_pedidos'))

# ------------------ CONFIRMAR PEDIDO DESDE EL CARRITO ------------------
@order_bp.route('/confirmar', methods=['GET'])
@login_required
def confirmar_pedido():
    order, error = create_order_from_cart(current_user.id)

    if error:
        session['error'] = error
        return redirect(url_for('cart.view_cart'))

    return render_template('cliente/pedido_confirmado.html', order=order)
