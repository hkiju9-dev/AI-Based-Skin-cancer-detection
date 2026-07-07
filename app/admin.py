from django.contrib import admin
from .models import Users,Profile,ContactMessage
from django.core.mail import send_mail
admin.site.register(Users)
admin.site.register(Profile)
# admin.site.register(ContactMessage)
# Register your models here.


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'admin_reply')
    search_fields = ('name', 'email', 'subject')

    def save_model(self, request, obj, form, change):
        """Automatically send email reply when admin submits a response."""
        if 'admin_reply' in form.changed_data:
            send_mail(
                subject=f"Reply to your inquiry: {obj.subject}",
                message=obj.admin_reply,
                from_email="ilsachoudhry@gmail.com",  # Update with your email
                recipient_list=[obj.email],
                fail_silently=False,
            )
        super().save_model(request, obj, form, change)

admin.site.register(ContactMessage, ContactMessageAdmin)
