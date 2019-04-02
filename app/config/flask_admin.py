from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Competition

class CompetitionModelView(ModelView):
  column_exclude_list = ['evaluations', 'description']
  column_searchable_list = ['name', 'code']
  form_excluded_columns = ['evaluations', 'created_at', 'updated_at']

def init_app(app, db):
  admin = Admin(app)
  admin.add_view(CompetitionModelView(Competition, db.session))
  return admin
