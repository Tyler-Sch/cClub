# Ingredient Part of Speech Tagger

Recurrent neural network (dual layer bidirectional GRU) created with keras running behind a web server for tagging individual words in list of recipes. Uses tensorflow backend and fastText pretrained word embeddings.

## requirements

```
  NVIDIA GPU with CUDA, CUDA toolkit, and cuDNN SDK installed
  [instructions](https://www.tensorflow.org/install/gpu)

  python virutalenv
  ```

## installation

  create a virtual environment and download requirements
  ```
  virtualenv env -p python3.6
  source env/bin/activate
  pip install -r requirements.txt
  ```

  start up the server:

  ```
  python ingredientPOStagger.py
  ```

## Use:

#### to use, send a post request to the server (most likely localhost:5001) with form data in the form of
  ```
    {'ingredients': ['1/2 cup of sugar', '5 pounds of beef brisket']}
  ```

  example:
    From python shell with requests library
  ```
    >>> import requests
    >>> request_data = {'ingredients': [
      '1 pound rigatoni',
      '3 chicken thighs',
      '2 chicken wings',
      '2 quarts of vegetable stock'
    ]}
    >>> response = requests.post('http://localhost:5001/ingredients', data=request_data)
  ```

#### The server returns a list of words with their tags.

  example:
  ```
    >>> response.json()
    {'ingredients': [[['1', 'QTY'], ['pound', 'UN'], ['rigatoni', 'IN']], [['3', 'QTY'], ['chicken', 'IN'], ['thighs', 'IN']], [['2', 'QTY'], ['chicken', 'IN'], ['wings', 'IN']], [['2', 'QTY'], ['quarts', 'UN'], ['of', 'C'], ['vegetable', 'IN'], ['stock', 'IN']]]}
  ```

## Tags:

  ```
  QTY: quantity
  UN: unit of measurement
  IN: ingredient
  C: comment
  RE: range end
  ```

## acknowledgment:

  This model was trained on modified data the new times posted in a [tech blog](https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/).
