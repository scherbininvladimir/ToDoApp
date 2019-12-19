from django.contrib import admin

from tasks.models import TodoItem, Category, Priority, PriorityCount, CategoryCount


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    exclude = ['todos_count']

# @admin.register(Priority)
# class PriorityAdmin(admin.ModelAdmin):
#     pass

# @admin.register(PriorityCount)
# class PriorityCountAdmin(admin.ModelAdmin):
#     pass

# @admin.register(CategoryCount)
# class CategoryCountAdmin(admin.ModelAdmin):
#     list_display = ('category', 'owner', 'category_count')
