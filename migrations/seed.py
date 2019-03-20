from app import app
from app.config.sql_alchemy import db
from app.models import Competition

db.init_app(app)

iris = Competition(
  name = 'Iris Flowers',
  code = 'iris',
  image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTt-bTDxcUL6-tMCxNEd7Xetp9GnmG4MNqNzVPoTLtpt5ItfhcNKA',
  training_data_url='/data/iris.csv',
  description="""The Iris Flowers Dataset involves predicting the flower species given measurements of iris flowers.

It is a multi-class classification problem. The number of observations for each class is balanced. There are 150 observations with 4 input variables and 1 output variable. The variable names are as follows:

Sepal length in cm.
Sepal width in cm.
Petal length in cm.
Petal width in cm.
Class (Iris Setosa, Iris Versicolour, Iris Virginica).
The baseline performance of predicting the most prevalent class is a classification accuracy of approximately 26%.
"""
)

with app.app_context():
  db.session.add(iris)
  db.session.commit()
