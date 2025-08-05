from flask import Blueprint, flash, render_template, redirect, url_for, request
from aguacate import db
from aguacate.models.repartidor import Repartidor

repartidor_bp = Blueprint('repartidor', __name__, url_prefix='/repartidores')

@repartidor_bp.route('/')
def listar_repartidores():
    repartidores = Repartidor.query.all()
    return render_template('repartidores/lista.html', repartidores=repartidores)

@repartidor_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_repartidor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        repartidor = Repartidor(nombre=nombre, telefono=telefono)
        db.session.add(repartidor)
        db.session.commit()
        return redirect(url_for('repartidor.listar_repartidores'))
    return render_template('repartidores/formulario.html')

@repartidor_bp.route('/<int:repartidor_id>/eliminar', methods=['POST'])
def eliminar_repartidor(repartidor_id):
    repartidor = Repartidor.query.get_or_404(repartidor_id)
    db.session.delete(repartidor)
    db.session.commit()
    flash('Repartidor eliminado.', 'success')
    return redirect(url_for('repartidor.listar_repartidores'))