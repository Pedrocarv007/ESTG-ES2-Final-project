from app.forms.material_forms import MaterialUploadForm
from app.models.material import Material
import os
from werkzeug.utils import secure_filename
from flask import abort
"""
Main application routes
"""
from flask import render_template, request, jsonify, redirect, url_for, flash
from app.models.group import Group
from app.forms.group_forms import GroupCreateForm, GroupEditForm
from flask_login import current_user, login_required
from app.config.database import db
from app.main import bp

@bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html', active_page='index')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route com dados dinâmicos."""
    # Grupos do usuário (todos que participa)
    user_groups = current_user.get_groups() if hasattr(current_user, 'get_groups') else []
    group_type = request.args.get('group_type', 'all')
    if group_type == 'manager':
        user_groups = [g for g in user_groups if g.created_by == current_user.id]
    elif group_type == 'participant':
        user_groups = [g for g in user_groups if g.created_by != current_user.id]
    active_groups = [g for g in user_groups if g.is_active]
    user_materials = current_user.uploaded_materials.order_by(Material.created_at.desc()).all() if hasattr(current_user, 'uploaded_materials') else []
    recent_activities = Group.query.filter(Group.created_by == current_user.id).order_by(Group.created_at.desc()).limit(5).all()
    notifications = []
    return render_template(
        'dashboard/dashboard.html',
        active_page='dashboard',
        user_groups=user_groups,
        active_groups=active_groups,
        user_materials=user_materials,
        recent_activities=recent_activities,
        notifications=notifications,
        group_type=group_type
    )

@bp.route('/groups')
def groups():
    """Groups route com busca e filtro."""
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

@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html', active_page='about')


@bp.route('/mimi')
def mimi():
    """Mimi AI chat page route."""
    return render_template('mimi.html', active_page='mimi')


@bp.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupCreateForm()
    if form.validate_on_submit():
        max_members = form.max_members.data if form.max_members.data not in (None, "") else None
        group = Group(
            name=form.name.data,
            subject=form.subject.data,
            description=form.description.data,
            goals=form.goals.data,
            max_members=max_members,
            is_active=form.is_active.data,
            created_by=current_user.id
        )
        db.session.add(group)
        db.session.commit()
        # Adiciona o criador como membro admin
        group.add_member(current_user, role='admin')
        db.session.commit()
        flash('Grupo criado com sucesso!', 'success')
        return redirect(url_for('main.groups'))
    return render_template('group_create.html', form=form, active_page='groups')


@bp.route('/groups/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group.created_by != current_user.id:
        flash('Você não tem permissão para editar este grupo.', 'danger')
        return redirect(url_for('main.groups'))
    form = GroupEditForm(obj=group)
    if form.validate_on_submit():
        max_members = form.max_members.data if form.max_members.data not in (None, "") else None
        group.name = form.name.data
        group.subject = form.subject.data
        group.description = form.description.data
        group.goals = form.goals.data
        group.max_members = max_members
        group.is_active = form.is_active.data
        db.session.commit()
        flash('Grupo atualizado com sucesso!', 'success')
        return redirect(url_for('main.groups'))
    return render_template('group_edit.html', form=form, group=group, active_page='groups')


@bp.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group.created_by != current_user.id:
        flash('Você não tem permissão para excluir este grupo.', 'danger')
        return redirect(url_for('main.groups'))
    db.session.delete(group)
    db.session.commit()
    flash('Grupo excluído com sucesso!', 'success')
    return redirect(url_for('main.groups'))


@bp.route('/groups/<int:group_id>')
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)
    is_member = False
    is_admin = False
    if current_user.is_authenticated:
        is_member = group.is_member(current_user)
        is_admin = group.is_admin(current_user)
    return render_template('group_detail.html', group=group, is_member=is_member, is_admin=is_admin, active_page='groups')



# --- JOIN GROUP ---
@bp.route('/groups/<int:group_id>/join', methods=['POST'])
@login_required
def join_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group.is_member(current_user):
        flash('Você já é membro deste grupo.', 'info')
        return redirect(url_for('main.group_detail', group_id=group_id))
    if group.max_members is not None and group.member_count() >= group.max_members:
        flash('O grupo já atingiu o número máximo de membros.', 'warning')
        return redirect(url_for('main.group_detail', group_id=group_id))
    group.add_member(current_user)
    db.session.commit()
    flash('Você entrou no grupo com sucesso!', 'success')
    return redirect(url_for('main.group_detail', group_id=group_id))

# --- LEAVE GROUP ---
@bp.route('/groups/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    group = Group.query.get_or_404(group_id)
    if not group.is_member(current_user):
        flash('Você não é membro deste grupo.', 'info')
        return redirect(url_for('main.group_detail', group_id=group_id))
    if group.is_admin(current_user):
        flash('Admins não podem sair do grupo. Transfira a administração antes de sair.', 'danger')
        return redirect(url_for('main.group_detail', group_id=group_id))
    group.remove_member(current_user)
    db.session.commit()
    flash('Você saiu do grupo.', 'success')
    return redirect(url_for('main.group_detail', group_id=group_id))



@bp.route('/dashboard/materials/upload', methods=['POST'])
@login_required
def upload_material():
    form = MaterialUploadForm()
    form.group_id.choices = [(g.id, g.name) for g in current_user.groups]
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
    return redirect(url_for('main.dashboard'))