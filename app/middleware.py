class SkipNgrokWarningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["HTTP_NGROK_SKIP_BROWSER_WARNING"] = "true"
        response = self.get_response(request)
        response["ngrok-skip-browser-warning"] = "true"  # Response ga ham qo‘shamiz
        return response
