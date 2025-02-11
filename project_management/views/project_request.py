from random import randint

from ChargePointHandler.cp_models.infrastructure import Location
from ChargePointHandler.forms import (AddressForm, CheckSumForm,
                                      ProfileGeneralForm, ProfileSimpleForm,
                                      UserForm, UserSimpleForm)
from ChargePointHandler.helpers.orm import get_object_or_none
from ChargePointHandler.models import Address, Profile, User
from django.shortcuts import render
from loguru import logger
from project_management.forms import (InstallationRequestForm,
                                      LocationDetailExtrasForm,
                                      LocationDetailForm)
from project_management.models.models import InstallationRequest, LocationDetail


def initialize_user_form(request, person=""):
    initial = {
        "first_name": request.session.get(person + "first_name"),
        "last_name": request.session.get(person + "number"),
        "email": request.session.get(person + "email"),
        "role": request.session.get(person + "role"),
    }

    if person != "":
        return UserSimpleForm(initial=initial)
    else:
        return UserForm(initial=initial)


def initialize_profile_form(request):
    if request.session.get("xx"):
        return ProfileGeneralForm()
    else:
        return ProfileGeneralForm()


def initialize_simple_profile_form(request, person=""):
    if person != "":
        person = person + "_"
    return ProfileSimpleForm(
        initial={
            "salutation": request.session.get(person + "salutation"),
            "phone": request.session.get(person + "phone"),
            "company": request.session.get(person + "company"),
        }
    )


def initialize_location_detail_form(request):
    return LocationDetailForm(
        initial={
            "name": request.session.get("object_name", None),
            "location_stage": request.session.get("location_stage", None),
            "parking_spaces": request.session.get("parking_spaces", None),
            "parking_space_types": request.session.get("parking_space_types", None),
        }
    )


def initialize_address_form(request):
    if (
        request.session.get("street")
        and request.session.get("number")
        and request.session.get("city")
        and request.session.get("zip_code")
        and request.session.get("country")
    ):
        return AddressForm(
            initial={
                "street": request.session.get("street"),
                "number": request.session.get("number"),
                "city": request.session.get("city"),
                "zip_code": request.session.get("zip_code"),
                "country": request.session.get("country"),
            }
        )
    else:
        return AddressForm()


def initialize_installation_request_form(request):
    return InstallationRequestForm(
        initial={
            "prepared_parking_spaces": request.session.get(
                "prepared_parking_spaces", None
            ),
            "charging_stations": request.session.get("charging_stations", None),
        }
    )


def initialize_location_detail_extra_form(request):
    return LocationDetailExtrasForm(
        initial={
            "user_group": request.session.get("user_group", None),
            "particularities": request.session.get("particularities", None),
            "spare_capacity": request.session.get("spare_capacity", None),
            "requested_capacity": request.session.get("requested_capacity", None),
            "number_net_connections": request.session.get(
                "number_net_connections", None
            ),
        }
    )


def project_request_object(request, messages):
    object_detail_form = LocationDetailForm(request.POST)
    address_form = AddressForm(request.POST)

    if ("already exists" in str(address_form.errors) or address_form.is_valid()) and (
        "already exists" in str(object_detail_form.errors)
        or object_detail_form.is_valid()
    ):
        request.session["street"] = address_form.data.get("street")
        request.session["number"] = address_form.data.get("number")
        request.session["city"] = address_form.data.get("city")
        request.session["zip_code"] = address_form.data.get("zip_code")
        request.session["country"] = address_form.data.get("country")

        existing = (
            True if request.POST.get(
                "existing_charging_stations") == "on" else False
        )
        request.session["object_name"] = object_detail_form.data.get("name")
        request.session["location_stage"] = object_detail_form.data.get(
            "location_stage"
        )
        request.session["parking_spaces"] = object_detail_form.data.get(
            "parking_spaces"
        )
        request.session["existing_charging_stations"] = existing
        request.session["parking_space_types"] = dict(object_detail_form.data).get(
            "parking_space_types"
        )
        logger.debug(f"EXISTING: {existing}")

        address = get_object_or_none(
            Address,
            street=request.session["street"],
            number=request.session["number"],
            city=request.session["city"],
            zip_code=request.session["zip_code"],
            country=request.session["country"],
        )

        if address and get_object_or_none(Location, address=address):
            messages.append(
                {
                    "msg": "Für diese Adresse wurde bereits ein Projekt angelegt.\n"
                    "Bitte melden Sie sich an, um Ihr Projekt einzusehen \n"
                    "oder kontaktieren Sie den Projektverantwortlichen",
                    "success": False,
                }
            )
            request.session["tab"] = "pills_object_tab"
        else:
            request.session["tab"] = "pills_contact_tab"

    else:
        messages.append({"msg": "Ungültige Eingabe", "success": False})
        request.session["tab"] = "pills_object_tab"

    return request, messages


