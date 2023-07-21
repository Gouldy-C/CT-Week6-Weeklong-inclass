from app import app
from flask import jsonify
from flask_jwt_extended import get_jwt,create_access_token,get_jwt_identity
from datetime import datetime, timezone, timedelta, timestamp

@app.after_request
def refresh_expiring_jwt(response):
    expiration = get_jwt()['exp']
    current  = datetime.now(timezone.utc)
    future_halfhour = timestamp(current + timedelta(minutes=30))
    if future_halfhour > expiration:
        access_token = create_access_token(identity= get_jwt_identity())
        data = response.get_json()
        data['access_token'] = access_token
        response.data = jsonify(data)
        return response