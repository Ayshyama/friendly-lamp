from django.shortcuts import render, redirect

from project_management.forms import ProjectCalculationForm
from project_management.models.models import ProjectCalculation, MainProductGroup, ProductGroup, MainItemGroup, \
    ItemGroup


def prepare_empty_calculation(project_calculation):
    main_product_groups = MainProductGroup.objects.all()
    product_groups = ProductGroup.objects.all()
    for main_product_group in main_product_groups:
        for product_group in product_groups:
            main_item_group = MainItemGroup.objects.create(
                project_calculation=project_calculation,
                main_product_group=main_product_group
            )
            ItemGroup.objects.create(
                main_item_group=main_item_group,
                product_group=product_group
            )
    return project_calculation


def project_calculation_list(request):
    project_calculations = ProjectCalculation.objects.all()

    if request.method == "POST":
        pass


    context = {
        "project_calculations": project_calculations,
    }

    return render(request, "project_calculation/calculation_list.html", context)


def add_project_calculation(request):
    project_calculation_form = ProjectCalculationForm()

    if request.method == "POST":
        print(request.POST)
        project_calculation_form = ProjectCalculationForm(request.POST)
        print(project_calculation_form)
        if project_calculation_form.is_valid():
            print(project_calculation_form)
            project_calculation = project_calculation_form.save()
            project_calculation = prepare_empty_calculation(project_calculation)
            print(project_calculation.pk)
            return redirect("create_project_calculation", project_calculation.pk)

    context = {
        "calculation_form": project_calculation_form,
    }
    return render(request, "project_calculation/new_calculation.html", context)