from django.contrib import admin

from expense_tracker.manage_expense.models import Category, Expense, MonthlyIncome


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    actions = ('delete_selected',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'date', 'category')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'reason')
    date_hierarchy = 'date'


@admin.register(MonthlyIncome)
class MonthlyIncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
    search_fields = ('user__username',)
