#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/research', methods=['GET'])
def get_researchs():
    researchs = Research.query.all()
    return make_response([research.to_dict() for research in researchs], 200)

@app.route('/research/<int:id>', methods=['GET', 'DELETE'])
def research_by_id(id):
    research = Research.query.filter_by(id=id).first()
    if not research:
        return make_response({"error": "Research paper not found"}, 404)
    elif request.method == 'GET':
        return make_response(research.to_dict(), 200)
    elif request.method == 'DELETE':
        if research:
            all_research_authors = ResearchAuthors.query.filter(ResearchAuthors.research_id == id).all()
            db.session.delete(research)
            for res in all_research_authors:
                db.session.delete(res)
            db.session.commit()
            return make_response({}, 200)

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return make_response([author.to_dict() for author in authors], 200)

@app.route('/research_author', methods=['POST'])
def new_author():
    try:
        new_researchauthor = ResearchAuthors(
            research_id = request.get_json()['research_id'],
            author_id = request.get_json()['author_id']
        )
        db.session.add(new_researchauthor)
        db.session.commit()
        return make_response(new_researchauthor.authors.to_dict(), 201)
    except:
        return make_response({
            "errors": ["validation errors"]
        }, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
