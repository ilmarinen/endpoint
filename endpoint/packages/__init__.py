def init(app, admin):
    import public
    import user
    import twilio
    
    # what is public? it imports views?
    # endpoint/public/__init__ --> endpoint/public/views.py
    # app.register_blueprint(bp, url_prefix="/")
    # what does this do?
    # This is using flask's Blueprint and render_template
    # there is a lot of functions decorating
    # ardoun the index page to require login, handle caching
    # and provide routing then templating
    # admin is not used? why?
    public.init(app, admin)
    # User has much more going on
    # it has groups, tokens, users
    # it was blueprint routes for /user and /api
    # it uses a LoginManager
    user.init(app, admin)
    twilio.init(app, admin)
