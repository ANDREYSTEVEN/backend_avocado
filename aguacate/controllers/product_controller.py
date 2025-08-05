from flask import render_template, request, redirect, url_for, flash
from aguacate.models.product import Product
from aguacate import db

def list_products():
    products = Product.query.order_by(Product.fecha_creado.desc()).all()
    return render_template('products/list.html', products=products)

def create_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        if not nombre or precio < 0 or stock < 0:
            flash("Datos inválidos. Revisa los campos.", "danger")
            return redirect(url_for('products.create'))

        product = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock
        )
        db.session.add(product)
        db.session.commit()
        flash("Producto creado exitosamente", "success")
        return redirect(url_for('products.list'))

    return render_template('products/create.html')
