import os

# General:
PAGE_TITLE = "Surfshark data engineer task"

# API:
SOIAF_ENDPOINT = "https://anapioficeandfire.com/api"
SOIAF_PAGE_SIZE = 10

# DB:
DB_FOLDERPATH = os.path.join("src", "data")

BOOKS_SCHEMA = {"url": "text",
                "name": "text",
                "isbn": "text",
                "authors": "text",
                "numberOfPages": "integer",
                "publiser": "text",
                "country": "text",
                "mediaType": "text",
                "released": "text",
                "characters": "text",
                "povCharacters": "text"}

CHARACTERS_SCHEMA = {"url": "text",
                     "name": "text",
                     "gender": "text",
                     "culture": "text",
                     "born": "integer",
                     "died": "text",
                     "titles": "text",
                     "aliases": "text",
                     "father": "text",
                     "mother": "text",
                     "spouse": "text",
                     "allegiances": "text",
                     "books": "text",
                     "povBooks": "text",
                     "tvSeries": "text",
                     "playedBy": "text"}

HOUSES_SCHEMA = {"url": "text",
                 "name": "text",
                 "region": "text",
                 "coatOfArms": "text",
                 "words": "integer",
                 "titles": "text",
                 "seats": "text",
                 "currentLord": "text",
                 "heir": "text",
                 "overlord": "text",
                 "founded": "text",
                 "founder": "text",
                 "diedOut": "text",
                 "ancestralWeapons": "text",
                 "cadetBranches": "text",
                 "swornMembers": "text"}

DB_SCHEMAS = {"books": BOOKS_SCHEMA,
              "characters": CHARACTERS_SCHEMA,
              "houses": HOUSES_SCHEMA}

# Scheduler:
SCHEDULER_OPTIONS = {"2 minutes": 2 * 60,
                     "30 minutes": 30 * 60,
                     "4 hours": 4 * 60 * 60,
                     "12 hours": 12 * 60 * 60,
                     "1 day": 24 * 60 * 60,
                     "1 week": 7 * 24 * 60 * 60}

if os.environ.get("COMPUTERNAME", False):
    SCHEDULER_FILEPATH = os.path.join("app", "src", "scheduler.py")
else:
    SCHEDULER_FILEPATH = os.path.join(".", "src", "scheduler.py")

# UI assets:
MODEL_FILEPATH = os.path.join("src", "ui", "assets", "model.png")