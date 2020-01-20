# coding: utf-8

import math

import types

import bcrypt
import hashlib

import unidecode

from flask import current_app as application

from app import db
from app.auth import login

from sqlalchemy.exc import DatabaseError
