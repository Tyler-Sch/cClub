from tests.fixture_base import app, db, session
from flask import url_for
from user_server.api.models import User
import json
from tests.testshortcuts import  add_user_via_endpoint, login_user_via_endpoint

def test_login_required_wrapper_not_authorized(session, client):
    response = client.post(
        url_for('users.get_recipe_lists'),
        data=json.dumps({}),
        content_type='application/json',
    )
    data = response.get_json()
    assert 'unauthorized' in data.get('status')
    assert response.status_code == 401

def test_login_required_bad_signature(client):
    pass
