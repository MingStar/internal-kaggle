from flask_admin import Admin
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from app.models import Competition, Evaluation
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from app.env import SITE_NAME

class CKTextAreaWidget(TextArea):
  def __call__(self, field, **kwargs):
    if kwargs.get('class'):
      kwargs['class'] += ' ckeditor'
    else:
      kwargs.setdefault('class', 'ckeditor')
    return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
  widget = CKTextAreaWidget()

class EvaluationModelView(ModelView):
  can_create = False
  can_edit = False
  can_delete = False
  column_exclude_list = ['competition', 'task_id']
  column_searchable_list = ['team_name', 'docker_image_name']

class CompetitionModelView(ModelView):
  form_base_class = SecureForm
  extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
  column_exclude_list = ['evaluations', 'description']
  column_searchable_list = ['name', 'code']
  form_excluded_columns = ['evaluations', 'created_at', 'updated_at']
  column_editable_list = ['is_active', 'training_data_url', 'code', 'name']
  form_overrides = {
    'description': CKTextAreaField
  }

  def __init__(self, model, session, *args, **kwargs):
    super(CompetitionModelView, self).__init__(model, session, *args, **kwargs)
    self.static_folder = 'static'
    self.endpoint = 'admin'
    self.name = 'Competition'


def init_app(app, db):
  c = CompetitionModelView(Competition, db.session, url='/admin')
  admin = Admin(app, name=f"{SITE_NAME} Admin", index_view=c)
  admin.add_view(EvaluationModelView(Evaluation, db.session))
  return admin
