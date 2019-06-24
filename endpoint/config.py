import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") or
        "sqlite:///{}".format(os.path.join(basedir, "endpoint.db")))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Claim expiry in number of days from issue
    CLAIM_EXPIRY_IN_DAYS = (os.environ.get("CLAIM_EXPIRY_IN_DAYS") or 10)

    SECRET_KEY = (os.environ.get("SECRET_KEY") or "secret-key")

    ADMIN = (os.environ.get("ADMIN") or "test@test.com")

    HOSTNAME = (os.environ.get("HOSTNAME") or "localhost:5000")

    SENDGRID_API_KEY = (os.environ.get("SENDGRID_API_KEY") or "AAAABBBBCCC")

    UPLOAD_FOLDER = os.path.join(basedir, "../uploads")
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

    GOOGLE_CLIENT_ID = (os.environ.get('GOOGLE_CLIENT_ID') or 'PUT CLIENT ID')
    GOOGLE_CLIENT_SECRET = (os.environ.get('GOOGLE_CLIENT_SECRET') or 'PUT CLIENT SECRET')

    GITHUB_CLIENT_ID = (os.environ.get('GITHUB_CLIENT_ID') or 'PUT CLIENT ID')
    GITHUB_CLIENT_SECRET = (os.environ.get('GITHUB_CLIENT_SECRET') or 'PUT CLIENT SECRET')
