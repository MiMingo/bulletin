from flask_restful import Resource

class Hello(Resource):
  def get(self, **kwargs):
    return {'hello': True}