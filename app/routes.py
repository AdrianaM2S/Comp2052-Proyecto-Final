from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import LibroForm, ChangePasswordForm
from app.models import db, Libro, User

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password actualizada exitosamente')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra libros a los usuarios con el rol de "Admin",
    "Lector" y "Bibliotecario".
    """
    if current_user.role.name == 'Lector':
        libro = Libro.query.all()
    else:
        libro = Libro.query.filter_by(bibliotecario_id=current_user.id).all()

    return render_template('dashboard.html', libro=libro)

@main.route('/libros', methods=['GET', 'POST'])
@login_required
def libros():
    """
    Permite crear un nuevo libro. Solo disponible para los admins y bibliotecarios.
    """
    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            isbn=form.isbn.data,
            categoria=form.categoria.data,
            estado=form.estado.data,
            anio_publicacion=form.anio_publicacion.data,
            bibliotecario_id=current_user.id
        )
        db.session.add(libro)
        db.session.commit()
        flash("Libro creado de manera exitosa.")  
        return redirect(url_for('main.dashboard'))

    return render_template('libro_form.html', form=form)

@main.route('/libros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    """
    Permite editar un libro existente. Solo si es admin o el bibliotecario.
    """
    libro = Libro.query.get_or_404(id)

    # Validación de permisos
    if current_user.role.name not in ['Admin', 'Bibliotecario'] or (
        libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        flash('Tu no tienes el permiso para editar este libro.')  
        return redirect(url_for('main.dashboard'))

    form = LibroForm(obj=libro)

    if form.validate_on_submit():
        libro.titulo = form.titulo.data
        libro.autor = form.autor.data
        libro.isbn = form.isbn.data
        libro.categoria = form.categoria.data
        libro.estado = form.estado.data
        libro.anio_publiocacion = form.anio_publicacion.data
        db.session.commit()
        flash("El libro fue editado de manera exitosa.")  
        return redirect(url_for('main.dashboard'))

    return render_template('libro_form.html', form=form, editar=True) 

@main.route('/libros/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_libro(id):
    """
    Elimina un libro si el usuario es admin o bibliotecario.
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] or (
        libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        flash('Tu no tienes el perimso para eliminar el libro.')  
        return redirect(url_for('main.dashboard'))

    db.session.delete(libro)
    db.session.commit()
    flash("El libro fue borrado de manera exitosa.")  
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("Tu no tienes el permiso para ver esta pagina.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)