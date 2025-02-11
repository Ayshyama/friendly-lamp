from django import forms
from django.forms import TextInput
from project_management.models.models import (InstallationRequest, LocationDetail,
                                              Milestone, ParkingSpace, Item, ProjectCalculation)


class LocationDetailForm(forms.ModelForm):
    class Meta:
        model = LocationDetail
        exclude = ["location"]
        labels = {
            "location_stage": "Status der Immobilie",
            "name": "Name der Immobilie (optional)",
            "parking_spaces": "Anzahl aller Stellplätze",
            "existing_charging_stations": "Ladestationen vorhanden",
            "parking_space_types": "Art der Stellplätze (Mehrfachauswahl)",
        }
        widgets = {
            "location_stage": forms.Select(attrs={"class": "form-control"}),
            "name": TextInput(
                attrs={"placeholder": "Neuländer Quarrée",
                       "class": "form-control"}
            ),
            "parking_spaces": TextInput(
                attrs={"placeholder": "50", "class": "form-control"}
            ),
            "parking_space_types": forms.CheckboxSelectMultiple(
                attrs={"class": "form-control"}
            ),
        }


class LocationDetailExtrasForm(forms.ModelForm):
    class Meta:
        model = LocationDetail
        fields = [
            "user_group",
            "particularities",
            "spare_capacity",
            "requested_capacity",
            "number_net_connections",
        ]
        labels = {
            "user_group": "Wer nutzt die Ladestationen?",
            "particularities": "Besonderheiten zum Objekt und Wünsche",
            "spare_capacity": "freie Kapazität [KW]",
            "requested_capacity": "angefragte Kapazität [kW]",
            "number_net_connections": "Anzahl der Netzanschlüsse",
        }
        widgets = {
            "user_group": forms.Textarea(
                attrs={
                    "rows": "5",
                    "placeholder": "Die Mieter und Eigentümer des Hauses sowie deren privater Besuch",
                    "class": "form-control",
                }
            ),
            "particularities": forms.Textarea(
                attrs={
                    "rows": "5",
                    "placeholder": "Wir wünschen Ladestationen mit Ladekabel und Kabelhalterung\nEs gibt folgende große elektrischen Verbraucher:\n2 Klimaanlagen\n1 elektrische Heizung",
                    "class": "form-control",
                }
            ),
            "spare_capacity": TextInput(
                attrs={"placeholder": "20", "class": "form-control"}
            ),
            "requested_capacity": TextInput(
                attrs={"placeholder": "0", "class": "form-control"}
            ),
            "number_net_connections": TextInput(
                attrs={"placeholder": "1", "class": "form-control"}
            ),
        }


class InstallationRequestForm(forms.ModelForm):
    class Meta:
        model = InstallationRequest
        exclude = ["location_detail", "basic_installation"]
        labels = {
            # "basic_installations": "Grundinstallationen",
            "prepared_parking_spaces": "So viele Stellplätze sollen vorgerüstet werden",
            "charging_stations": "Davon erhalten so viele eine Ladestation",
        }
        widgets = {
            "prepared_parking_spaces": TextInput(
                attrs={"placeholder": 20, "class": "form-control"}
            ),
            "charging_stations": TextInput(
                attrs={"placeholder": 10, "class": "form-control"}
            ),
        }


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        exclude = ["location_details"]
        labels = {
            "target_date": "Zieldatum",
            "name": "Titel",
            "description": "Beschreibung",
            "created": "erstellt am",
        }


class LocationDocument(forms.ModelForm):
    class Meta:
        model = InstallationRequest
        exclude = ["location_details"]
        labels = {
            "name": "Dokumententitel",
            "document": "Dokument",
        }


class ParkingSpace(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        exclude = ["location_details"]
        labels = {
            "owner": "Eigentümer",
            "number": "Stellplatz-Nr.",
            "position": "InvoiceItem",
            "installation_stage": "Installationsstufe",
            "parking_space_type": "Parkplatz-Typ",
            "charging_station": "Ladestation",
        }


class DateInput(forms.DateInput):
    input_type = "date"


class ProjectCalculationForm(forms.ModelForm):
    class Meta:
        model = ProjectCalculation
        fields = ["execution_date"]
        widgets = {
            "execution_date": DateInput(attrs={"class": "form-control", "input_formats": ["%Y-%m-%d"]}),
        }
