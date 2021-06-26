import pyrebase
import os

ConfigVars = {
    'apiKey': os.getenv('apiKey'),
    'authDomain': os.getenv('authDomain'),
    'projectId': os.getenv('projectId'),
    'storageBucket': os.getenv('storageBucket'),
    'serviceAccount': {
        "type": os.getenv('type'),
        "project_id": os.getenv('projectId'),
        "private_key_id": os.getenv('private_key_id'),
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrW1TNIURoyjiY\ngc3wnLztgbV7zBLBuSIX12Gz3xDinzCTyA6MkXoZ/TY9fwqEb8c5hUmvI9tED9x6\no6wVdG+KcyRYeQdqjpg1oiQowaf/zbxBc8QPNooCIb1tfYuEGPhiLVHyb5LO0Qdk\n/nYrr6CFEsBP5VZwp65zE78FWMhfywiroxBsV9Qujz5iqyP7NmPEPizbDPoft6rQ\npr/6IHVQni1XILKAqPsumJbtK7PpQtUEDvA9SzFhIUuhDdVBzyMly9zqx3wc1ejJ\nvZzNIeTpriO5HqoU5fyjjNs+q74HroKUXlq2v59EkZ6yKrrF8OKlga9TsIE9cLRQ\nMfUbD3YBAgMBAAECggEAB69K+f+xCZs9qlOlijhlREHqAyxiqcILoUXjl+vIxJKl\nQynLwtcVXD83iwHjCI+nJh4jPbg3pNfdqFK/X9KLqNbDSjdA5pddhFSj4+YHcQvn\neO7GdXSZmad5gmsI2KEMDQJOTgQqvjawN7T67lIFupVEMnETc6FTGM5JmOV9Gvqb\nl/Fyszufveo7Boi/H8LpopQ7iWps9RIu+aR04GsdEfX/JLNDKT+61hHUvzbYKdab\nwKHm2ebqGM7sQzBVLudph+YyhvqVg8pUgOcWh2j0SWRtZSOSakbcvzTG8yJ7PWKW\nulbBmSDM4OgIAVHEV/Ef09uqLRKCyvFC9b2nZWUsvwKBgQDtHV1KO0BGpHU3X68z\nEPf26UAmA6uewydpk7hzhVvvs2seXqG8XY7XXoUlnqLW6rW9uXMoN8ft+7jGEJiN\nXzrX7GslYufenecfMiLZ9sv+Ggtk0x6AAijT+WJj5gxNL4dAC3KW84khyh+iikgP\nBbSeECCq6Y7eDp4lOCX8O2xwswKBgQC5ATMI7jsVcwE3pLvqmXZ1OgOeBOlZzYEj\ngg1FMaya18lr4dKrXAhNhFyJZ2Bw/6siEjArOtSf9zJxZjbdxlvZWvhrViD8RfA3\namZMDp87jojr1A1JLEL4hsZCgCxCj8CKPADFNbU45N1w625DUvygIPN5tf94drPf\ndld1tj1wewKBgQDKPZOGbwchub/onQo4Ci8VQFlgkxzcayPAnyhiD8scpfGlk51r\npnjhJVN3hNjraoHc8sJP+VPjniI5fYpAeoscBCBXYQbYD+JD72Ved2wCrYAuXQvU\nrwLX2gubnWm8o98+NwVjzxCV62oUHtHbTkiB0MusO02KBPnKURvFCYIylQKBgBOD\nxd9eScs0a190OAJCF9W7vd/wQrEfVUzqjf3LhJp8wplno7JBrfqHSL+RsQGaZnHc\nm0okFYOeLqr5jjYMk2m1B9lCp44Uzob56TqCnFdK7LR7lL8wNQxEIyumm4SV50ht\nleM3jBspQRaFLwdY/J7jeutOwFjzpHug3w7in057AoGAZhmOuO34tzQMXHGz5g6K\n6d7PDMIgNRGZwevzdn/+jtx0cRnC+0Gemx6jHYhfw1erC9FT/fwK5vmdyDJs5YNn\nplCayanp1vfNUnZMqIL9G9r4XnyG/K3fxYl+kTXrpA84xXYfbciHudz2EV9TiMwU\n20CXJjX0kf3LYKl56rnIl0A=\n-----END PRIVATE KEY-----\n",
        "client_email": os.getenv('client_email'),
        "client_id": os.getenv('client_id'),
        "auth_uri": os.getenv('auth_uri'),
        "token_uri": os.getenv('token_uri'),
        "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
        "client_x509_cert_url": os.getenv('client_x509_cert_url')
    },
    'messagingSenderId': os.getenv('messagingSenderId'),
    'appId': os.getenv('appId'),
    'measurementId': os.getenv('measurementId'),
    'databaseURL': os.getenv('databaseURL')
}



firebase = pyrebase.initialize_app(ConfigVars)