import json

from rest_framework.views import APIView
from datetime import datetime
from expense_tracker.manage_expense.models import Expense, Category, MonthlyIncome
from rest_framework.response import Response
from expense_tracker.manage_expense.serializers import CategorySerializer, ExpenseSerializer

# Create your views here.

class CategoryView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serialized_categories = CategorySerializer(categories, many=True)
        return Response({"categories": serialized_categories.data}, status=200)


class ManageExpenseView(APIView):

    def filter_expenses(self, expenses, search_query=None, date_range=None):
        if search_query:
            expenses = expenses.filter(title__icontains=search_query)
        if date_range:
            date_from, date_to = date_range.split("to")
            date_from = datetime.strptime(date_from.strip(), "%d-%m-%Y").date()
            date_to = datetime.strptime(date_to.strip(), "%d-%m-%Y").date()
            expenses = expenses.filter(date__range=(date_from, date_to))

        return expenses

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        if not expenses.exists():
            return Response({"msg": "No expenses found for the user."}, status=404)

        filter_flag = json.loads(request.query_params.get("filter", "false").lower())

        if filter_flag:
            search_query = request.query_params.get("term", None)
            date_range = request.query_params.get("date_range", None)
            expenses = self.filter_expenses(expenses, search_query=search_query, date_range=date_range)

        serialized_expenses = ExpenseSerializer(expenses, many=True)

        return Response({"expenses": serialized_expenses.data}, status=200)

    def post(self, request):
        data = request.data
        expense_name = data.get('expense_name')
        expense_amount = data.get('expense_amount')
        expense_date = data.get('expense_date')
        category_id = data.get('category_id')
        reason = data.get('reason')

        if not all([expense_name, expense_amount, expense_date, category_id]):
            return Response(
                {
                    "error": "Missing required fields.",
                    "msg": "Required fields are expense_name,expense_amount,expense_date,category_id",
                }, 
                status=400
            )
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Requested category does not exist."}, status=400)

        try:
            date_of_expense = datetime.strptime(expense_date, "%d-%m-%Y").date()
        except ValueError:
            return Response({"error": "Invalid expense date format."}, status=400)

        expense = Expense.objects.create(
            user=request.user,
            title=expense_name,
            amount=expense_amount,
            date=date_of_expense,
            category=category,
            reason=reason
        )

        serialized_expense = ExpenseSerializer(expense)
        return Response(
            {
                "msg": "Expense added successfully.",
                "expense": serialized_expense.data,
            },
            status=201,
        )
        
