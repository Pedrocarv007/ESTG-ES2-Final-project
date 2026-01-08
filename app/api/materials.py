
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.material import Material, Folder
from app.config.database import db
import os
from werkzeug.utils import secure_filename

materials_api = Blueprint('materials_api', __name__, url_prefix='/materials')




@materials_api.route('/upload', methods=['POST'])
@login_required
def upload_material():
	from app.forms.material_forms import MaterialUploadForm
	form = MaterialUploadForm()
	form.group_id.choices = [(g.id, g.name) for g in current_user.get_groups()]
	if form.validate_on_submit():
		file = form.file.data
		filename = secure_filename(file.filename)
		upload_dir = os.path.join('app', 'static', 'uploads')
		os.makedirs(upload_dir, exist_ok=True)
		file_path = os.path.join(upload_dir, filename)
		file.save(file_path)
		material = Material(
			title=form.title.data,
			description=form.description.data,
			file_path=file_path,
			file_name=filename,
			file_type=file.content_type,
			file_size=os.path.getsize(file_path),
			uploaded_by=current_user.id,
			group_id=form.group_id.data
		)
		db.session.add(material)
		db.session.commit()
		flash('Arquivo enviado com sucesso!', 'success')
	else:
		flash('Erro ao enviar arquivo.', 'danger')
	return redirect(url_for('dashboard_api.dashboard'))

@materials_api.route('/explorer_full/<int:folder_id>/new_folder', methods=['POST'])
@login_required
def new_folder(folder_id):
	name = request.form.get('name', '').strip()
	if not name:
		flash('Nome da pasta é obrigatório.', 'danger')
		return redirect(url_for('materials_api.explorer_full', folder_id=folder_id if folder_id else None))
	if folder_id == 0:
		# Criar na raiz do grupo (pega group_id do usuário ou query param)
		group_id = request.args.get('group_id', type=int)
		if not group_id and hasattr(current_user, 'groups') and current_user.groups:
			group_id = current_user.groups[0].id
		if not group_id:
			flash('Grupo não encontrado para criar pasta na raiz.', 'danger')
			return redirect(url_for('materials_api.explorer_full'))
		folder = Folder(name=name, parent_id=None, group_id=group_id)
	else:
		parent = Folder.query.get_or_404(folder_id)
		folder = Folder(name=name, parent_id=parent.id, group_id=parent.group_id)
	db.session.add(folder)
	db.session.commit()
	flash('Pasta criada com sucesso!', 'success')
	return redirect(url_for('materials_api.explorer_full', folder_id=folder.parent_id or folder.id))

@materials_api.route('/explorer_full/<int:folder_id>/upload', methods=['POST'])
@login_required
def upload_to_folder(folder_id):
	from app.forms.material_forms import MaterialUploadForm
	form = MaterialUploadForm()
	parent = Folder.query.get_or_404(folder_id)
	form.group_id.choices = [(parent.group_id, 'Grupo')]  # só permite o grupo da pasta
	if form.validate_on_submit():
		file = form.file.data
		filename = secure_filename(file.filename)
		upload_dir = os.path.join('app', 'static', 'uploads')
		os.makedirs(upload_dir, exist_ok=True)
		file_path = os.path.join(upload_dir, filename)
		file.save(file_path)
		material = Material(
			title=form.title.data,
			description=form.description.data,
			file_path=file_path,
			file_name=filename,
			file_type=file.content_type,
			file_size=os.path.getsize(file_path),
			uploaded_by=current_user.id,
			group_id=parent.group_id,
			folder_id=folder_id
		)
		db.session.add(material)
		db.session.commit()
		flash('Arquivo enviado com sucesso!', 'success')
	else:
		flash('Erro ao enviar arquivo.', 'danger')
	return redirect(url_for('materials_api.explorer_full', folder_id=folder_id))


@materials_api.route('/explorer_full', defaults={'folder_id': None})
@materials_api.route('/explorer_full/<int:folder_id>')
@login_required
def explorer_full(folder_id):
	# Sidebar: todas as pastas raiz de todos os grupos do usuário
	user_groups = getattr(current_user, 'groups', [])
	group_ids = [g.id for g in user_groups]
	sidebar_folders = Folder.query.filter(Folder.parent_id==None, Folder.group_id.in_(group_ids)).all() if group_ids else []
	# Conteúdo da pasta atual
	if folder_id:
		folder = Folder.query.get_or_404(folder_id)
		breadcrumbs = []
		f = folder
		while f:
			breadcrumbs.insert(0, f)
			f = f.parent
		subfolders = folder.subfolders
		materials = folder.materials
		current_folder_id = folder.id
	else:
		subfolders = sidebar_folders
		materials = []
		breadcrumbs = []
		current_folder_id = None
	return render_template('materials_explorer_full.html',
		sidebar_folders=sidebar_folders,
		subfolders=subfolders,
		materials=materials,
		breadcrumbs=breadcrumbs,
		current_folder_id=current_folder_id)


@materials_api.route('/folder/<int:folder_id>/rename', methods=['POST'])
@login_required
def rename_folder(folder_id):
	folder = Folder.query.get_or_404(folder_id)
	new_name = request.form.get('name', '').strip()
	if not new_name:
		return {'error': 'Nome não pode ser vazio.'}, 400
	folder.name = new_name
	db.session.commit()
	return {'success': True, 'name': folder.name}

@materials_api.route('/material/<int:material_id>/rename', methods=['POST'])
@login_required
def rename_material(material_id):
	material = Material.query.get_or_404(material_id)
	new_title = request.form.get('title', '').strip()
	if not new_title:
		return {'error': 'Título não pode ser vazio.'}, 400
	material.title = new_title
	db.session.commit()
	return {'success': True, 'title': material.title}
