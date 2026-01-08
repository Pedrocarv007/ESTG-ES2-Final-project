from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.group import Group
from app.models.material import Material

bp_dashboard = Blueprint('dashboard_api', __name__, url_prefix='/dashboard')

@bp_dashboard.route('/')
@login_required
def dashboard():
    user_groups = current_user.get_groups() if hasattr(current_user, 'get_groups') else []
    active_groups = [g for g in user_groups if g.is_active]
    user_materials = current_user.uploaded_materials.order_by(Material.created_at.desc()).all() if hasattr(current_user, 'uploaded_materials') else []
    recent_activities = Group.query.filter(Group.created_by == current_user.id).order_by(Group.created_at.desc()).limit(5).all()
    notifications = []
    print("Rendering dashboard for user:", current_user.id)
    print("User groups:", user_groups)
    return render_template(
        'dashboard/dashboard.html',
        active_page='dashboard',
        user_groups=user_groups,
        active_groups=active_groups,
        user_materials=user_materials,
        recent_activities=recent_activities,
        notifications=notifications
    )

@bp_dashboard.route('/materials/upload', methods=['POST'])
@login_required
def upload_material():
    from app.forms.material_forms import MaterialUploadForm
    import os
    from werkzeug.utils import secure_filename
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
        from app.config.database import db
        db.session.add(material)
        db.session.commit()
        flash('Arquivo enviado com sucesso!', 'success')
    else:
        flash('Erro ao enviar arquivo.', 'danger')
    return redirect(url_for('dashboard_api.dashboard'))
