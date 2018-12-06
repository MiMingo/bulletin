class PollTapeTemplate:

  district_1 = {
      "district": 1,
      "precinct": None,
      "date": None,
      "time": None,
      "ballots_cast": None,
      "races": [
        {
          "race_name": "Senate",
          "candidates": [
            {
              "name": "Harry Johnson",
              "votes": None
            },
            {
              "name": "Suzie Doosie",
              "votes": None
            }
          ]
        },
        {
          "race_name": "Governor",
          "candidates": [
            {
              "name": "Alice Muppet",
              "votes": None
            },
            {
              "name": "Bob Builder",
              "votes": None
            }
          ]
        },
        {
          "race_name": "State House",
          "candidates": [
            {
              "name": "Melinda Harrington",
              "votes": None
            },
            {
              "name": "Doyle Yates",
              "votes": None
            }
          ]
        },
      ]
    }

  district_2 = {
    "district": 2,
    "precinct": None,
    "date": None,
    "time": None,
    "ballots_cast": None,
    "races": [
      {
        "race_name": "Senate",
        "candidates": [
          {
            "name": "Harry Johnson",
            "votes": None
          },
          {
            "name": "Suzie Doosie",
            "votes": None
          }
        ]
      },
      {
        "race_name": "Governor",
        "candidates": [
          {
            "name": "Alice Muppet",
            "votes": None
          },
          {
            "name": "Bob Builder",
            "votes": None
          }
        ]
      },
      {
        "race_name": "State House",
        "candidates": [
          {
            "name": "Robert Paulson",
            "votes": None
          },
          {
            "name": "Tyler Durden",
            "votes": None
          }
        ]
      },
    ]
  }

  district_3 = {
    "district": 3,
    "precinct": None,
    "date": None,
    "time": None,
    "ballots_cast": None,
    "races": [
      {
        "race_name": "Senate",
        "candidates": [
          {
            "name": "Harry Johnson",
            "votes": None
          },
          {
            "name": "Suzie Doosie",
            "votes": None
          }
        ]
      },
      {
        "race_name": "Governor",
        "candidates": [
          {
            "name": "Alice Muppet",
            "votes": None
          },
          {
            "name": "Bob Builder",
            "votes": None
          }
        ]
      },
      {
        "race_name": "State House",
        "candidates": [
          {
            "name": "Brennan Huff",
            "votes": None
          },
          {
            "name": "Dale Doback",
            "votes": None
          }
        ]
      },
    ]
  }

  def __init__(self):
    self.districts = {
      "1": type(self).district_1,
      "2": type(self).district_2,
      "3": type(self).district_3
    }

  @staticmethod
  def get_poll_tape_template():
    poll_tape = {
      "district": None,
      "precinct": None,
      "date": None,
      "time": None,
      "ballots_cast": None,
      "races": []
    }
    return poll_tape

  @staticmethod
  def get_race_template():
    race = {
        "race_name": None,
        "candidates": []
    }
    return race

  @staticmethod
  def get_candidate_template():
    candidate = {
        "name": None,
        "votes": None
    }
    return candidate

  def get_template(self, district):
    if district in self.districts:
      return self.districts[district]
    return None