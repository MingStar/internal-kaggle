from app import app
from app.config.sql_alchemy import db
from app.models import Competition

db.init_app(app)

iris = Competition(
  name = 'Iris Flowers',
  code = 'iris',
  image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTt-bTDxcUL6-tMCxNEd7Xetp9GnmG4MNqNzVPoTLtpt5ItfhcNKA',
  training_data_url='/data/iris.zip',
  description="""<p>The <strong>Iris Flowers </strong>Dataset involves predicting the flower species given measurements of iris flowers.</p>

<p>It is a multi-class classification problem.</p>

<p>The number of observations for each class is balanced. There are 150 observations with 4 input variables and 1 output variable.</p>

<p>The variable names are as follows:</p>

<ul>
	<li>Sepal length in cm.</li>
	<li>Sepal width in cm.</li>
	<li>Petal length in cm.</li>
	<li>Petal width in cm.</li>
</ul>

<p>The baseline performance of predicting the most prevalent class is a classification accuracy of approximately 26%.</p>
"""
)

with app.app_context():
  db.session.add(iris)
  db.session.commit()
