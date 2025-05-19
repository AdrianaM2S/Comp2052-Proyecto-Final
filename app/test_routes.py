from flask import Blueprint, request, jsonify
from app.models import db, Libro

# Blueprint solo con endpoints de prueba para libros
main = Blueprint('main', __name__)

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/libro', methods=['GET'])
def listar_libro():
    """
    Retorna una lista de los libros (JSON).
    """
    libro = Libro.query.all()

    data = [
        {'id': libro.id, 
        'titulo': libro.titulo, 
        'autor': libro.autor, 
        'isbn': libro.isbn, 
        'categoria': libro.categoria, 
        'estado': libro.estado, 
        'anio_pubilcacion': libro.anio_publicacion, 
        'bibliotecario_id': libro.bibliotecario_id}
        for libro in libro
    ]
    return jsonify(data), 200


@main.route('/libro/<int:id>', methods=['GET'])
def listar_un_libro(id):
    """
    Retorna un solo libro por su ID (JSON).
    """
    libro = Libro.query.get_or_404(id)

    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'isbn': libro.isbn,
        'categoria': libro.categoria,
        'estado': libro.estado,
        'anio_publicacion': libro.anio_publicacion,
        'bibliotecario_id': libro.bibliotecario_id
    }

    return jsonify(data), 200


@main.route('/libro', methods=['POST'])
def crear_libro():
    """
    Crea un libro sin validación.
    Espera JSON con 'titulo', 'autor', 'isbn', 'categoria', 'estado', 'anio_publicacion' y 'bibliotecario_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se entraron datos'}), 400

    libro = Libro(
        titulo=data.get('titulo'),
        autor=data.get('autor'),
        isbn=data.get('isbn'),
        categoria=data.get('categoria'),
        estado=data.get('estado'),
        anio_publicacion=data.get('anio_publicacion'),
        bibliotecario_id=data.get('bibliotecario_id')  # sin validación de usuario
    )

    db.session.add(libro)
    db.session.commit()

    return jsonify({'message': 'Libro creado', 'id': libro.id, 'bibliotecario_id': libro.bibliotecario_id}), 201

@main.route('/libro/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    """
    Actualiza un libro sin validación de usuario o permisos.
    """
    libro = Libro.query.get_or_404(id)
    data = request.get_json()

    libro.titulo = data.get('titulo', libro.titulo)
    libro.autor = data.get('autor', libro.autor)
    libro.isbn = data.get('isbn', libro.isbn)
    libro.categoria = data.get('categoria', libro.categoria)
    libro.estado = data.get('estado', libro.estado)
    libro.anio_publicacion = data.get('anio_publicacion', libro.anio_publicacion)
    libro.bibliotecario_id = data.get('bibliotecario_id', libro.bibliotecario_id)

    db.session.commit()

    return jsonify({'message': 'libro actualizado', 'id': libro.id}), 200

@main.route('/libro/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    """
    Elimina un libro sin validación de permisos.
    """
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()

    return jsonify({'message': 'Libro eliminado', 'id': libro.id}), 200