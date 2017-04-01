def init(app, admin):
    import public
    import user

    public.init(app, admin)
    user.init(app, admin)
