# Register your models here.
from django.contrib.admin import ModelAdmin, register

from bee.models import EmailLog


@register(EmailLog)
class EmailLogAdmin(ModelAdmin):
    list_display = ['created', 'name', 'email', 'short_text']

    def short_text(self, log: EmailLog):
        return log.message[:200]
