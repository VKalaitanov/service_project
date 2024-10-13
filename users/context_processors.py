# context_processors.py
from .models import GlobalMessage

def global_messages(request):
    messages = GlobalMessage.objects.filter(is_active=True).order_by('-created_at')
    return {'global_messages': messages}
