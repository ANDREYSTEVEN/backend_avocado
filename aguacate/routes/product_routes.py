from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from aguacate import db
from aguacate.models.product import Producto

product_bp = Blueprint('products', __name__, url_prefix='/productos')

@product_bp.route('/')
@login_required
def listar_productos():
    productos = Producto.query.order_by(Producto.fecha_creacion.desc()).all()
    return render_template('productos/listar.html', productos=productos)


@product_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        activo = 'activo' in request.form  # Captura si el checkbox está marcado

        if not nombre or not precio or not stock:
            flash('Todos los campos obligatorios deben ser llenados.', 'danger')
            return redirect(url_for('products.crear_producto'))

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            flash('Precio y stock deben ser valores numéricos válidos.', 'danger')
            return redirect(url_for('products.crear_producto'))

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            activo='activo' in request.form  # Esto guarda True o False según si el checkbox está marcado
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado exitosamente.', 'success')
        return redirect(url_for('products.listar_productos'))

    return render_template('productos/crear.html')


@product_bp.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])
        producto.activo = 'activo' in request.form  # checkbox devuelve True si está marcado

        db.session.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('products.listar_productos'))

    return render_template('productos/editar.html', producto=producto)



@product_bp.route('/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('products.listar_productos'))

@product_bp.route('/toggle/<int:producto_id>', methods=['POST'])
@login_required
def toggle_estado_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    producto.activo = not producto.activo
    db.session.commit()
    estado = 'activado' if producto.activo else 'desactivado'
    flash(f'Producto {estado} correctamente.', 'info')
    return redirect(url_for('products.listar_productos'))