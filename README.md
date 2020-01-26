# aktia-dev-challenge-enron

Aktia summerjob 2020 data task

Running the program:

- Step 1

  - Install pipenv with homebrew: ```$ brew install pipenv```
  (Other options listed in this link <https://github.com/pypa/pipenv>)

  - Add 'maildir' folder to the root folder.
  Link for download: <https://www.cs.cmu.edu/~./enron/>

  - Install all dependencies for a project (including dev): ```$ pipenv install --dev```

- Step 2

  - Activate virtualenv by running pipenv shell: ```$ pipenv shell```

  - Run the 'main.py' program: ```$ python main.py```

  The main.py program produces two csv files. File 'emails_sent_totals.csv' contains data of all send emails per employee sent to all his or her recipients.
  
  File 'emails_sent_average_per_weekday.csv' contains data of average number of recieved emails per employee per day of week.
  