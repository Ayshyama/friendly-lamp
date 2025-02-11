from django.urls import path

from project_management.views.project_calculation import create_project_calculation
from project_management.views.project_calculation_list import project_calculation_list, add_project_calculation
from project_management.views.project_request import create_project_request

urlpatterns = [
    # test urls
    path("project/new/", create_project_request, name="create_project"),
    path("project/calculation/", project_calculation_list, name="create_project_calculation"),
    path("project/calculation/add/", add_project_calculation, name="add_project_calculation"),
    path("project/calculation/<str:calculation_id>/", create_project_calculation, name="create_project_calculation"),

]
