from flask import request
from flask_restful import Resource, reqparse
from classes import PollTapeTemplate

# Merges all ballot formats into one json object, for reporting aggregation.
class Merger(Resource):
  def get(self):
    template = PollTapeTemplate()
    
    merged = {
      'ballots_cast': 0,
      'races': {}
    }
    for d, ballot in template.districts.items():
      dname = 'district{}'.format(d)
      for race in ballot['races']:
        name = race['race_name']
        if name not in merged['races']:
          merged['races'][name] = {}
        if dname not in merged['races'][name]:
          merged['races'][name][dname] = {}
        for cand in race['candidates']:
          merged['races'][name][dname][cand['name']] = 0

    return merged, 200

