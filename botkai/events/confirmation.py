import os
def confirmation(request):
    return os.getenv("CONFIRMATION")