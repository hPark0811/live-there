""" 
This file will store the reference of common isntances used
throughout the lifecycle of the app.

SQLAlchemy table schema datatypes are created with below commands.
generated with -> flask-sqlacodegen --flask --outfile models.py mysql+pymysql://ID:PW@DB_SERVER_IP_ADDRESS/DB_NAME
"""


# coding: utf-8
from sqlalchemy import types, Column, Date, Float, ForeignKey, Index, Integer, Numeric, SmallInteger, String
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import cast
from flask_caching import Cache


db = SQLAlchemy()
ma = Marshmallow()
cache = Cache()


class CastToFloatType(types.TypeDecorator):
    '''
        Converts stored Decimal values to Floats via CAST 
        operations, because Decimal type number is not handled
        gracefully in python.
    '''
    impl = types.Numeric

    def column_expression(self, col):
        return cast(col, Float)


class Rental(db.Model):
    __tablename__ = 'Rental'

    id = db.Column(db.Integer, primary_key=True)
    rentalPrice = db.Column(db.SmallInteger, nullable=False)
    postalCode = db.Column(db.String(6), nullable=False)
    longitude = db.Column(CastToFloatType, nullable=False)
    latitude = db.Column(CastToFloatType, nullable=False)
    stubId = db.Column(db.Integer, unique=True)
    bathroomCount = db.Column(db.Integer)
    bedroomCount = db.Column(db.Integer)
    lastUpdatedDate = db.Column(db.Date, nullable=False)
    propertyType = db.Column(db.String(255))


class RentalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'rentalPrice', 'postalCode',
                  'longitude', 'latitude', 'stubId', 'bathroomCount',
                  'bedroomCount', 'lastUpdatedDate', 'propertyType')


class RentalRange(db.Model):
    __tablename__ = 'RentalRange'

    universityId = db.Column(db.ForeignKey(
        'University.id'), primary_key=True, nullable=False)
    rentalId = db.Column(db.ForeignKey('Rental.id'),
                         primary_key=True, nullable=False, index=True)
    rentToUniversityDistance = db.Column(CastToFloatType, nullable=False)

    Rental = db.relationship(
        'Rental', primaryjoin='RentalRange.rentalId == Rental.id', backref='rental_ranges')
    University = db.relationship(
        'University', primaryjoin='RentalRange.universityId == University.id', backref='rental_ranges')


class Restaurant(db.Model):
    __tablename__ = 'Restaurant'

    restaurantId = db.Column(db.Integer, primary_key=True)
    restaurantType = db.Column(db.String(1))
    postalCode = db.Column(db.String(6), nullable=True)
    yelpId = db.Column(db.String(55), nullable=False)
    priceLevel = db.Column(db.String(6))
    ratingCount = db.Column(db.Integer)
    longitude = db.Column(CastToFloatType, nullable=False)
    latitude = db.Column(CastToFloatType, nullable=False)


class RestaurantRange(db.Model):
    __tablename__ = 'RestaurantRange'

    universityId = db.Column(db.ForeignKey(
        'University.id'), primary_key=True, nullable=False)
    restaurantId = db.Column(db.ForeignKey(
        'Restaurant.restaurantId'), primary_key=True, nullable=False, index=True)
    restaurantToUniversityDistance = db.Column(
        CastToFloatType, nullable=False)

    Restaurant = db.relationship(
        'Restaurant', primaryjoin='RestaurantRange.restaurantId == Restaurant.restaurantId', backref='restaurant_ranges')
    University = db.relationship(
        'University', primaryjoin='RestaurantRange.universityId == University.id', backref='restaurant_ranges')


class University(db.Model):
    __tablename__ = 'University'
    __table_args__ = (
        db.Index('universityName', 'universityName', 'campus'),
    )

    id = db.Column(db.Integer, primary_key=True)
    universityName = db.Column(db.String(255), nullable=False)
    campus = db.Column(db.String(255), nullable=False)
    institutionType = db.Column(db.String(1), nullable=False)
    postalCode = db.Column(db.String(6), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)


class UniversitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'universityName', 'campus')


class UniversityDetailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'universityName', 'campus', 'institutionType',
                  'city', 'province', 'longitude', 'latitude', 'postalCode')


class MainCampusMap(University):
    __tablename__ = 'MainCampusMap'

    universityId = db.Column(db.ForeignKey('University.id'), primary_key=True)


class AverageUtilityFee(db.Model):
    __tablename__ = 'AverageUtilityFee'
    __table_args__ = (
        db.ForeignKeyConstraint(['universityId'], ['University.id']),
    )

    universityId = db.Column(db.Integer, primary_key=True)
    averageEC = Column(db.Float)
    averageNG = Column(db.Float)
    averageHD = Column(db.Float)


class AverageUtilityFeeSchema(ma.Schema):
    class Meta:
        fields = ('universityId', 'averageEC', 'averageNG', 'averageHD')


class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('restaurantId', 'restaurantType', 'postalCode',
                  'yelpId', 'priceLevel', 'latitude', 'longitude', 'ratingCount')
