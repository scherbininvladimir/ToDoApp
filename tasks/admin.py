from django.contrib import admin

from tasks.models import TodoItem, Category, Priority, PriorityCount


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    pass

@admin.register(PriorityCount)
class PriorityCountAdmin(admin.ModelAdmin):
    pass