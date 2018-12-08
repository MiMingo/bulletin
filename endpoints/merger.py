from flask import request
from flask_restful import Resource, reqparse
from classes import PollTapeTemplate

# Merges all ballot formats into one json object, for reporting aggregation.
class Merger(Resource):
  def get(self):
    template = PollTapeTemplate()

    precincts = {
      'district1': ['precinct1', 'precinct2', 'precinct3', 'precinct4'],
      'district2': ['precinct1', 'precinct2'],
      'district3': ['precinct1', 'precinct2']
    }
    
    merged = {
      'ballots_cast': 0,
      'races': {}
    }
    for d, ballot in template.districts.items():
      dname = 'district{}'.format(d)
      for race in ballot['races']:
        rname = race['race_name']
        if rname not in merged['races']:
          merged['races'][rname] = {}
        if dname not in merged['races'][rname]:
          merged['races'][rname][dname] = {}
          for pname in precincts[dname]:
            merged['races'][rname][dname][pname] = {}
        for cand in race['candidates']:
          for pname in precincts[dname]:
            merged['races'][rname][dname][pname][cand['name']] = []

    return merged, 200

