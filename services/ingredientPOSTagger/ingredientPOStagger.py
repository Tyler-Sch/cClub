import numpy as np
import json
from tagdata import tokenize
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from sanic import Sanic
from sanic.response import json as json_response
import asyncio
import uvloop

"""
    Sanic server with one end point ('/ingredients') which takes a list
    of ingredients, written in english, and uses an RNN to label the parts of
    speech. Have not run without gpu support
"""


app = Sanic()
model_main = load_model(
    'winningModelSoFar/doubleLayerGRUMoreData/'
    'doubleLayerGRUTrainable2McommonMostData.hdf5'
)
model_main._make_predict_function()
with open('winningModelSoFar/doubleLayerGRUMoreData/word2index.json', 'r') as f:
    word2index = json.loads(f.read())
with open('winningModelSoFar/doubleLayerGRUMoreData/tag2index.json', 'r') as f:
    tag2index = json.loads(f.read())


@app.route('/ingredients', methods=["POST"])
async def processIngredients(request):
    """
        takes {'ingredients': [list of ingredients]} and returns a list
        for each word in the ingredient with a ingredients specific
        part of speech tag.
            'IN' = ingredient
            'QTY' = quantity
            'RE' = range end (for recipes with variable quantity range)
            'UN' = unit of measurement
            'C' = everything else (comment)
    """

    ingredients_list = request.form['ingredients']

    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(
        None,
        tag_ingredients,
        ingredients_list,
        model_main,
        word2index,
        tag2index
    )


    return json_response({'ingredients': results})

def process_sentence(s, wordDict):
    """
        turn string into vector of indexes for embedding layer of rnn
    """
    tokens = tokenize(s)
    if len(s) > 57:
        s = s[:57]
    new_sent_nums = []
    for i in tokens:
        try:
            word_num = wordDict[i]
        except KeyError:
            word_num = len(wordDict) - 1
        new_sent_nums.append(word_num)
    return np.array(new_sent_nums)

def tag_ingredients(ingredientList, model, word2index, tag2index, maxlen=57):
    #print(ingredientList)
    """
        preprocesses text, make POS predictions, returns POS tagged
        list of texts
    """
    ingredient_vecs = [process_sentence(s, word2index) for s in ingredientList]
    padded_vecs = pad_sequences(ingredient_vecs, maxlen=maxlen, padding='post')
    # print(padded_vecs)
    predictions = model.predict(padded_vecs)
    index2tag = {v:k for k,v in tag2index.items()}
    predic_matrix = np.argmax(predictions, axis=2)
    preds = []
    for row in predic_matrix:
        preds.append([index2tag[i] for i in row])
    results = []
    for idx in range(len(ingredientList)):
        result = []
        tok = [i for i in tokenize(ingredientList[idx])]
        for i in range(len(tok)):
            result.append((tok[i], preds[idx][i]))

        results.append(result)
    return results



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
