from views import bp
from link_archiver import mediawiki_bot


def init(app, admin):
    app.register_blueprint(bp, url_prefix='/twilio')
    mediawiki_bot.init(
        app.config["WIKI_URL"],
        app.config["WIKI_USERNAME"],
        app.config["WIKI_PASSWORD"])
