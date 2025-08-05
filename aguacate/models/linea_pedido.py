from aguacate import db

class LineaPedido(db.Model):
    __tablename__ = 'linea_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    # Relaciones
    pedido = db.relationship('Pedido', back_populates='lineas')
    producto = db.relationship('Producto')
