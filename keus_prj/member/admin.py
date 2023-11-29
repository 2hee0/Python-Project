from django.contrib import admin

from django.db import models
from .models import Member

from board.models import Board, Category
# Register your models here.

admin.site.register(Member)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    # prepopulated_fields : 장고 제공 기능,
    # 다른 필드의 값을 가지고 와서 자동으로 채울수 있도록 함


admin.site.register(Category, CategoryAdmin)