def contact(request, messages):
    user_form = UserForm(request.POST)
    profile_form = ProfileGeneralForm(request.POST)

    if request.POST.get("dsgvo_agreed", None) != "on":
        request.session["dsgvo_agreed"] = False
        messages.append(
            {
                "msg": "Bitte stimmen Sie den Datenschutzvereinbarungen zu um fortzufahren.",
                "success": False,
            }
        )
        request.session["tab"] = "pills_contact_tab"

    else:
        request.session["conditions_agreed"] = True

        if ("already exists" in str(user_form.errors) or user_form.is_valid()) and (
            "already exists" in str(
                profile_form.errors) or profile_form.is_valid()
        ):
            user, created = User.objects.get_or_create(
                email=user_form.data.get("email")
            )

            profile = None
            if not created:
                profile = get_object_or_none(Profile, user=user)

            if not profile or created:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

            request.session["user_email"] = user.email
            request.session["tab"] = "pills_request_tab"

        else:
            messages.append({"msg": "Ungültige Eingabe", "success": False})
            request.session["tab"] = "pills_contact_tab"

    return request, messages


def installation_request(request, messages):
    installation_request_form = InstallationRequestForm(request.POST)

    if installation_request_form.is_valid():
        request.session["prepared_parking_spaces"] = installation_request_form.data.get(
            "prepared_parking_spaces"
        )
        request.session["charging_stations"] = installation_request_form.data.get(
            "charging_stations"
        )

        messages.append(
            {"msg": "Wir haben Ihre Anfrage entgegengenommen.", "success": True}
        )
        request.session["tab"] = "pills_object_details_tab"

    else:
        messages.append({"msg": "Ungültige Eingabe", "success": False})
        request.session["tab"] = "pills_request_tab"

    return request, messages


def location_detail_request(request, messages):
    location_detail_extra_form = LocationDetailExtrasForm(request.POST)

    if location_detail_extra_form.is_valid():
        request.session["user_group"] = location_detail_extra_form.data.get(
            "user_group"
        )
        request.session["particularities"] = location_detail_extra_form.data.get(
            "particularities"
        )
        request.session["spare_capacity"] = location_detail_extra_form.data.get(
            "spare_capacity"
        )
        request.session["requested_capacity"] = location_detail_extra_form.data.get(
            "requested_capacity"
        )
        request.session["number_net_connections"] = location_detail_extra_form.data.get(
            "number_net_connections", None
        )

        request.session["tab"] = "pills_additional_contact_tab"

    else:
        messages.append({"msg": "Ungültige Eingabe", "success": False})
        request.session["tab"] = "pills_object_details_tab"

    return request, messages


def additional_contact(request, messages):
    post = dict(request.POST)

    # handle user and profile form for local_admin
    if request.POST.get("same_person", None) == "on":
        admin = User.objects.get(email=request.session.get("user_email"))
    else:
        first_contact_post = {k: post[k][0] for k in request.POST}
        user_form_admin = UserForm(first_contact_post)
        profile_form_admin = ProfileSimpleForm(first_contact_post)

        if (
            "already exists" in str(user_form_admin.errors)
            or user_form_admin.is_valid()
        ) and (
            "already exists" in str(profile_form_admin.errors)
            or profile_form_admin.is_valid()
        ):
            # ToDo using 'email' only might be too less for terminating a user
            admin, created = User.objects.get_or_create(
                email=user_form_admin.data.get("email")
            )

            # create user and profile if both does not exist
            if not created:
                profile = get_object_or_none(Profile, user=admin)
                if not profile:
                    profile = profile_form_admin.save(commit=False)
                    profile.user = admin
                    profile.save()
            else:
                admin = user_form_admin.save()
                profile = profile_form_admin.save(commit=False)
                profile.user = admin
                profile.save()
        else:
            admin = None

    # handle user and profile form for installer
    if request.POST.get("specific_installer", None) == "on":
        second_contact_post = {k: post[k][-1] for k in request.POST}
        user_form_installer = UserForm(second_contact_post)
        profile_form_installer = ProfileSimpleForm(second_contact_post)

        if (
            "already exists" in str(user_form_installer.errors)
            or user_form_installer.is_valid()
        ) and (
            "already exists" in str(profile_form_installer.errors)
            or profile_form_installer.is_valid()
        ):
            # ToDo using 'email' only might be too less for terminating a user
            installer, created = User.objects.get_or_create(
                email=user_form_installer.data.get("email")
            )

            # create user and profile if both does not exist
            if not created:
                profile = get_object_or_none(Profile, user=installer)
                if not profile:
                    profile = profile_form_installer.save(commit=False)
                    profile.user = admin
                    profile.save()
            else:
                installer = user_form_installer.save()
                profile = profile_form_installer.save(commit=False)
                profile.user = installer
                profile.save()
        else:
            installer = None
    else:
        installer = None

    # request.session['admin'] = admin
    # request.session['installer'] = installer

    # check checksum
    solution = request.session.get("result")
    entered_result = int(request.POST.get("result", None))

    if entered_result != solution:
        logger.debug("FALSE")
        request = get_calculation_string(request, new=True)
        request.session["tab"] = "pills_additional_contact_tab"

    else:
        logger.debug("SUCCESS")

        # create whole project
        # address and location
        address, created = Address.objects.get_or_create(
            street=request.session["street"],
            number=request.session["number"],
            city=request.session["city"],
            zip_code=request.session["zip_code"],
            country=request.session["country"],
        )
        location = get_object_or_none(Location, address=address)
        if not location:
            location = Location.objects.create(
                name=request.session.get("object_name"))
            location.address.add(address)
            location.save()
        logger.debug(address)
        logger.debug(location)

        # location details
        location_detail = LocationDetail.objects.create(
            location=location,
            name=request.session.get("object_name"),
            location_stage=request.session.get("location_stage"),
            parking_spaces=request.session.get("parking_spaces"),
            existing_charging_stations=request.session.get(
                "existing_charging_stations"
            ),
            parking_space_types=request.session.get("parking_space_types"),
            main_contact=User.objects.get(
                email=request.session.get("user_email")),
            installer=installer,
            property_manager=admin,
            user_group=request.session.get("user_group"),
            particularities=request.session.get("particularities"),
            spare_capacity=request.session.get("spare_capacity"),
            requested_capacity=request.session.get("requested_capacity"),
            number_net_connections=request.session.get(
                "number_net_connections"),
        )
        logger.debug(location_detail)

        installation_request = InstallationRequest.objects.create(
            location_detail=location_detail,
            charging_stations=request.session.get("charging_stations"),
            prepared_parking_spaces=request.session.get(
                "prepared_parking_spaces"),
            basic_installation=0,
        )
        logger.debug(installation_request)

        request.session["tab"] = "final"

    return request, messages


