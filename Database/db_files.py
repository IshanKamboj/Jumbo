import pyrebase
import os

ConfigVars = {
    'apiKey':os.getenv('apiKey'),
    'authDomain':os.getenv('authDomain'),
    'projectId': os.getenv('projectId'),
    'storageBucket':os.getenv('storageBucket'),
    'serviceAccount':{
        "type": "service_account",
        "project_id": "jumbo-17e7f",
        "private_key_id": "4fdb577b02e920a908d89ec14be53789fe19cfad",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDj7yF4UGIKy98P\no/M+OjZec5Gjp2bwxIbLh0oLaR1gED4y8tw4458U65dgtoDY3JRJbHJjwZB5udmJ\nR1aS7O1KoFUQrcs7oGEqrmRM5ar+/HXwfdUhf/a5UzQ81gvaCkFcRHmDNEB1O4oJ\n/DMEWh8kyTn80svyU/iKIuOUS9SBtkaeaG2yT3Yuhg90OLhL4EeCdBZqdwbaS4ir\n+UGIceU6c8mOAzPTOzwawd0okpOGgBbDqd9pGST22BHCR6YugzUEgkb4EAmS3sgg\nxiox9ic6UZOy7TjjYEzyTm7tULs0cUXEki6YCvYt7m8tB0w5sPcagil/hySbQB3d\nZX3gq6+zAgMBAAECggEAA2CIo2q1eSl6HZY1RWfBZHbb4ovZZ5nR0XQosbCWAdVb\nxo94mdMtiTbQYFtz30KtY8UakMXOaS9KvND0xGqEPYXQnNWmXDTNG7/Htqf0d6Cv\n8qc6oCtwMWC9NmWJeWqLe118W2hLyDDgo7M74kWfjoD4vfk1klqSJSHNM2ZIOL++\ndWezbkwsvnGfj7JQIQZo8cjokMCTsOHluDgcWGz+1J0yJ9dnfy+SSik3LJtVdqpY\nJSk1AvZwsnV6jojPpaSdaQwZCtiQL6Qqko8NuTuVwjE2A0Pq+jovj6b1Ovl42gBX\nwxTdgfM6B6p1VtjgajEVlapcc8pS3V4YaWZjHnDeiQKBgQD1kcVtocSYqbJVLqHz\n41Rh6DT0EEDp4K1NCPzq+TPLym2ltPq5Hpy2Ef8IuRHztoEkSDunu4rFzbP1pAM3\nJV+gPAkJD6SW72kPRe5AiZgHnglendTWiijD6aXHYivpLmvfNqhPS0e0cdURfeJF\ndbI9vb+nusxUTBpf3oXJAuqg9wKBgQDtnZmNYQ7w3ZQwCYLGsSusmoyNvuLyq7AA\njJ7b0qVhhA3YsuunGyjP7PHvHFHwwH3PjDYD9WmND8jiYFhsR43Q+8AjjuJX9NVe\nfzF6Ut13dpa4QJ12FWq9A8a9tSRWxrHjJZuthP1Dm845v28Ks8fx2TcB3EDWMNa0\n5qvlKKH0JQKBgHFRXQtkFLZlyFcqd611f6DWaGkffvTtqsrblOpRKKent8U5qGD4\nUVRrJYa+8BvIYft+IZkbH8R7UcnOb3VpF6F3UqwNveOwgoh7up+pXrBVKvmwV2DQ\nzFLrZIaHNMAbnceZDz3X/TS1Op8hueJXl3KKNwCNYHCd1aXbp1zErcStAoGAQkJX\nRkBRbUMshnSwff17o0b5eLFJEchkbNLJnZzQty+euNWztsZxDAITuMyZ4NuceZqs\nmU/+3fIP32hkX9VYK3V4L7IxVbuVICOxxV2EGkL8ZmbGQd5ZBFogOlhfyL7hbejX\nz3wtL4Qr7ph+O2rEj6E1oJQtlEzMImfMeTtqZe0CgYEAvLSNl46zyuGYZsctf60I\nWLbWg36coi4dog81C75XL99+HhuspxsDbOrtH56gPFfVURtpvZdgtY8igivUU27d\n4RRmKs22aq6DmvdNXeJ9HgMTzBb326qOiC5CVTvjQwKZEaW+nmxJpxkXDyHz03Zv\n+KnGFEejSkFLHQCN++b08c4=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-n5y12@jumbo-17e7f.iam.gserviceaccount.com",
        "client_id": "104663426995212882160",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-n5y12%40jumbo-17e7f.iam.gserviceaccount.com"
    },
    'messagingSenderId':os.getenv('messagingSenderId'),
    'appId':os.getenv('appId'),
    'measurementId':os.getenv('measurementId'),
    'databaseURL':os.getenv('databaseURL')
}



firebase = pyrebase.initialize_app(ConfigVars)