# aguacate/routes/report_routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func
from aguacate import db
from aguacate.models.order import Pedido
from aguacate.models.linea_pedido import LineaPedido
from aguacate.models.product import Producto
from aguacate.models.cliente import Cliente
from datetime import datetime

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/', methods=['GET'])
@login_required
def resumen_reportes():
    # Obtener fechas del formulario o usar todo
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d') if fecha_inicio else None
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') if fecha_fin else None
    except ValueError:
        fecha_inicio, fecha_fin = None, None

    # Filtro base
    query = Pedido.query
    if fecha_inicio:
        query = query.filter(Pedido.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Pedido.fecha <= fecha_fin)

    # Pedidos por estado (filtrado)
    pedidos_por_estado = query.with_entities(Pedido.estado, func.count(Pedido.id)).group_by(Pedido.estado).all()

    # Total de ventas (filtrado)
    ventas_totales = query.with_entities(func.sum(Pedido.total)).scalar() or 0

    # Productos más vendidos (filtrado por pedidos)
    subquery = query.with_entities(Pedido.id).subquery()
    productos_mas_vendidos = db.session.query(
        Producto.nombre,
        func.sum(LineaPedido.cantidad).label('total_vendidos')
    ).join(LineaPedido.producto)\
     .filter(LineaPedido.pedido_id.in_(subquery))\
     .group_by(Producto.id)\
     .order_by(func.sum(LineaPedido.cantidad).desc())\
     .limit(5).all()

    # Clientes más activos (filtrado)
    clientes_mas_activos = db.session.query(
        Cliente.nombre,
        func.count(Pedido.id)
    ).join(Pedido).filter(Pedido.id.in_(subquery))\
     .group_by(Cliente.id)\
     .order_by(func.count(Pedido.id).desc())\
     .limit(5).all()

    return render_template(
        'reportes/resumen.html',
        pedidos_por_estado=pedidos_por_estado,
        ventas_totales=ventas_totales,
        productos_mas_vendidos=productos_mas_vendidos,
        clientes_mas_activos=clientes_mas_activos,
        fecha_inicio=fecha_inicio.strftime('%Y-%m-%d') if fecha_inicio else '',
        fecha_fin=fecha_fin.strftime('%Y-%m-%d') if fecha_fin else ''
    )
