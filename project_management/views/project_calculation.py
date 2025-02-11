from django.db.models import Sum
from django.shortcuts import render

from enums.product import ProductGroupName, MainProductGroupName
from project_management.models.models import Product, Item, ItemGroup, ProductGroup, MainItemGroup, ProjectCalculation, \
    MainProductGroup


def create_item(item_pk, quantity_net, item_group):
    product = Product.objects.get(pk=item_pk)
    item = Item.objects.create(
        item_group=item_group,
        quantity_net=quantity_net,
        product=product,
    )
    return item


def update_item(item_pk, quantity_net):
    item = Item.objects.get(pk=item_pk)
    print(f"update item {item} with quantity {quantity_net}")
    if quantity_net == 0:
        item.delete()
    else:
        item.quantity_net = quantity_net
        item.save()


def create_project_calculation(request, calculation_id):

    """prepare Calculation an item groups"""
    project_calculation, created = ProjectCalculation.objects.get_or_create(pk=calculation_id)
    if created:
        main_product_groups = MainProductGroup.objects.all()
        product_groups = ProductGroup.objects.all()
        for main_product_group in main_product_groups:
            for product_group in product_groups:
                main_item_group = MainItemGroup.objects.create(
                    project_calculation=project_calculation,
                    main_product_group=main_product_group
                )
                item_group = ItemGroup.objects.create(
                    main_item_group=main_item_group,
                    product_group=product_group
                )

    """save or update item"""
    if request.method == "POST":
        if 'pdf' in request.POST:
            print("xxx")

        else:
            print(request.POST)
            quantity_net = request.POST.get('quantity_net', None)
            product_group_pk = request.POST.get('product_group_pk', None)
            if quantity_net is not None:
                if request.POST.get("save_item", None):
                    item_group = ItemGroup.objects.get(
                        product_group__pk=product_group_pk,
                        main_item_group__project_calculation=project_calculation
                    )
                    create_item(request.POST.get("save_item", None), float(quantity_net), item_group)
                if request.POST.get("update_item", None):
                    update_item(request.POST.get("update_item", None), float(quantity_net))

    """tmp"""
    groups = [
        ProductGroupName.FEEDING_CABLE.value,
        ProductGroupName.MAIN_DISTRIBUTION.value,
        ProductGroupName.METER_PANEL.value
    ]
    #item_group = MainItemGroup.objects.all().first()
    #product_groups = list(ProductGroup.objects.filter(item_group=item_group).values_list('name', flat=True))

    items = Item.objects.filter(
        product__product_group__name__in=groups
    ).order_by("id").distinct()

    products = Product.objects.filter(
        product_group__name__in=groups
    ).exclude(
        item_set__in=list(items)
    ).order_by(
        "product_group__group_id", "id"
    )
    print(products)

    product_groups = ProductGroup.objects.filter(
        main_product_group__name=MainProductGroupName.BASE_INSTALLATION.value
    ).order_by("group_id")

    item_ids = list(items.values_list('product', flat=True))
    print(f"****{item_ids}****")

    item_groups = ItemGroup.objects.filter(main_item_group__project_calculation=project_calculation)
    for item_group in item_groups:
        items_in_group = item_group.item_set

        item_sum = items_in_group.aggregate(
            # Sum("total_selling_price_inflation"),
            Sum("total_purchase_price"),
        )
        print(item_sum)

    main_item_groups = MainItemGroup.objects.filter(project_calculation=project_calculation)
    for main_item_group in main_item_groups:
        items_in_group = Item.objects.filter(item_group__main_item_group=main_item_group)

        item_sum = items_in_group.aggregate(
            Sum("total_selling_price_margin"),
            Sum("total_purchase_price"),
        )
        print(item_sum)
        main_item_group.total_purchase_price = item_sum.get('total_purchase_price__sum', 0)
        main_item_group.total_selling_price_margin = item_sum.get('total_selling_price_margin__sum', 0)
        main_item_group.save()

    """
    item_forms = []
    for item in items:
        item_forms.append(ItemForm(initial={"quantity_net": item.quantity_net}))
    item_selection = zip(items, item_forms)
    """

    """
    item_forms = [ItemForm(initial={"quantity_net": 0})] * len(products)
    item_choice = zip(products, item_forms)

    item_sum = items.aggregate(
        # Sum("total_selling_price_inflation"),
        Sum("total_purchase_price"),
    )
    """

    #item_group.total_selling_price_margin = item_sum.get("total_purchase_price__sum", 0)

    context = {
        #"products": products,
        #"item_forms": item_forms,
        #"item_choice": item_choice,
        #"item_selection": item_selection,
        # "item_sum": item_sum,
        # "item_group": item_group,
        "ps": products,
        "product_groups": product_groups,
        "items": items,
        "item_ids": item_ids,
        "main_item_group": main_item_group,
    }

    return render(request, "project_calculation/select_project_items.html", context)
