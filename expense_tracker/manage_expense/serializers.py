from rest_framework import serializers
from expense_tracker.manage_expense.models import Expense, Category, MonthlyIncome

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        fields = ['id', 'name']
        model = Category

class ExpenseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    date = serializers.DateField(read_only=True)
    category = CategorySerializer(read_only=True)
    reason = serializers.CharField(read_only=True)

    class Meta:
        fields = ['id', 'user', 'title', 'amount', 'date', 'category', 'reason']
        model = Expense