from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from .api.month.api import api as month_router
from .api.year.api import api as year_router
from .api.savings.api import api as savings_router
from .api.transaction.api import api as transaction_router
from .api.time.api import api as time_router
from .api.income.api import api as income_router
from .api.variable_expense.api import api as variable_expense_router
from .api.fixed_expense.api import api as fixed_expense_router

api: NinjaAPI = NinjaAPI(title="Budget Bop API", version="1.0")

api.add_router("/years", year_router, tags=["Years"])
api.add_router("/months", month_router, tags=["Months"])
api.add_router("/income", income_router, tags=["Income"])
api.add_router("/variable-expense", variable_expense_router, tags=["Variable Expenses"])
api.add_router("/fixed-expense", fixed_expense_router, tags=["Fixed Expenses"])
api.add_router("/savings", savings_router, tags=["Savings"])
api.add_router("/transactions", transaction_router, tags=["Transactions"])
api.add_router("/time", time_router, tags=["Time"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
