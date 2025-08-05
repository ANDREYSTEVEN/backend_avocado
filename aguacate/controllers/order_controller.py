from flask import session
from datetime import datetime
from aguacate import db
from aguacate.models.order import Pedido
from aguacate.models.linea_pedido import LineaPedido
from aguacate.models.product import Producto


def create_order_from_cart():
    carrito = session.get('carrito', {})
    if not carrito:
        return None, "El carrito está vacío"

    total = 0
    lineas = []

    for producto_id_str, item in carrito.items():
        producto_id = int(producto_id_str)
        producto = Producto.query.get(producto_id)

        if not producto:
            return None, f"Producto con ID {producto_id} no encontrado"
        if item['cantidad'] > producto.stock:
            return None, f"No hay suficiente stock para {producto.nombre}"

        subtotal = producto.precio * item['cantidad']
        total += subtotal

        lineas.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'precio_unitario': producto.precio
        })

    nuevo_pedido = Pedido(
        cliente_nombre="Cliente Web",
        direccion="Sin dirección",  # Puedes actualizar esto si se recolecta
        total=total,
        fecha=datetime.utcnow(),
        estado='pendiente'
    )
    db.session.add(nuevo_pedido)
    db.session.flush()  # Para obtener el ID antes del commit

    for linea in lineas:
        nueva_linea = LineaPedido(
            pedido_id=nuevo_pedido.id,
            producto_id=linea['producto'].id,
            cantidad=linea['cantidad'],
            precio_unitario=linea['precio_unitario']
        )
        db.session.add(nueva_linea)

        # Actualizar el stock del producto
        linea['producto'].stock -= linea['cantidad']

    db.session.commit()
    session.pop('carrito', None)

    return nuevo_pedido, None
