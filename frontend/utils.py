def process_redirect_to(redirect_to):
    redirect_to = redirect_to if redirect_to else "/home"
    if redirect_to != "/home":
        redirect_to = "/user/" + redirect_to
    return redirect_to
