# legal-search
*Flask API to search brazilian legal process*

### API Documentation
You need to know how to test this API? Access the API Documentation, with examples and importants informations [here](https://documenter.getpostman.com/view/12464969/TVCiUmZZ?version=latest)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.getpostman.com/collections/e26737ef0ba95a0042ff)

### Run this project
*This project was developed in an environment with Ubuntu 18.04 and Python 3.6.9. But, you can run in any system with Python 3.6.9+*

Before run export FLASK_APP enviroment var:
```
export FLASK_APP=api
```


Inside the project's root folder, run:
```commandline
flask run
```

### Running tests
If you want just to execute the tests, run:
```commandline
python -m unittest -v
```

If you want to see the test coverage level, run:
```
coverage run --source=api,crawlers -m unittest discover -s tests/ -v

coverage report
# or
coverage html
```