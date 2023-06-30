from django.contrib import admin
from main.models import User, PostModel, Comment  # ,Friend, FriendRequest

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content',
                    'created_by', 'date_created', 'likes_number']


# class FriendListAdmin(admin.ModelAdmin):
#     list_filter = ['user']
#     list_display = ['user']
#     search_fields = ['user']
#     readonly_fields = ['user',]

#     class Meta:
#         model = Friend


# admin.site.register(Friend, FriendListAdmin)


# class FriendRequestAdmin(admin.ModelAdmin):
#     list_filter = ['sender', 'receiver']
#     list_display = ['sender', 'receiver',]
#     search_fields = ['sender__username', 'receiver__username']

#     class Meta:
#         model = FriendRequest


admin.site.register(User, UserAdmin)
admin.site.register(PostModel, PostAdmin)
admin.site.register(Comment)
# admin.site.register(FriendRequest, FriendRequestAdmin)
