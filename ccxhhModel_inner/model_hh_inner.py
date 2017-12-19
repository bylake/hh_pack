# coding: utf-8
import flask
from flask import request
from flask import jsonify
import json
from ccxhhModel_inner.score_main import score_main

server = flask.Flask(__name__)


@server.route('/HhModelApiInner', methods=['post'])
def HhModelApiInner():
    try:
        json_data = json.loads(request.data.decode())
        base_hh, score, score_amt, final_amt, flag_sal = score_main(json_data)
        return jsonify({'apply_score': score, 'amt_score': score_amt, 'base_score': base_hh, 'credit_amount': final_amt,
                        'flag_sal': flag_sal})

    except Exception as e:

        return jsonify({"code": 500, "msg": "计算失败", "error_msg": str(e)})


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=1027)  # processes 为可支持并发量
