ketocalc - web app for ketogenic diet calculation and management

##How to run project

- Clone repository

- create local `.env` file
  - use `env.example` for example

- Prepare enviroment with `pipenv`
  - `pipenv install`

- Prepare and update database
  - create scheme in db
  - `pipenv run flask db upgrade`

- Run application on localhost
  
  ```bash
  export FLASK_ENV="development";
  export APP_STATE="development";
  pipenv run flask run;

  ```
  - see Flask documentation for more information


Formatted with:
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Checked for vulnerabilities with:
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

