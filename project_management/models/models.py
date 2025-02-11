from datetime import date

from ChargePointHandler.cp_models.infrastructure import (ChargingStation,
                                                         Location)
from ChargePointHandler.models import User
from django.conf import settings
from django.db import models
from enums.generic import choices
from enums.pm import InstallationStage, LocationStage, ParkingSpaceType
from multiselectfield import MultiSelectField

from enums.product import ProductGroupName, MainProductGroupName, Unite, ProductStatus, ProductType


class LocationDetail(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    location_stage = models.CharField(
        max_length=32,
        choices=choices(LocationStage),
        default=LocationStage.OLD_BUILDING.value,
    )
    name = models.CharField(max_length=128, null=True, blank=True)
    parking_spaces = models.IntegerField()
    particularities = models.TextField(max_length=512, null=True, blank=True)
    number_net_connections = models.IntegerField(null=True, blank=True)
    requested_capacity = models.IntegerField(null=True, blank=True)
    approved_capacity = models.IntegerField(null=True, blank=True)
    spare_capacity = models.IntegerField(null=True, blank=True)
    user_group = models.TextField(null=True, blank=True)
    main_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="main_contact",
    )
    installer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="installer"
    )
    property_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="property_manager",
    )
    existing_charging_stations = models.BooleanField(default=False)
    parking_space_types = MultiSelectField(
        max_length=30, choices=choices(ParkingSpaceType), null=True)

    def __str__(self):
        return "{0} - {1} with {2} PS".format(
            self.id, self.location_stage, self.parking_spaces
        )


class LocationDocument(models.Model):
    location_detail = models.ForeignKey(
        LocationDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    document = models.FileField(
        upload_to="media", null=True, blank=True
    )  # ToDo: tbd path

    def __str__(self):
        return "{0}".format(self.name)


class InstallationRequest(models.Model):
    location_detail = models.ForeignKey(
        LocationDetail, on_delete=models.CASCADE)
    charging_stations = models.IntegerField()
    prepared_parking_spaces = models.IntegerField()
    basic_installation = models.IntegerField()

    def __str__(self):
        return "{0} basic, {1} preparations, {2} CPs".format(
            self.basic_installation,
            self.prepared_parking_spaces,
            self.charging_stations,
        )


class Milestone(models.Model):
    location_detail = models.ForeignKey(
        LocationDetail, on_delete=models.CASCADE)
    target_date = models.DateField()
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    created = models.DateField(auto_created=True)
    # assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.target_date, self.name)


class ParkingSpace(models.Model):
    location_detail = models.ForeignKey(
        LocationDetail, on_delete=models.SET_NULL, null=True
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    charging_station = models.ForeignKey(
        ChargingStation, on_delete=models.SET_NULL, null=True, blank=True
    )
    number = models.IntegerField(null=True)
    position = models.CharField(max_length=256, null=True)
    installation_stage = models.CharField(
        max_length=128,
        choices=choices(InstallationStage),
        default=InstallationStage.NO_INSTALLATION.value,
    )
    parking_space_type = models.CharField(
        max_length=128,
        choices=choices(ParkingSpaceType),
        default=ParkingSpaceType.UNDERGROUDN_CAR_PARK.value,
    )

    def __str__(self):
        return f"{self.basic_installation} " \
               f"basic, {self.prepared_parking_spaces} " \
               f"preparations, {self.charging_stations} CPs"


"""
class ticket(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    topic = models.CharField(max_length=128)
    description = models.TextField()
    status = models.CharField(
        choices=TicketStatus.choices,
        max_length=128,
        default=TicketStatus.new.value)
    report_date = models.DateTimeField

    def __str__(self):
        return "{0}: {1}".format(self.topic, self.status)
"""


class MainProductGroup(models.Model):
    name = models.CharField(
        max_length=128,
        choices=choices(MainProductGroupName),
        default=MainProductGroupName.PROJECT_ENGINEERING.value,
    )
    group_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} ({self.group_id})"


class ProductGroup(models.Model):
    main_product_group = models.ForeignKey(
        MainProductGroup, on_delete=models.PROTECT, null=True
    )
    name = models.CharField(
        max_length=256,
        choices=choices(ProductGroupName),
        default=ProductGroupName.FEEDING_CABLE.value
    )
    group_id = models.IntegerField(null=True)

    def hash_name(self):
        return "#"+self.name

    def __str__(self):
        return f"{self.name} ({self.group_id})"


class Product(models.Model):
    product_group = models.ManyToManyField(ProductGroup)
    internal_description_de = models.TextField()
    internal_description_en = models.TextField()
    customer_description_de = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    source = models.CharField(max_length=512, null=True)
    manufacturer = models.CharField(max_length=128, null=True)
    article_number = models.CharField(max_length=64, null=True)
    bundle_quantity = models.IntegerField(default=1)

    status = models.CharField(
        max_length=32,
        choices=choices(ProductStatus),
        default=ProductStatus.ACTIVE.value,
    )
    product_type = models.CharField(
        max_length=128,
        choices=choices(ProductType),
        default=ProductType.PRODUCT.value,
    )
    unite = models.CharField(
        max_length=32,
        choices=choices(Unite),
        default=Unite.PICE.value,
    )

    taxes = models.FloatField(default=19.0, help_text="in %")
    working_time = models.FloatField(default=0.0, help_text="in h")
    inflation_rate = models.FloatField(default=2.0, help_text="in %")
    target_margin = models.FloatField(default=30.0, help_text="in %")
    safety_margin = models.FloatField(default=2.0, help_text="in %")

    shipping_cost_per_unite = models.FloatField(default=0)
    packaging_cost_per_unite = models.FloatField(default=0)
    purchase_price = models.FloatField(default=0)
    target_purchase_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)

    def hash_article_number(self):
        return "#"+str(self.article_number_str())

    def article_number_str(self):
        return "A"+self.article_number.replace('.', '')

    def calculate_target_purchase_price(self):
        return (self.purchase_price + self.shipping_cost_per_unite + self.packaging_cost_per_unite
                )/(1 - self.safety_margin/100)

    def save(self, *args, **kwargs):
        self.target_purchase_price = round(self.calculate_target_purchase_price(), 2)
        self.selling_price = round(self.target_purchase_price / (1-self.target_margin/100), 2)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.internal_description_de} ({self.product_group})"


