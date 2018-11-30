class PollTapeTemplate:

  @staticmethod
  def get_poll_tape_template():
    poll_tape = {
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

  @staticmethod
  def get_template():
    template = {
      "precinct": None,
      "date": None,
      "time": None,
      "ballots_cast": None,
      "races": [
        {
          "race_name": "Senate",
          "candidates": [
            {
              "name": "Harry",
              "votes": None
            },
            {
              "name": "Suzie",
              "votes": None
            }
          ]
        },
        {
          "race_name": "Governor",
          "candidates": [
            {
              "name": "Alice",
              "votes": None
            },
            {
              "name": "Bob",
              "votes": None
            }
          ]
        }
      ]
    }

    return template