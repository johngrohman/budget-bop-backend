"""
URL configuration for budgetbop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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

api = NinjaAPI(title="Budget Bop API", version="1.0")

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
