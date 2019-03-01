import os

import firebase_admin
from firebase_admin import credentials

from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    name = 'api'

    path = "secutopia/secupia-firebase-adminsdk.json"
    creds = credentials.Certificate(os.path.join(
                                        settings.BASE_DIR,
                                        path
                                        )
                                    )
    app = firebase_admin.initialize_app(creds)
