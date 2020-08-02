# generated with -> flask-sqlacodegen --flask --outfile models.py mysql+pymysql://root:livethere2020@35.225.74.52/livethere

# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, Index, Integer, Numeric, SmallInteger, String
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()


class Rental(db.Model):
    __tablename__ = 'Rental'

    id = db.Column(db.Integer, primary_key=True)
    rentalPrice = db.Column(db.SmallInteger, nullable=False)
    postalCode = db.Column(db.String(6), nullable=False)
    longitude = db.Column(db.Numeric(9, 7), nullable=False)
    latitude = db.Column(db.Numeric(9, 7), nullable=False)
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
    rentToUniversityDistance = db.Column(db.Numeric(3, 1), nullable=False)

    Rental = db.relationship(
        'Rental', primaryjoin='RentalRange.rentalId == Rental.id', backref='rental_ranges')
    University = db.relationship(
        'University', primaryjoin='RentalRange.universityId == University.id', backref='rental_ranges')


class Restaurant(db.Model):
    __tablename__ = 'Restaurant'

    restaurantId = db.Column(db.Integer, primary_key=True)
    restaurantType = db.Column(db.String(1))
    postalCode = db.Column(db.String(6), nullable=False)
    yelpId = db.Column(db.ForeignKey('YelpSchema.yelpId'),
                       nullable=False, index=True)

    YelpSchema = db.relationship(
        'YelpSchema', primaryjoin='Restaurant.yelpId == YelpSchema.yelpId', backref='restaurants')


class RestaurantRange(db.Model):
    __tablename__ = 'RestaurantRange'

    universityId = db.Column(db.ForeignKey(
        'University.id'), primary_key=True, nullable=False)
    restaurantId = db.Column(db.ForeignKey(
        'Restaurant.restaurantId'), primary_key=True, nullable=False, index=True)
    restaurantToUniversityDistance = db.Column(
        db.Numeric(3, 1), nullable=False)

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


class UniversitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'universityName', 'campus', 'city')


class MainCampusMap(University):
    __tablename__ = 'MainCampusMap'

    universityId = db.Column(db.ForeignKey('University.id'), primary_key=True)


class YelpSchema(db.Model):
    __tablename__ = 'YelpSchema'

    yelpId = db.Column(db.Integer, primary_key=True)
    priceLevel = db.Column(db.Integer, nullable=False)
    minPrice = db.Column(db.Float)
    maxPrice = db.Column(db.Float)


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