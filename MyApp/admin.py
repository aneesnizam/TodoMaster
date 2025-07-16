from django.contrib import admin
from .models import userDatas
from .models import task
from django.contrib.auth.hashers import make_password


# Register your models here.
class UserDataAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "username")

    def save_model(self, request, obj, form, change):
        if not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)

        super().save_model(request, obj, form, change)


admin.site.register(userDatas, UserDataAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "due_date",
                    "category", "important", "completed")


admin.site.register(task, TaskAdmin)
