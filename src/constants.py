import os

# API:
SOIAF_ENDPOINT = "https://anapioficeandfire.com/api"
SOIAF_PAGE_SIZE = 10

# DB:
DB_FILEPATH = os.path.join("src", "data", "db.sqlite")

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