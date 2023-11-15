import os
import vertexai
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import pytz
from model import chatbot

# pylint: disable=C0103
app = Flask(__name__)
def get_user_timezone(offset):
    offset_timedelta = timedelta(minutes=offset)
    utc_time = datetime.utcnow()
    user_local_time = utc_time + offset_timedelta
    user_timezone = pytz.timezone("UTC")
    user_timezone = user_timezone.localize(user_local_time)
    return user_timezone

@app.route('/predict', methods=['POST'])
def predict(chatuser):
  data = request.get_json()
  prompt = data.get('prompt')
  offset = data.get('offset')
  if not prompt:
    return jsonify({"Response": "Halo! Selamat datang di Zein Virtual Asisten. Bagaimana saya bisa membantu Anda hari ini ?"}), 200
  try:
     user_timezone_offset = int(offset)
  except (TypeError, ValueError):
     return jsonify({'error': 'Invalid offset parameter'}), 400

  user_timezone = get_user_timezone(user_timezone_offset)

  prediction = chatbot(prompt)

  return {
        "Prompt": prompt,
        "Response": prediction,
        "UserTimezone": user_timezone.strftime("%Y-%m-%d %H:%M:%S %Z")
    }

