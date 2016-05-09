from django.contrib import admin

from .models import Post  #, Images


class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "timestamp"]  # displays

    def queryset(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(user=request.user)

    class Meta:
        model = Post  #, Images

admin.site.register(Post, PostAdmin)

# class ImagesAdmin(admin.ModelAdmin):
#     list_display = ["post", "image"]  # displays
#
#     def queryset(self, request):
#         if request.user.is_superuser or request.user.is_staff:
#             return Images.objects.all()
#         return Images.objects.filter(user=request.user)
#
#     class Meta:
#         model = Images
#
# admin.site.register(Images, ImagesAdmin)
