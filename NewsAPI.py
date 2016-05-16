from flask import Flask, request
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:123@SQLO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
#-----------------------Models-------------------------------------------------------------
class Base(db.Model):
    __abstract__ = True
    ID = db.Column(db.Integer, primary_key=True)

class News(Base):
    __tablename__ = 'News'

    Title = db.Column(db.String(100))
    Description = db.Column(db.String)
    HeaderImageURL = db.Column(db.String(300))
    Date = db.Column(db.Date)
    AgencyID = db.Column(db.Integer, db.ForeignKey('Agency.ID'))

    def __init__(self, name):
        self.Name = name

    def __repr__(self):
        return '<News %r>' % (self.Name)

class Agency(Base):
    __tablename__ = 'Agency'

    Name = db.Column(db.String(128), nullable=False)
    NewesList = db.relationship('News', backref='Agency',
                                lazy='dynamic')
    def __init__(self, name):
        self.Name = name

    def __repr__(self):
        return '<Agency %r>' % (self.Name)


#-----------------------Services-------------------------------------------------------------
class AgencyGetAll(Resource):
    def get(self):
        result = []
        agencyList = Agency.query.all()
        for agency in agencyList:
            result.append({'name': agency.Name, 'id': agency.ID})
        return result

class NewsGetAll(Resource):
    def get(self):
        result = []
        newsList = News.query.all()
        for news in newsList:
            result.append({'title': news.Title, 'description': news.Description , 'id': news.ID, 'agencyName': news.Agency.Name})
        return result

class NewsGetByAgencyId(Resource):
    def get(self, agencyId):
        result = []
        newsList = News.query.filter_by(AgencyID=agencyId)
        for news in newsList:
            result.append({'title': news.Title, 'id': news.ID, 'agencyName': news.Agency.Name, 'imgUrl': news.HeaderImageURL})
        return result

class NewsGet(Resource):
    def get(self, id):
        news = News.query.filter_by(ID=id).first()
        return {'title': news.Title, 'id': news.ID, 'description': news.Description , 'agencyName': news.Agency.Name, 'imgUrl': news.HeaderImageURL}

class NewsAdd(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        title = json_data['Title']
        agency = json_data['Agency']
        description = json_data['Description']
        author = json_data['Author']
        dateTime = json_data['PublishDate']
        link = json_data['Link']
        news = News('sdsds')
        news.Title = title
        news.AgencyID = 1
        news.Description = description
        db.session.add(news)
        db.session.commit()
        print(dateTime)

api.add_resource(NewsGetAll, '/api/news/getAll')
api.add_resource(NewsGet, '/api/news/get/<string:id>')
api.add_resource(AgencyGetAll, '/api/agency/getAll')
api.add_resource(NewsGetByAgencyId, '/api/news/getByAgencyId/<string:agencyId>')
api.add_resource(NewsAdd, '/api/news/add')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)