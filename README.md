As part of the interview process, I was tasked with creating a schedulable client to collect data from [Game of Thrones API](https://anapioficeandfire.com/)  and store it using Python and any other open source software. Solution has to satisfy the following critera:

```
1. Create data model for storing books, characters and houses entities (provide
DDL and/or Data Diagram).
2. Data model should satisfy against queries:
   - Be able to extract the total count of each entity from DB (provide example query).
   - Be able to extract a list of all book names, authors, release dates and character names, genders and titles mentioned in the book in the best manner for human-readable format. (provide example query).
   - Be able to extract a list of all character names and played by actor names. (provide example query).
   - Be able to extract a list of all house names, regions, overlord names and sworn member names (provide example query).
3. Develop a data extraction client (fulfilling requirements in section 2). Extraction should reflect up-to-date data.
4. Process should be able run on demand or be scheduled.
5. Document the solution and put it on gitHub providing the project's URL.
```

### Solution:
Solution proposed here consists of the following:
- Python powered back-end using [Streamlit](https://streamlit.io/) library;
- [SQLite](https://www.sqlite.org/index.html) powered DB framework using Python API;
- Python [Pandas](https://pandas.pydata.org/) library for data processing;
- Python [Requests](https://docs.python-requests.org/en/latest/) library for HTTP requests;
- [App Engine](https://cloud.google.com/appengine) in Google Cloud Platform for hosting;
- [GitHub action](https://github.com/augustinasn/surfshark-data-engineer-task/blob/main/.github/workflows/deploy-to-cloud.yaml) for automated deployment.

Source code can be found [here](https://github.com/augustinasn/soiaf-data-client), whereas the deployed App can be reached using the following URL - https://surfshark-data-engineer-task.ey.r.appspot.com/


### Usage:
Navigate this application using the select box in the left side menu. Each menu option represents the following:
- **Intro** - general information about the App, it's usage, etc.
- **Model** - explains data acquisition process and shows in what way is data structured after extracting it in the SQLite DB;
- **Init/remove** - enables user to manually trigger extraction of up-to-date data from GoT API and initialization of a new DB using that data. Also allows user to remove existing DBs;
- **Queries** - involves trigger for various queries and data transformations defined in the criteria part;
- **Init scheduler** - involves interface for setting up a scheduled data extraction and DB initialization job.

### Places to improve:
Granted if I had unlimited time resources I'd also add the following functionalities:
- Define GCP configurationg using Terradata (as opposed to using the Console). This way I'd enable an easy and efficient TEST/PROD environment switching, faster configuration and an ability to more easily migrate to another cloud provider if need be;
- Set up a more sophisticated DB solution, ideally on GCP as a separate resource. This would allow more complex SQL queries and wouldn't require additional processing with Python thus saving time and compute; 
- Set up a storage resource in GCP. App currently saves data locally, which means that it gets destroyed when redeployng the app;
- Authentication, preferably a Google login;
- More sophisticated data model. Could have created more than three tables that would've made some queries much easier to write; 
