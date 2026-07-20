class SecurityHeadersMiddleware:
    """Apply restrictive browser policy and prevent caching sensitive pages."""

    sensitive_prefixes = (
        "/quan-tri/",
        "/dang-ky-tu-van/",
        "/dat-lich-hoc-thu/",
        "/dang-ky-thanh-cong/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault(
            "Permissions-Policy", "camera=(), geolocation=(), microphone=()"
        )
        response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")
        if request.path.startswith(self.sensitive_prefixes):
            response.headers["Cache-Control"] = "no-store, private"
        return response
