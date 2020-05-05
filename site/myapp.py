import os
import stockquotes
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "comments.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Comment(db.Model):
	comment = db.Column(db.String(140), unique=True, nullable=False, primary_key=True)
	name = db.Column(db.String(40), unique=True, nullable=False, primary_key=True)
	def __repr__(self):
		return "<Comment: {}>".format(self.comment), "<Name: {}>".format(self.name)

@app.route("/", methods=["GET", "POST"])
def home():
	american = stockquotes.Stock('AAL')
	americanPrice = american.current_price
	if request.form:
		comment = Comment(comment=request.form.get("comment"), name=request.form.get("name"))
		db.session.add(comment)
		db.session.commit()
	comments = Comment.query.all()
	return render_template('home.html', comments=comments, americanPrice=americanPrice)


@app.route("/manage", methods=["GET", "POST"])
def manage():
	if request.form:
		comment = request.form.get("comment")
		comment = Comment.query.filter_by(comment=comment).first()
		db.session.delete(comment)
		db.session.commit()
	comments = Comment.query.all()
	american = stockquotes.Stock('AAL')
	americanPrice = american.current_price
	return render_template('manage.html', comments=comments, americanPrice=americanPrice)

if __name__ == "__main__":
	app.run(debug=True)

