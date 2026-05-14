"""
Global Configuration for Application
"""

import os

DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "sqlite:///test.db"
)

SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "s3cr3t-key-shhhh"
)
