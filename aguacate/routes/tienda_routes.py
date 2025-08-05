from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Markup
from aguacate import db
from aguacate.models.product import Producto
from aguacate.models.order import Pedido
from aguacate.models.linea_pedido import LineaPedido
from datetime import datetime
from aguacate.utils.cliente_login import cliente_login_required, cliente_actual

tienda_bp = Blueprint('tienda', __name__, url_prefix='/tienda')


@tienda_bp.route('/')
def index():
    productos = Producto.query.filter(Producto.activo == True).all()
    return render_template('tienda/index.html', productos=productos)


@tienda_bp.route('/agregar/<int:producto_id>')
def agregar_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    carrito = session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1
        }

    session['carrito'] = carrito
    flash(f'{producto.nombre} agregado al carrito.', 'success')
    return redirect(url_for('tienda.index'))


@tienda_bp.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('tienda/carrito.html', carrito=carrito, total=total)


@tienda_bp.route('/eliminar/<int:producto_id>')
def eliminar_producto(producto_id):
    carrito = session.get('carrito', {})
    carrito.pop(str(producto_id), None)
    session['carrito'] = carrito
    flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('tienda.ver_carrito'))


@tienda_bp.route('/confirmar', methods=['GET', 'POST'])
@cliente_login_required
def confirmar_pedido():
    carrito = session.get('carrito', {})
    if not carrito:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('tienda.index'))

    cliente = cliente_actual()
    if not cliente:
        flash("Debes iniciar sesión para confirmar el pedido.", "danger")
        return redirect(url_for('cliente_auth.login'))

    if request.method == 'POST':
        total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

        nuevo_pedido = Pedido(
            cliente_id=cliente.id,
            cliente_nombre=cliente.nombre,
            direccion=cliente.direccion,
            total=total,
            fecha=datetime.utcnow(),
            estado='pendiente'
        )
        db.session.add(nuevo_pedido)
        db.session.flush()

        for producto_id, item in carrito.items():
            linea = LineaPedido(
                pedido_id=nuevo_pedido.id,
                producto_id=int(producto_id),
                cantidad=item['cantidad'],
                precio_unitario=item['precio']
            )
            db.session.add(linea)

            producto = Producto.query.get(int(producto_id))
            if producto and producto.stock is not None:
                producto.stock -= item['cantidad']

        db.session.commit()
        session.pop('carrito', None)
        return redirect(url_for('tienda.pedido_confirmado', pedido_id=nuevo_pedido.id))

    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('tienda/confirmar.html', carrito=carrito, total=total, cliente=cliente)


@tienda_bp.route('/pedido_confirmado/<int:pedido_id>')
@cliente_login_required
def pedido_confirmado(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('tienda/pedido_confirmado.html', pedido=pedido)
