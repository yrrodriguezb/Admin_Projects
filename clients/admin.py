from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import Client, SocialNetwork


class ClientAdmin(admin.ModelAdmin):
    exclude = ('user', )

class ClientInLine(admin.StackedInline):
    model = Client
    can_delete = False

class SocialNetworkInLine(admin.StackedInline):
    model = SocialNetwork
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [ClientInLine, SocialNetworkInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)