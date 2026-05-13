#!/usr/bin/env python
"""活动管理 API 服务器"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# 模拟数据库
activities = []
activity_id = 1

@app.route('/')
def index():
    return render_template('activity_management.html')

@app.route('/api/activities', methods=['GET'])
def get_activities():
    return jsonify(activities)

@app.route('/api/activities', methods=['POST'])
def create_activity():
    global activity_id
    data = request.json
    data['id'] = activity_id
    data['createTime'] = datetime.now().isoformat()
    data['status'] = '待提交'
    activities.append(data)
    activity_id += 1
    return jsonify({'success': True, 'id': data['id']})

@app.route('/api/activities/<int:aid>', methods=['PUT'])
def update_activity(aid):
    for activity in activities:
        if activity['id'] == aid:
            activity.update(request.json)
            return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/activities/<int:aid>', methods=['DELETE'])
def delete_activity(aid):
    global activities
    activities = [a for a in activities if a['id'] != aid]
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 活动管理服务器启动")
    print("=" * 50)
    print(f"📍 访问地址: http://localhost:5000")
    print(f"📁 静态文件: demo/activity_management.html")
    print("=" * 50)
    app.run(debug=True, port=5000)