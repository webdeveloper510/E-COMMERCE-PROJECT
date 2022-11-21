from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Logo)
class LogoModelAdmin(admin.ModelAdmin):
  list_display = ('id','image','display')

  def has_add_permission(self, request):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  def has_add_permission(self, request):
    if self.model.objects.count() >= 1:
        return False
    return super().has_add_permission(request)

  def display(self, obj):
     return format_html(f'<img src="/media/{obj.image}" style="height:30px;">')

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
  list_display = ('id','url')

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
  exclude=()
  list_display = ('id','menu')
  # list_display = ('id','content','click_me','menu')

  # def content(self, obj):
  #    print(obj)
  #    return format_html(f'<span style="color:red">{obj.menu[:100]}</span>')
  
  # def click_me(self, obj):
  #   return format_html('<a href="#">View</a>')

  
admin.site.register(Banner)
admin.site.register(Services)
admin.site.register(FAQ)

