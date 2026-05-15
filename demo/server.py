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

# ==================== 地址数据（添加到现有代码中）====================
# 完整的全国省市区数据（简化版，包含主要城市）
PROVINCES = [
    "北京市", "天津市", "上海市", "重庆市",
    "河北省", "山西省", "内蒙古自治区",
    "辽宁省", "吉林省", "黑龙江省",
    "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省",
    "四川省", "贵州省", "云南省", "西藏自治区",
    "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区",
    "香港特别行政区", "澳门特别行政区", "台湾省"
]

# 城市数据（直辖市的"区"作为城市级）
CITIES = {
    "北京市": ["北京市"],
    "上海市": ["上海市"],
    "天津市": ["和平区", "河东区", "河西区", "南开区", "河北区", "红桥区",
              "东丽区", "西青区", "津南区", "北辰区", "武清区", "宝坻区",
              "滨海新区", "宁河区", "静海区", "蓟州区"],
    "重庆市": ["渝中区", "大渡口区", "江北区", "沙坪坝区", "九龙坡区", "南岸区",
              "北碚区", "渝北区", "巴南区", "涪陵区", "綦江区", "大足区",
              "长寿区", "江津区", "合川区", "永川区"],
    "广东省": ["广州市", "深圳市", "珠海市", "汕头市", "佛山市", "韶关市",
              "湛江市", "肇庆市", "江门市", "茂名市", "惠州市", "梅州市",
              "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市"],
    "浙江省": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市",
              "金华市", "衢州市", "舟山市", "台州市", "丽水市"],
    "江苏省": ["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市",
              "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市"],
    "四川省": ["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市",
              "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市"],
    "湖北省": ["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市",
              "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市"],
    "湖南省": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市",
              "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市"],
    "福建省": ["福州市", "厦门市", "莆田市", "三明市", "泉州市", "漳州市",
              "南平市", "龙岩市", "宁德市"]
}

# 区县数据（部分主要城市）
DISTRICTS = {
    # 广东省
    "广州市": ["天河区", "越秀区", "海珠区", "白云区", "黄埔区", "番禺区",
              "花都区", "南沙区", "增城区", "从化区"],
    "深圳市": ["罗湖区", "福田区", "南山区", "宝安区", "龙岗区", "龙华区",
              "光明区", "坪山区", "大鹏新区", "盐田区"],
    "东莞市": ["莞城街道", "南城街道", "东城街道", "万江街道", "石龙镇", "虎门镇"],
    "佛山市": ["禅城区", "南海区", "顺德区", "三水区", "高明区"],
    # 浙江省
    "杭州市": ["上城区", "拱墅区", "西湖区", "滨江区", "萧山区", "余杭区",
              "富阳区", "临平区", "钱塘区", "临安区"],
    "宁波市": ["海曙区", "江北区", "北仑区", "镇海区", "鄞州区", "奉化区"],
    # 江苏省
    "南京市": ["玄武区", "秦淮区", "鼓楼区", "建邺区", "栖霞区", "雨花台区",
              "江宁区", "浦口区", "六合区", "溧水区"],
    "苏州市": ["姑苏区", "虎丘区", "吴中区", "相城区", "吴江区", "昆山市"],
    # 四川省
    "成都市": ["锦江区", "青羊区", "金牛区", "武侯区", "成华区", "龙泉驿区",
              "青白江区", "新都区", "温江区", "双流区"],
    # 湖北省
    "武汉市": ["江岸区", "江汉区", "硚口区", "汉阳区", "武昌区", "青山区",
              "洪山区", "东西湖区", "蔡甸区", "江夏区"],
    # 湖南省
    "长沙市": ["芙蓉区", "天心区", "岳麓区", "开福区", "雨花区", "望城区"],
    # 福建省
    "厦门市": ["思明区", "海沧区", "湖里区", "集美区", "同安区", "翔安区"],
    "福州市": ["鼓楼区", "台江区", "仓山区", "马尾区", "晋安区", "长乐区"],
    # 北京市
    "北京市": ["东城区", "西城区", "朝阳区", "海淀区", "丰台区", "石景山区", 
              "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区",
              "怀柔区", "平谷区", "密云区", "延庆区"],
    # 上海市
    "上海市": ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区",
              "杨浦区", "闵行区", "宝山区", "嘉定区", "浦东新区", "金山区",
              "松江区", "青浦区", "奉贤区", "崇明区"]
}


# ==================== 地址API（添加到现有代码中）====================
@app.route('/api/address/provinces', methods=['GET'])
def get_provinces():
    return jsonify({"success": True, "data": PROVINCES})

@app.route('/api/address/cities', methods=['GET'])
def get_cities():
    province = request.args.get('province')
    cities = CITIES.get(province, [])
    return jsonify({"success": True, "data": cities})

@app.route('/api/address/districts', methods=['GET'])
def get_districts():
    city = request.args.get('city')
    districts = DISTRICTS.get(city, [])
    return jsonify({"success": True, "data": districts})

# ==================== 活动类型API（添加到现有代码中）====================
@app.route('/api/activity/types', methods=['GET'])
def get_activity_types():
    activity_types = {
        "community": {"name": "社区活动", "sub_types": ["运动会", "知识讲座", "才艺比赛"]},
        "family": {"name": "家庭活动", "sub_types": ["亲子活动", "户外露营", "亲子烘焙"]},
        "other": {"name": "其他", "sub_types": []}
    }
    return jsonify({"success": True, "data": activity_types})


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 活动管理服务器启动")
    print("=" * 50)
    print(f"📍 访问地址: http://localhost:5000")
    print(f"📁 静态文件: demo/activity_management.html")
    print("=" * 50)
    app.run(debug=True, port=5000)