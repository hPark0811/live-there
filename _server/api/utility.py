from models import *
from flask import Blueprint, request

utility_api = Blueprint('utility_api', __name__)

utility_schema = AverageUtilityFeeSchema()
utilities_schema = AverageUtilityFeeSchema(many=True)


@utility_api.route('', methods=['GET'])
def get_avg_utility_fee():
    id = request.args['universityId']
    avg_fee = AverageUtilityFee.query.get(int(id))
    return utility_schema.jsonify(avg_fee)

