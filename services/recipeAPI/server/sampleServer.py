from sanic import Sanic
from sanic.response import html

app = Sanic(__name__)

@app.route('/')
async def testingClick(request):
    return html('<h1>Server is up and running</h1>')