def get_calculation_string(request, new=False):
    calculation_string = request.session.get("calculation_string", None)
    result = request.session.get("result", None)

    if not calculation_string or not result or new:
        a = randint(10, 20)
        b = randint(1, 10)
        operator = randint(0, 1)

        if operator:
            calculation_string = " " + str(a) + "  + " + str(b) + " = "
            result = a + b
        else:
            calculation_string = " " + str(a) + "  - " + str(b) + " = "
            result = a - b

        request.session["calculation_string"] = calculation_string
        request.session["result"] = result

    return request


def create_project_request(request):
    """5-step project request form

    Pills:
    1. pills_object_tab: basic object data, object address - returns 'object'
    2. pills_contact_tab: contact person of object (user, profile) - returns 'contact'
    3. pills_request_tab: installation target date, parking spaces (type and amount) - retuns 'request'
    4. pills_object_details_tab: technical details about the object and document upload - returns 'details'
    5. pills_additional_contact_tab: further contacts and check-sum - returns 'additional'
    """

    messages = []
    request.session["tab"] = "pills_object_tab"

    """initialize forms"""
    user_form = initialize_user_form(request)
    profile_form = initialize_profile_form(request)
    location_detail_form = initialize_location_detail_form(request)
    address_form = initialize_address_form(request)
    installation_request_form = initialize_installation_request_form(request)
    location_detail_extra_form = initialize_location_detail_extra_form(request)
    admin_user_form = initialize_user_form(request, person="admin_")
    admin_profile_form = initialize_simple_profile_form(
        request, person="admin_")
    installer_user_form = initialize_user_form(request, person="installer_")
    installer_profile_form = initialize_simple_profile_form(
        request, person="installer_"
    )
    check_sum_form = CheckSumForm()
    request = get_calculation_string(request)

    """process tab 'object'"""
    if request.method == "POST" and "object" in request.POST:
        request, messages = project_request_object(
            request=request, messages=messages)

    """process tab 'contact'"""
    if request.method == "POST" and "contact" in request.POST:
        request, messages = contact(request=request, messages=messages)

    """process tab 'request'"""
    if request.method == "POST" and "request" in request.POST:
        request, messages = installation_request(
            request=request, messages=messages)

    """process tab 'details'"""
    if request.method == "POST" and "details" in request.POST:
        request, messages = location_detail_request(
            request=request, messages=messages)

    """process tab 'contact'"""
    if request.method == "POST" and "additional" in request.POST:
        request, messages = additional_contact(
            request=request, messages=messages)

    context = {
        "messages": messages,
        "next_tab": request.session["tab"],
        "location_detail_form": location_detail_form,
        "address_form": address_form,
        "installation_request_form": installation_request_form,
        "location_detail_extra_form": location_detail_extra_form,
        "user_form": user_form,
        "profile_form": profile_form,
        "admin_user_form": admin_user_form,
        "admin_profile_form": admin_profile_form,
        "installer_user_form": installer_user_form,
        "installer_profile_form": installer_profile_form,
        "check_sum_form": check_sum_form,
        "calculation_string": request.session.get("calculation_string", None),
    }

    return render(request, "project_request/create_project_request.html", context)
