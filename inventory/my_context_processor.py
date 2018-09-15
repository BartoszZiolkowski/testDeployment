
def cp_logged_in(request):
    logged_in = request.user.is_authenticated

    ctx = {
        "logged_in": logged_in,
        "data": request.user

    }
    return ctx
