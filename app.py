# 0. ejecutamos pip install flask flask-sqlalchemy flask-migrate flask-cors flask-jwt-extended
# 1. Crear modelos
# 2. importamos las librerias de flask
from crypt import methods
from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from sqlalchemy import true
from models import db, Usuario, Regiones, Provincias, Comunas, Clientes, Suscripciones
from models import Donaciones, Descuentos, Productos, Descuentos_Productos, Detalle_Ventas
from models import Ventas, Vendedores, Despachos
from flask_cors import CORS, cross_origin

# 16. jwt seguridad
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# 3. instanciamos la app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Conten-Type'
app.url_map.strict_slashes = False
app.config['DEBUG'] = False
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_ECHO'] = True # para ver los cambios en la base de datos 

# 17. configuracion de seguridad
app.config['JWT_SECRET_KEY'] = "secret-key"
app.config["JWT_SECRET_KEY"] = "os.environ.get('super-secret')"
jwt = JWTManager(app)

db.init_app(app)

Migrate(app, db)


# 18. Ruta de login
@app.route("/login", methods=["POST"])
def create_token():
    email = request.json.get("email")
    password = request.json.get("password")

    user = Usuario.query.filter(Usuario.email == email, Usuario.password == password).first()

    if user == None:
        return jsonify({ 
            "estado": "error",
            "msg": "Error en email o password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, usuario_id=user.id),200


# 5. Creamos la ruta por defecto para saber si mi app esta funcionado
# 6. ejecutamos el comando en la consola: python app.py o python3 app.py y revisamos nuestro navegador
@app.route('/')
# @jwt_required()
def index():
    return 'Hola desde gitpod'

######## Usuarios #########

# 7. Ruta para consultar todos los Usuarios
@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    user = Usuario.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200

# 12. Ruta para agregar usuario
@app.route('/usuarios', methods=['POST'])
def addUsuario():
    user = Usuario()
    # asignar a variables lo que recibo mediante post
    user.primer_nombre = request.json.get('primer_nombre')
    user.segundo_nombre = request.json.get('segundo_nombre')
    user.apellido_paterno = request.json.get('apellido_paterno')
    user.apellido_materno = request.json.get('apellido_materno')
    user.direccion = request.json.get('direccion')

    Usuario.save(user)

    return jsonify(user.serialize()),200

# 13. Creamos método para consultar un usuario en específico
@app.route('/usuarios/<id>', methods=['GET'])
def getUsuario(id):
    user = Usuario.query.get(id)
    return jsonify(user.serialize()),200

# 14. Borrar usuario en específico
@app.route('/usuarios/<id>', methods=['DELETE'])
def deleteUsuario(id):
    user = Usuario.query.get(id)
    Usuario.delete(user)
    return jsonify(user.serialize()),200

# 15. Modificar Usuario
@app.route('/usuarios/<id>', methods=['PUT'])
def updateUsuario(id):
    user = Usuario.query.get(id)

    user.primer_nombre = request.json.get('primer_nombre')
    user.segundo_nombre = request.json.get('segundo_nombre')
    user.apellido_paterno = request.json.get('apellido_paterno')
    user.apellido_materno = request.json.get('apellido_materno')
    user.direccion = request.json.get('direccion')
    user.email = request.json.get('email')
    user.password = request.json.get('password')

    Usuario.update(user)

    return jsonify(user.serialize()),200

######## Regiones #########
@app.route('/regiones', methods=['GET'])
def getRegiones():
    regiones = Regiones.query.all()
    regiones = list(map(lambda x: x.serialize(), regiones))
    return jsonify(regiones),200

######## Provincia #########
@app.route('/provincias', methods=['GET'])
def getProvincias():
    provincias = Provincias.query.all()
    provincias = list(map(lambda x: x.serialize(), provincias))
    return jsonify(provincias),200

######## Comunas #########
@app.route('/comunas', methods=['GET'])
def getComunas():
    comunas = Comunas.query.all()
    comunas = list(map(lambda x: x.serialize(), comunas))
    return jsonify(comunas),200

# obtener listado de todas las comunas de la región solicitada
@app.route('/regiones/<id>/comunas', methods=['GET'])
def getComunasByRegion(id):
    #comunas = db.session.query(Comunas).filter(Regiones.id == id).filter(Provincias.region_id == id).filter(Comunas.provincia_id == Provincias.id)
    comunas = db.session.query(Comunas).select_from(Comunas).join(Provincias).join(Regiones).filter(Provincias.region_id == id).filter(Comunas.provincia_id == Provincias.id).all()
    #print(comunas)  
    comunas = list(map(lambda x: x.serialize(), comunas))
    return jsonify(comunas),200

######### Clientes #########
@app.route('/clientes', methods=['GET'])
def getClientes():
    clientes = Clientes.query.all()
    clientes = list(map(lambda x: x.serialize(), clientes))
    return jsonify(clientes),200

@app.route('/clientes', methods=['POST'])
def addCliente():
    cliente = Clientes()

    cliente.id = request.json.get('id')
    cliente.rut = request.json.get('rut')
    cliente.nombre = request.json.get('nombre')
    cliente.apellido_paterno = request.json.get('apellido_paterno')
    cliente.apellido_materno = request.json.get('apellido_materno')
    cliente.direccion = request.json.get('direccion')
    cliente.comunas_id = request.json.get('comunas_id')
    cliente.email = request.json.get('email')
    cliente.password = request.json.get('password')
    cliente.telefono = request.json.get('telefono')

    Clientes.save(cliente)

    return jsonify(cliente.serialize()),200

@app.route('/clientes/<id>', methods=['GET'])
def getCliente(id):
    cliente = Clientes.query.get(id)
    return jsonify(cliente.serialize()),200

@app.route('/clientes/<id>', methods=['DELETE'])
def deleteCliente(id):
    cliente = Clientes.query.get(id)
    Clientes.delete(cliente)
    return jsonify(cliente.serialize()),200

@app.route('/clientes/<id>', methods=['PUT'])
def updateCliente(id):
    cliente = Clientes.query.get(id)

    cliente.rut = request.json.get('rut')
    cliente.nombre = request.json.get('nombre')
    cliente.apellido_paterno = request.json.get('apellido_paterno')
    cliente.apellido_materno = request.json.get('apellido_materno')
    cliente.direccion = request.json.get('direccion')
    cliente.comunas_id = request.json.get('comunas_id')
    cliente.email = request.json.get('email')
    cliente.password = request.json.get('password')
    cliente.telefono = request.json.get('telefono')

    Clientes.update(cliente)

    return jsonify(cliente.serialize()),200

######### Suscripciones #########
@app.route('/suscripciones', methods=['GET'])
def getSuscripciones():
    suscripciones = Suscripciones.query.all()
    suscripciones = list(map(lambda x: x.serialize(), suscripciones))
    return jsonify(suscripciones),200

@app.route('/suscripciones', methods=['POST'])
def addSuscripcion():
    suscripcion = Suscripciones()

    suscripcion.id = request.json.get('id')
    suscripcion.cliente_id = request.json.get('cliente_id')
    suscripcion.fecha_inicio = request.json.get('fecha_inicio')
    suscripcion.fecha_termino = request.json.get('fecha_termino')
    suscripcion.estado = request.json.get('estado')

    Suscripciones.save(suscripcion)

    return jsonify(suscripcion.serialize()),200

@app.route('/suscripciones/<id>', methods=['GET'])
def getSuscripcion(id):
    suscripcion = Suscripciones.query.get(id)
    return jsonify(suscripcion.serialize()),200

@app.route('/suscripciones/<id>', methods=['DELETE'])
def deleteSuscripcion(id):
    suscripcion = Suscripciones.query.get(id)
    Suscripciones.delete(suscripcion)
    return jsonify(suscripcion.serialize()),200

@app.route('/suscripciones/<id>', methods=['PUT'])
def updateSuscripcion(id):
    suscripcion = Suscripciones.query.get(id)

    suscripcion.cliente_id = request.json.get('cliente_id')
    suscripcion.fecha_inicio = request.json.get('fecha_inicio')
    suscripcion.fecha_termino = request.json.get('fecha_termino')
    suscripcion.estado = request.json.get('estado')

    Suscripciones.update(suscripcion)

    return jsonify(suscripcion.serialize()),200

######### Donaciones #########
@app.route('/donaciones', methods=['GET'])
def getDonaciones():
    donaciones = Donaciones.query.all()
    donaciones = list(map(lambda x: x.serialize(), donaciones))
    return jsonify(donaciones),200

@app.route('/donaciones', methods=['POST'])
def addDonacion():
    donacion = Donaciones()

    donacion.id = request.json.get('id')
    donacion.cliente_id = request.json.get('cliente_id')
    donacion.fecha_donacion = request.json.get('fecha_donacion')
    donacion.monto_donacion = request.json.get('monto_donacion')
    donacion.estado = request.json.get('estado')

    donacion.password = request.json.get('password')

    Donaciones.save(donacion)

    return jsonify(donacion.serialize()),200

@app.route('/donaciones/<id>', methods=['GET'])
def getDonacion(id):
    donacion = Donaciones.query.get(id)
    return jsonify(donacion.serialize()),200

@app.route('/donaciones/<id>', methods=['DELETE'])
def deleteDonacion(id):
    donacion = Donaciones.query.get(id)
    Donaciones.delete(donacion)
    return jsonify(donacion.serialize()),200

@app.route('/donaciones/<id>', methods=['PUT'])
def updateDonacion(id):
    donacion = Donaciones.query.get(id)

    donacion.cliente_id = request.json.get('cliente_id')
    donacion.fecha_donacion = request.json.get('fecha_donacion')
    donacion.monto_donacion = request.json.get('monto_donacion')
    donacion.estado = request.json.get('estado')

    donacion.password = request.json.get('password')

    Donaciones.update(donacion)

    return jsonify(donacion.serialize()),200

######### Descuentos #########
@app.route('/descuentos', methods=['GET'])
def getDescuentos():
    descuentos = Descuentos.query.all()
    descuentos = list(map(lambda x: x.serialize(), descuentos))
    return jsonify(descuentos),200

@app.route('/descuentos', methods=['POST'])
def addDescuento():
    descuento = Descuentos()

    descuento.id = request.json.get('id')
    descuento.nombre = request.json.get('nombre')
    descuento.fecha = request.json.get('fecha')
    descuento.porcentaje = request.json.get('porcentaje')
    descuento.estado = request.json.get('estado')

    Descuentos.save(descuento)

    return jsonify(descuento.serialize()),200

@app.route('/descuentos/<id>', methods=['GET'])
def getDescuento(id):
    descuento = Descuentos.query.get(id)
    return jsonify(descuento.serialize()),200

@app.route('/descuentos/<id>', methods=['DELETE'])
def deleteDescuento(id):
    descuento = Descuentos.query.get(id)
    Descuentos.delete(descuento)
    return jsonify(descuento.serialize()),200

@app.route('/descuentos/<id>', methods=['PUT'])
def updateDescuento(id):
    descuento = Descuentos.query.get(id)

    descuento.nombre = request.json.get('nombre')
    descuento.fecha = request.json.get('fecha')
    descuento.porcentaje = request.json.get('porcentaje')
    descuento.estado = request.json.get('estado')

    Descuentos.update(descuento)

    return jsonify(descuento.serialize()),200

######### Productos #########
@app.route('/productos', methods=['GET'])
def getProductos():
    productos = Productos.query.filter(Productos.estado == 1).all()
    productos = list(map(lambda x: x.serialize(), productos))
    return jsonify(productos),200

@app.route('/productos', methods=['POST'])
def addProducto():
    producto = Productos()

    producto.id = request.json.get('id')
    producto.codigo = request.json.get('codigo')
    producto.nombre = request.json.get('nombre')
    producto.valor_venta = request.json.get('valor_venta')
    producto.stock = request.json.get('stock')
    producto.descripcion = request.json.get('descripcion')
    producto.imagen = request.json.get('imagen')
    producto.estado = request.json.get('estado')

    Productos.save(producto)

    return jsonify(producto.serialize()),200

@app.route('/productos/<id>', methods=['GET'])
def getProducto(id):
    producto = Productos.query.get(id)
    return jsonify(producto.serialize()),200

@app.route('/productos/<id>', methods=['DELETE'])
def deleteProducto(id):
    producto = Productos.query.get(id)
    Productos.delete(producto)
    return jsonify(producto.serialize()),200

@app.route('/productos/<id>', methods=['PUT'])
def updateProducto(id):
    producto = Productos.query.get(id)

    producto.codigo = request.json.get('codigo')
    producto.nombre = request.json.get('nombre')
    producto.valor_venta = request.json.get('valor_venta')
    producto.stock = request.json.get('stock')
    producto.descripcion = request.json.get('descripcion')
    producto.imagen = request.json.get('imagen')
    producto.estado = request.json.get('estado')

    Productos.update(producto)

    return jsonify(producto.serialize()),200

######### Descuentos_Productos #########
@app.route('/descuentos_productos', methods=['GET'])
def getDescuentosProductos():
    descuentos_productos = Descuentos_Productos.query.all()
    descuentos_productos = list(map(lambda x: x.serialize(), descuentos_productos))
    return jsonify(descuentos_productos),200

@app.route('/descuentos_productos', methods=['POST'])
def addDescuentosProducto():
    descuentos_producto = Descuentos_Productos()

    descuentos_producto.id = request.json.get('id')
    descuentos_producto.producto_id = request.json.get('producto_id')
    descuentos_producto.descuento_id = request.json.get('descuento_id')
    descuentos_producto.estado = request.json.get('estado')

    Descuentos_Productos.save(descuentos_producto)

    return jsonify(descuentos_producto.serialize()),200

@app.route('/descuentos_productos/<id>', methods=['GET'])
def getDescuentosProducto(id):
    descuentos_producto = Descuentos_Productos.query.get(id)
    return jsonify(descuentos_producto.serialize()),200

@app.route('/descuentos_productos/<id>', methods=['DELETE'])
def deleteDescuentosProducto(id):
    descuentos_producto = Descuentos_Productos.query.get(id)
    Descuentos_Productos.delete(descuentos_producto)
    return jsonify(descuentos_producto.serialize()),200

@app.route('/descuentos_productos/<id>', methods=['PUT'])
def updateDescuentosProducto(id):
    descuentos_producto = Descuentos_Productos.query.get(id)

    descuentos_producto.producto_id = request.json.get('producto_id')
    descuentos_producto.descuento_id = request.json.get('descuento_id')
    descuentos_producto.estado = request.json.get('estado')

    Descuentos_Productos.update(descuentos_producto)

    return jsonify(descuentos_producto.serialize()),200

######### Vendedores #########
@app.route('/vendedores', methods=['GET'])
def getVendedores():
    vendedores = Vendedores.query.all()
    vendedores = list(map(lambda x: x.serialize(), vendedores))
    return jsonify(vendedores),200

@app.route('/vendedores', methods=['POST'])
def addVendedor():
    vendedor = Vendedores()

    vendedor.id = request.json.get('id')
    vendedor.primer_nombre = request.json.get('primer_nombre')
    vendedor.segundo_nombre = request.json.get('segundo_nombre')
    vendedor.apellido_paterno = request.json.get('apellido_paterno')
    vendedor.apellido_materno = request.json.get('apellido_materno')
    vendedor.direccion = request.json.get('direccion')
    vendedor.password = request.json.get('password')
    vendedor.email = request.json.get('email')
    vendedor.telefono = request.json.get('telefono')
    vendedor.estado = request.json.get('estado')

    Vendedores.save(vendedor)

    return jsonify(vendedor.serialize()),200

@app.route('/vendedores/<id>', methods=['GET'])
def getVendedor(id):
    vendedor = Vendedores.query.get(id)
    return jsonify(vendedor.serialize()),200

@app.route('/vendedores/<id>', methods=['DELETE'])
def deleteVendedor(id):
    vendedor = Vendedores.query.get(id)
    Vendedores.delete(vendedor)
    return jsonify(vendedor.serialize()),200

@app.route('/vendedores/<id>', methods=['PUT'])
def updateVendedor(id):
    vendedor = Vendedores.query.get(id)

    vendedor.primer_nombre = request.json.get('primer_nombre')
    vendedor.segundo_nombre = request.json.get('segundo_nombre')
    vendedor.apellido_paterno = request.json.get('apellido_paterno')
    vendedor.apellido_materno = request.json.get('apellido_materno')
    vendedor.direccion = request.json.get('direccion')
    vendedor.password = request.json.get('password')
    vendedor.email = request.json.get('email')
    vendedor.telefono = request.json.get('telefono')
    vendedor.estado = request.json.get('estado')

    Vendedores.update(vendedor)

    return jsonify(vendedor.serialize()),200

######### Ventas #########
@app.route('/ventas', methods=['GET'])
def getVentas():
    ventas = Ventas.query.all()
    ventas = list(map(lambda x: x.serialize(), ventas))
    return jsonify(ventas),200

@app.route('/ventas', methods=['POST'])
def addVenta():
    venta = Ventas()

    venta.id = request.json.get('id')
    venta.vendedor_id = request.json.get('vendedor_id')
    venta.cliente_id = request.json.get('cliente_id')
    venta.descuento_id = request.json.get('descuento_id')
    venta.fecha = request.json.get('fecha')
    venta.total = request.json.get('total')
    venta.iva = request.json.get('iva')
    venta.estado = request.json.get('estado')

    Ventas.save(venta)

    return jsonify(venta.serialize()),200

@app.route('/ventas/<id>', methods=['GET'])
def getVenta(id):
    venta = Ventas.query.get(id)
    return jsonify(venta.serialize()),200

@app.route('/ventas/<id>', methods=['DELETE'])
def deleteVenta(id):
    venta = Ventas.query.get(id)
    Ventas.delete(venta)
    return jsonify(venta.serialize()),200

@app.route('/ventas/<id>', methods=['PUT'])
def updateVenta(id):
    venta = Ventas.query.get(id)

    venta.vendedor_id = request.json.get('vendedor_id')
    venta.cliente_id = request.json.get('cliente_id')
    venta.descuento_id = request.json.get('descuento_id')
    venta.fecha = request.json.get('fecha')
    venta.total = request.json.get('total')
    venta.iva = request.json.get('iva')
    venta.estado = request.json.get('estado')

    Ventas.update(venta)

    return jsonify(venta.serialize()),200

######### Detalle_Ventas #########
@app.route('/detalle_ventas', methods=['GET'])
def getDetalleVentas():
    detalle_ventas = Detalle_Ventas.query.all()
    detalle_ventas = list(map(lambda x: x.serialize(), detalle_ventas))
    return jsonify(detalle_ventas),200

@app.route('/detalle_ventas', methods=['POST'])
def addDetalleVenta():
    detalle_venta = Detalle_Ventas()

    detalle_venta.id = request.json.get('id')
    detalle_venta.venta_id = request.json.get('venta_id')
    detalle_venta.producto_id = request.json.get('producto_id')
    detalle_venta.cantidad = request.json.get('cantidad')
    detalle_venta.precio = request.json.get('precio')
    detalle_venta.descuento = request.json.get('descuento')
    detalle_venta.estado = request.json.get('estado')

    Detalle_Ventas.save(detalle_venta)

    return jsonify(detalle_venta.serialize()),200

@app.route('/detalle_ventas/<id>', methods=['GET'])
def getDetalleVenta(id):
    detalle_venta = Detalle_Ventas.query.get(id)
    return jsonify(detalle_venta.serialize()),200

@app.route('/detalle_ventas/<id>', methods=['DELETE'])
def deleteDetalleVenta(id):
    detalle_venta = Detalle_Ventas.query.get(id)
    Detalle_Ventas.delete(detalle_venta)
    return jsonify(detalle_venta.serialize()),200

@app.route('/detalle_ventas/<id>', methods=['PUT'])
def updateDetalleVenta(id):
    detalle_venta = Detalle_Ventas.query.get(id)

    detalle_venta.venta_id = request.json.get('venta_id')
    detalle_venta.producto_id = request.json.get('producto_id')
    detalle_venta.cantidad = request.json.get('cantidad')
    detalle_venta.precio = request.json.get('precio')
    detalle_venta.descuento = request.json.get('descuento')
    detalle_venta.estado = request.json.get('estado')

    Detalle_Ventas.update(detalle_venta)

    return jsonify(detalle_venta.serialize()),200

######### Despachos #########
@app.route('/despachos', methods=['GET'])
def getDespachos():
    despachos = Despachos.query.all()
    despachos = list(map(lambda x: x.serialize(), despachos))
    return jsonify(despachos),200

@app.route('/despachos', methods=['POST'])
def addDespacho():
    despacho = Despachos()

    despacho.id = request.json.get('id')
    despacho.fecha_entrega = request.json.get('fecha_entrega')
    despacho.hora_entrega = request.json.get('hora_entrega')
    despacho.rut_recibe = request.json.get('rut_recibe')
    despacho.nombre_recibe = request.json.get('nombre_recibe')
    despacho.direccion = request.json.get('direccion')
    despacho.venta_id = request.json.get('venta_id')
    despacho.cliente_id = request.json.get('cliente_id')

    Despachos.save(despacho)

    return jsonify(despacho.serialize()),200

@app.route('/despachos/<id>', methods=['GET'])
def getDespacho(id):
    despacho = Despachos.query.get(id)
    return jsonify(despacho.serialize()),200

@app.route('/despachos/<id>', methods=['DELETE'])
def deleteDespacho(id):
    despacho = Despachos.query.get(id)
    Despachos.delete(despacho)
    return jsonify(despacho.serialize()),200

@app.route('/despachos/<id>', methods=['PUT'])
def updateDespacho(id):
    despacho = Despachos.query.get(id)

    despacho.fecha_entrega = request.json.get('fecha_entrega')
    despacho.hora_entrega = request.json.get('hora_entrega')
    despacho.rut_recibe = request.json.get('rut_recibe')
    despacho.nombre_recibe = request.json.get('nombre_recibe')
    despacho.direccion = request.json.get('direccion')
    despacho.venta_id = request.json.get('venta_id')
    despacho.cliente_id = request.json.get('cliente_id')

    Despachos.update(despacho)

    return jsonify(despacho.serialize()),200


######### Final #########

# 8. comando para iniciar mi app flask:     flask db init
# 9. comando para migrar mis modelos:       flask db migrate
# 10. comando para crear nuestros modelos como tablas : flask db upgrade
# 11. comando para iniciar la app flask:    flask run

# 4. Configurar los puertos nuestra app
# va al final del código de este archivo
if __name__ == '__main__':
    app.run(port=5000, debug=True)