class AbstractItem(models.Model):
    position_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_purchase_price = models.FloatField(null=True)
    total_selling_price_margin = models.FloatField(null=True)

    """
    def calculate_selling_price(self):
        self.total_selling_price_margin = self.total_purchase_price
    """

    class Meta:
        abstract = True


class ProjectCalculation(AbstractItem):
    execution_date = models.DateField(default=date.today())

    def __str__(self):
        return f"Project calculation: {self.execution_date}"


class MainItemGroup(AbstractItem):
    project_calculation = models.ForeignKey(
        ProjectCalculation, on_delete=models.SET_NULL, null=True
    )
    main_product_group = models.ForeignKey(
        MainProductGroup, on_delete=models.SET_NULL, null=True
    )
    project_calculation = models.ForeignKey(ProjectCalculation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.main_product_group.name}"


class ItemGroup(models.Model):
    main_item_group = models.ForeignKey(
        MainItemGroup, on_delete=models.CASCADE, null=True
    )
    product_group = models.ForeignKey(
        ProductGroup, on_delete=models.SET_NULL, null=True
    )

    #def __str__(self):
    #    return f"{self.product_group.name}"


class Item(AbstractItem):
    item_group = models.ForeignKey(
        ItemGroup, on_delete=models.CASCADE, null=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="item_set"
    )
    quantity_net = models.FloatField(default=0)
    quantity_gross = models.IntegerField(default=0)

    def calculate_selling_price_margin(self, purchase_date=0, extra_margin=0):
        days = 100
        return self.product.selling_price * (1+self.product.inflation_rate/100*days/365) / (1-extra_margin/100)

    def save(self, *args, **kwargs):
        if self.product.unite == Unite.METER.value:
            self.quantity_gross = round(self.quantity_net*1.1, 0)
        elif self.product.unite == Unite.PICE.value:
            self.quantity_gross = self.quantity_net
        else:
            self.quantity_gross = round(self.quantity_net, 0)

        try:
            self.total_purchase_price = self.quantity_gross * self.product.target_purchase_price
            self.total_selling_price_margin = round(self.quantity_gross * self.calculate_selling_price_margin(), 2)
        except:
            pass
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.internal_description_de} " \
               f"{self.quantity_gross} " \
               f"x {self.product.selling_price} " \
               f"= {self.total_selling_price_margin}"

