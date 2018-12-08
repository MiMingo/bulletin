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
              "name": "Hank Johnson",
              "votes": None
            },
            {
              "name": "Joe Profit",
              "votes": None
            }
          ]
        },
        {
          "race_name": "Governor",
          "candidates": [
            {
              "name": "Brian Kemp",
              "votes": None
            },
            {
              "name": "Stacey Abrams",
              "votes": None
            },
            {
              "name": "Ted Metz",
              "votes": None
            }
          ]
        },
        {
          "race_name": "House",
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
            "name": "Lucy McBath",
            "votes": None
          },
          {
            "name": "Karen Handel",
            "votes": None
          }
        ]
      },
      {
        "race_name": "Governor",
        "candidates": [
          {
            "name": "Brian Kemp",
            "votes": None
          },
          {
            "name": "Stacey Abrams",
            "votes": None
          },
          {
            "name": "Ted Metz",
            "votes": None
          }
        ]
      },
      {
        "race_name": "House",
        "candidates": [
          {
            "name": "Sanford Bishop",
            "votes": None
          },
          {
            "name": "Herman West",
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
            "name": "Rob Woodall",
            "votes": None
          },
          {
            "name": "Carolyn Bourdeaux",
            "votes": None
          }
        ]
      },
      {
        "race_name": "Governor",
        "candidates": [
          {
            "name": "Brian Kemp",
            "votes": None
          },
          {
            "name": "Stacey Abrams",
            "votes": None
          },
          {
            "name": "Ted Metz",
            "votes": None
          }
        ]
      },
      {
        "race_name": "House",
        "candidates": [
          {
            "name": "Drew Ferguson",
            "votes": None
          },
          {
            "name": "Chuck Enderlin",
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
