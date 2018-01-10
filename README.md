# Semantic-Engine based on Document Embedding

## Dependencies and Setup
To use the semantic engine application, you will need:
* Python 2.7
* A recent version of [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/)
* [NLTK 3](http://www.nltk.org/)
* [Flask](http://flask.pocoo.org/)
* [gensim](https://radimrehurek.com/gensim/) (for vocabulary expansion when training new models)

## How to run the app

  In the project directory run the following commands:
  
  *

  ```
  $ sh getPrepared.sh
  ```
  This will download all the models files required (WARNING: the files are about 5 GB each)
  
  * 
  
  ```
  $ python flaskr.py
  ```
  
  This will run the app on: http://127.0.0.1:5000/engine
