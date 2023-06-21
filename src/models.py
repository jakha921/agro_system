from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData, TIMESTAMP, Table, Enum

from src.database import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), unique=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))

    regions = relationship("Region", back_populates="country")

    def __repr__(self):
        return f'<Country {self.name_ru}>'


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))
    country_id = Column(Integer, ForeignKey('countries.id'))

    country = relationship("Country", back_populates="regions")

    cities = relationship("City", back_populates="region")

    def __repr__(self):
        return f'<Region {self.name_ru}>'


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))
    region_id = Column(Integer, ForeignKey('regions.id'))

    region = relationship("Region", back_populates="cities")

    districts = relationship("District", back_populates="city")

    def __repr__(self):
        return f'<City {self.name_ru}>'


class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), unique=True, nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))
    city_id = Column(Integer, ForeignKey('cities.id'))

    city = relationship("City", back_populates="districts")

    department = relationship("Department", back_populates="district")
    users = relationship("User", back_populates="district")

    def __repr__(self):
        return f'<District {self.name_ru}>'


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(String(255))
    district_id = Column(Integer, ForeignKey('districts.id'))

    district = relationship("District", back_populates="department")

    def __repr__(self):
        return f'<Department {self.name_ru}>'


class Gender(Base):
    __tablename__ = 'genders'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))

    users = relationship("User", back_populates="gender")

    def __repr__(self):
        return f'<Gender {self.name_ru}>'


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))

    users = relationship("User", back_populates="status")

    def __repr__(self):
        return f'<Status {self.name_ru}>'


class Device(str, Enum):
    ios = 'ios'
    android = 'android'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    phone_number = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(255), nullable=True)
    gender_id = Column(Integer, ForeignKey('genders.id'))
    status_id = Column(Integer, ForeignKey('statuses.id'))
    district_id = Column(Integer, ForeignKey('districts.id'))
    device_type = Column(Enum('ios', 'android', name="Device"), default='android')
    registration_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    gender = relationship("Gender", back_populates="users")
    status = relationship("Status", back_populates="users")
    district = relationship("District", back_populates="users")

    complain = relationship("Complain", back_populates="users")

    def __repr__(self):
        return f'<User {self.username}>'


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title_ru = Column(String(50), nullable=False)
    title_en = Column(String(50))
    title_uz = Column(String(50))
    short_description_ru = Column(String(255), nullable=False)
    short_description_en = Column(String(255))
    short_description_uz = Column(String(255))

    rights = relationship("Right", back_populates="category")

    def __repr__(self):
        return f'<Category {self.title_ru}>'


class Right(Base):
    __tablename__ = 'rights'

    id = Column(Integer, primary_key=True)
    title_ru = Column(String(50), nullable=False)
    title_en = Column(String(50))
    title_uz = Column(String(50))
    short_description_ru = Column(String(255), nullable=False)
    short_description_en = Column(String(255))
    short_description_uz = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="rights")

    def __repr__(self):
        return f'<Right {self.title_ru}>'


class ComplainStatus(Base):
    __tablename__ = 'complain_statuses'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))

    complain = relationship("Complain", back_populates="complain_status")

    def __repr__(self):
        return f'<ComplainStatus {self.name_ru}>'


class Complain(Base):
    __tablename__ = 'complains'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    complain_status_id = Column(Integer, ForeignKey('complain_statuses.id'))
    title = Column(String(50))
    description = Column(String(255))
    image = Column(String(255))
    rate = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    users = relationship("User", back_populates="complain")
    complain_status = relationship("ComplainStatus", back_populates="complain")

    def __repr__(self):
        return f'<Complain {self.title}>'


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), nullable=False)
    name_en = Column(String(50))
    name_uz = Column(String(50))

    admins = relationship("Admin", back_populates="role")

    def __repr__(self):
        return f'<Role {self.name_ru}>'


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    registration_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="admins")

    def __repr__(self):
        return f'<Admin {self.username}>'
