from models import *
from util import make_cache_key
from flask import Blueprint, jsonify

university_api = Blueprint('university_api', __name__)

# Init Schema
university_schema = UniversityDetailSchema()
universities_schema = UniversitySchema(many=True)

# Cache TODO: Improve cache method
universities_cache = None


@university_api.route('', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def get_universities():
    # Update cache
    global universities_cache
    if universities_cache == None:
        universities_cache = University.query.all()

    return universities_schema.jsonify(universities_cache)


@university_api.route('<id>', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def get_university(id):
    university_detail = University.query.get(id)

    return university_schema.jsonify(university_detail)
