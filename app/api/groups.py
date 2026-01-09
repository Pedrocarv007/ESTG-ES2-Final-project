from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app.models.group import Group
from app.forms.group_forms import GroupCreateForm, GroupEditForm
from app.config.database import db

groups_api = Blueprint('groups_api', __name__, url_prefix='/groups')

@groups_api.route('/')
def groups():
	q = request.args.get('q', '').strip()
	group_type = request.args.get('type', 'all')
	query = Group.query
	if q:
		query = query.filter(Group.name.ilike(f'%{q}%'))
	if group_type == 'public':
		query = query.filter(Group.is_active == True)
	elif group_type == 'private':
		query = query.filter(Group.is_active == False)
	all_groups = query.order_by(Group.created_at.desc()).all()
	return render_template('groups.html', active_page='groups', groups=all_groups, q=q, group_type=group_type)

@groups_api.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
	form = GroupCreateForm()
	if form.validate_on_submit():
		group = Group(
			name=form.name.data,
			subject=form.subject.data,
			description=form.description.data,
			goals=form.goals.data,
			max_members=form.max_members.data or 50,
			is_active=form.is_active.data,
			created_by=current_user.id
		)
		db.session.add(group)
		db.session.commit()
		group.add_member(current_user, role='admin')
		db.session.commit()
		# Forçar refresh do objeto current_user para garantir associação
		try:
			db.session.refresh(current_user)
		except Exception:
			pass
		# Criar pasta do grupo no explorer
		from app.models.material import Folder, Material
		from app.config.database import db as _db
		folder = Folder(name=group.name, parent_id=None, group_id=group.id)
		_db.session.add(folder)
		_db.session.commit()
		# Criar arquivo de boas-vindas
		welcome_text = f"Bem-vindo ao grupo {group.name}! Aqui você pode compartilhar materiais e colaborar."
		material = Material(
			title="Boas-vindas",
			description=welcome_text,
			file_path=None,
			file_name=None,
			file_type="text/plain",
			file_size=len(welcome_text.encode()),
			uploaded_by=current_user.id,
			group_id=group.id,
			folder_id=folder.id
		)
		_db.session.add(material)
		_db.session.commit()
		flash('Grupo criado com sucesso!', 'success')
		return redirect(url_for('groups_api.groups'))
	return render_template('group_create.html', form=form, active_page='groups')

@groups_api.route('/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
	group = Group.query.get_or_404(group_id)
	if group.created_by != current_user.id:
		flash('Você não tem permissão para editar este grupo.', 'danger')
		return redirect(url_for('groups_api.groups'))
	form = GroupEditForm(obj=group)
	if form.validate_on_submit():
		group.name = form.name.data
		group.subject = form.subject.data
		group.description = form.description.data
		group.goals = form.goals.data
		group.max_members = form.max_members.data or 50
		group.is_active = form.is_active.data
		db.session.commit()
		flash('Grupo atualizado com sucesso!', 'success')
		return redirect(url_for('groups_api.groups'))
	return render_template('group_edit.html', form=form, group=group, active_page='groups')

@groups_api.route('/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
	group = Group.query.get_or_404(group_id)
	if group.created_by != current_user.id:
		flash('Você não tem permissão para excluir este grupo.', 'danger')
		return redirect(url_for('groups_api.groups'))
	db.session.delete(group)
	db.session.commit()
	flash('Grupo excluído com sucesso!', 'success')
	return redirect(url_for('groups_api.groups'))

@groups_api.route('/<int:group_id>')
def group_detail(group_id):
	group = Group.query.get_or_404(group_id)
	is_member = False
	is_admin = False
	if current_user.is_authenticated:
		is_member = group.is_member(current_user)
		is_admin = group.is_admin(current_user)
	return render_template('group_detail.html', group=group, is_member=is_member, is_admin=is_admin, active_page='groups')

@groups_api.route('/<int:group_id>/join', methods=['POST'])
@login_required
def join_group(group_id):
	group = Group.query.get_or_404(group_id)
	if group.is_member(current_user):
		flash('Você já é membro deste grupo.', 'info')
		return redirect(url_for('groups_api.group_detail', group_id=group_id))
	if group.member_count() >= group.max_members:
		flash('O grupo já atingiu o número máximo de membros.', 'warning')
		return redirect(url_for('groups_api.group_detail', group_id=group_id))
	group.add_member(current_user)
	db.session.commit()
	flash('Você entrou no grupo com sucesso!', 'success')
	return redirect(url_for('groups_api.group_detail', group_id=group_id))

@groups_api.route('/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
	group = Group.query.get_or_404(group_id)
	if not group.is_member(current_user):
		flash('Você não é membro deste grupo.', 'info')
		return redirect(url_for('groups_api.group_detail', group_id=group_id))
	if group.is_admin(current_user):
		flash('Admins não podem sair do grupo. Transfira a administração antes de sair.', 'danger')
		return redirect(url_for('groups_api.group_detail', group_id=group_id))
	group.remove_member(current_user)
	db.session.commit()
	flash('Você saiu do grupo.', 'success')
	return redirect(url_for('groups_api.group_detail', group_id=group_id))