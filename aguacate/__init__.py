from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

def create_app():
    app = Flask(__name__)
    
    # Cargar configuración desde config.py
    app.config.from_object('aguacate.config.Config')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Registro de Blueprints
    from aguacate.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from aguacate.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from aguacate.routes.product_routes import product_bp
    app.register_blueprint(product_bp)

    from aguacate.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from aguacate.routes.order_routes import order_bp
    app.register_blueprint(order_bp)

    from aguacate.routes.cliente_routes import client_bp
    app.register_blueprint(client_bp)

    from aguacate.routes.repartidor_routes import repartidor_bp
    app.register_blueprint(repartidor_bp)

    from aguacate.routes.tienda_routes import tienda_bp
    app.register_blueprint(tienda_bp)

    from aguacate.routes.report_routes import reportes_bp
    app.register_blueprint(reportes_bp)

    from aguacate.routes.cliente_auth_routes import cliente_auth_bp
    app.register_blueprint(cliente_auth_bp)

    # Inyección de cliente autenticado en templates
    from aguacate.models.cliente import Cliente

    @app.context_processor
    def inject_cliente_autenticado():
        cliente_id = session.get('cliente_id')
        if cliente_id:
            cliente = Cliente.query.get(cliente_id)
            return dict(cliente_autenticado=cliente)
        return dict(cliente_autenticado=None)

    return app
