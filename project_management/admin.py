from django.contrib import admin
from project_management.models.models import (InstallationRequest, LocationDetail,
                                              ParkingSpace, ProjectCalculation, ItemGroup, ProductGroup, Product, Item,
                                              MainItemGroup, MainProductGroup)

admin.site.register(InstallationRequest)


@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ("location_detail", "owner", "number", "installation_stage")
    list_filter = ("installation_stage",)
    search_fields = (
        "location_detail",
        "owner",
        "number",
    )
    ordering = (
        "location_detail",
        "owner",
        "number",
    )


@admin.register(LocationDetail)
class LocationDetailAdmin(admin.ModelAdmin):
    list_display = ("location", "name", "location_stage", "parking_spaces")
    list_filter = ("location_stage",)
    search_fields = (
        "location_detail",
        "owner",
        "number",
    )
    ordering = ("location",)


@admin.register(ProjectCalculation)
class ProjectCalculationAdmin(admin.ModelAdmin):
    list_display = ("execution_date",)


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ("product_group",)


@admin.register(MainItemGroup)
class MainItemGroupAdmin(admin.ModelAdmin):
    list_display = ("main_product_group", "total_purchase_price", "total_selling_price_margin")


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("group_id", "name")


@admin.register(MainProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("group_id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("internal_description_de", "internal_description_en", "purchase_price")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity_net", "quantity_gross")

