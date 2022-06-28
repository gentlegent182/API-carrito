from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(250), nullable= False)
    segundo_nombre = db.Column(db.String(250), nullable= True)
    apellido_paterno = db.Column(db.String(250), nullable= False)
    apellido_materno = db.Column(db.String(250), nullable= True)
    direccion = db.Column(db.String(250), nullable= False)
    password = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "direccion": self.direccion,
            "password": self.password,
            "email": self.email
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Regiones(db.Model):
    __tablename__ = 'Regiones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)
    numero = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre
        }

class Provincias(db.Model):
    __tablename__ = 'Provincias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)
    region_id = db.Column(db.Integer, db.ForeignKey('Regiones.id'), nullable=False)
    region = db.relationship('Regiones', backref=db.backref('provincias', lazy=True))

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "region_id": self.region_id
        }


class Comunas(db.Model):
    __tablename__ = 'Comunas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('Provincias.id'), nullable=False)
    provincia = db.relationship('Provincias', backref=db.backref('comunas', lazy=True))

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "provincia_id": self.provincia_id
        }

class Clientes(db.Model):
    __tablename__ = 'Clientes'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(250), nullable= False)
    nombre = db.Column(db.String(250), nullable= False)
    apellido_paterno = db.Column(db.String(250), nullable= False)
    apellido_materno = db.Column(db.String(250), nullable= True)
    direccion = db.Column(db.String(250), nullable= False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('Comunas.id'), nullable= False)
    comuna = db.relationship('Comunas', backref=db.backref('clientes', lazy='dynamic'))
    email = db.Column(db.String(250), nullable=True)
    password = db.Column(db.String(250), nullable=True)
    telefono = db.Column(db.String(250), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "rut": self.rut,
            "nombre": self.nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "direccion": self.direccion,
            "comuna_id": self.comuna_id,
            "email": self.email,
            "password": self.password,
            "telefono": self.telefono
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Suscripciones(db.Model):
    __tablename__ = 'Suscripciones'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable= False)
    cliente = db.relationship('Clientes', backref=db.backref('suscripciones', lazy='dynamic'))
    fecha_inicio = db.Column(db.DateTime, nullable= False)
    fecha_termino = db.Column(db.DateTime, nullable= False)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "cliente_id": self.cliente_id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_termino": self.fecha_termino,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Donaciones(db.Model):
    __tablename__ = 'Donaciones'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable= False)
    cliente = db.relationship('Clientes', backref=db.backref('donaciones', lazy='dynamic'))
    fecha_donacion = db.Column(db.DateTime, nullable= False)
    monto_donacion = db.Column(db.Integer, nullable= False)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "cliente_id": self.cliente_id,
            "fecha_donacion": self.fecha_donacion,
            "monto_donacion": self.monto_donacion,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Descuentos(db.Model):
    __tablename__ = 'Descuentos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)
    fecha = db.Column(db.DateTime, nullable= False)
    porcentaje = db.Column(db.Integer, nullable= False)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "porcentaje": self.porcentaje,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Productos(db.Model):
    __tablename__ = 'Productos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(250), nullable= False)
    nombre = db.Column(db.String(250), nullable= False)
    valor_venta = db.Column(db.Integer, nullable= False)
    stock = db.Column(db.Integer, nullable= False)
    descripcion = db.Column(db.String(250), nullable= False)
    imagen = db.Column(db.String(250), nullable= False)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "valor_venta": self.valor_venta,
            "stock": self.stock,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Descuentos_Productos(db.Model):
    __tablename__ = 'Descuentos_Productos'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('Productos.id'), nullable= False)
    producto = db.relationship('Productos', backref=db.backref('descuentos_productos', lazy='dynamic'))
    descuento_id = db.Column(db.Integer, db.ForeignKey('Descuentos.id'), nullable= False)
    descuento = db.relationship('Descuentos', backref=db.backref('descuentos_productos', lazy='dynamic'))
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "producto_id": self.producto_id,
            "descuento_id": self.descuento_id,
            "estado": self.estado
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Vendedores(db.Model):
    __tablename__ = 'Vendedores'
    id = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(250), nullable= False)
    segundo_nombre = db.Column(db.String(250), nullable= True)
    apellido_paterno = db.Column(db.String(250), nullable= False)
    apellido_materno = db.Column(db.String(250), nullable= True)
    direccion = db.Column(db.String(250), nullable= False)
    password = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    telefono = db.Column(db.String(250), nullable=False)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "direccion": self.direccion,
            "password": self.password,
            "email": self.email,
            "telefono": self.telefono,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Ventas(db.Model):
    __tablename__ = 'Ventas'
    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('Vendedores.id'), nullable= False)
    vendedor = db.relationship('Vendedores', backref=db.backref('ventas', lazy='dynamic'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable= False)
    cliente = db.relationship('Clientes', backref=db.backref('ventas', lazy='dynamic'))
    descuento = db.Column(db.Integer, nullable= True)
    fecha = db.Column(db.DateTime, nullable= False)
    total = db.Column(db.Integer, nullable= False)
    iva = db.Column(db.Integer, nullable= False)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "vendedor_id": self.vendedor_id,
            "cliente_id": self.cliente_id,
            "descuento": self.descuento,
            "fecha": self.fecha,
            "total": self.total,
            "iva": self.iva,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Detalle_Ventas(db.Model):
    __tablename__ = 'Detalle_Ventas'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('Ventas.id'), nullable= False)
    venta = db.relationship('Ventas', backref=db.backref('detalle_ventas', lazy='dynamic'))
    producto_id = db.Column(db.Integer, db.ForeignKey('Productos.id'), nullable= False)
    producto = db.relationship('Productos', backref=db.backref('detalle_ventas', lazy='dynamic'))
    cantidad = db.Column(db.Integer, nullable= False)
    precio = db.Column(db.Integer, nullable= False)
    descuento = db.Column(db.Integer, nullable= True)
    estado = db.Column(db.String(250), nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "venta_id": self.venta_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "descuento": self.descuento,
            "estado": self.estado
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Despachos(db.Model):
    __tablename__ = 'Despachos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrega = db.Column(db.DateTime, nullable= True)
    hora_entrega = db.Column(db.Time, nullable= True)
    rut_recibe = db.Column(db.String(250), nullable= True)
    nombre_recibe = db.Column(db.String(250), nullable= True)
    direccion = db.Column(db.String(250), nullable= False)
    venta_id = db.Column(db.Integer, db.ForeignKey('Ventas.id'), nullable= False)
    venta = db.relationship('Ventas', backref=db.backref('despachos', lazy='dynamic'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable= False)
    cliente = db.relationship('Clientes', backref=db.backref('despachos', lazy='dynamic'))

    def serialize(self):
        return{
            "id": self.id,
            "fecha_entrega": self.fecha_entrega,
            "hora_entrega": self.hora_entrega,
            "rut_recibe": self.rut_recibe,
            "nombre_recibe": self.nombre_recibe,
            "direccion": self.direccion,
            "venta_id": self.venta_id,
            "cliente_id": self.cliente_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()