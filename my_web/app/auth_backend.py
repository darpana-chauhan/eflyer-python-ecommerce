from django.contrib.sessions.middleware import SessionMiddleware

class SeparateAdminUserSessionMiddleware(SessionMiddleware):
    """
    Custom Middleware to maintain separate sessions for Admin and Normal Users.
    """
    def process_request(self, request):
        super().process_request(request)

        if request.path.startswith("/admin/"):
            request.session["is_admin"] = True  # ✅ Mark as Admin Session
        else:
            request.session["is_admin"] = False  # ✅ Mark as User Session
