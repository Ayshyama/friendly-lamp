from ChargePointHandler.models import User
from ChargePointHandler.storage_backend import MediaStorage
from django.core.files.base import ContentFile
from django.db import models
from enums.custom import DocumentKind, FileType
from loguru import logger
from mail_app.file_generator.file_generator import PdfGenerator


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"{MediaStorage.location}/{instance.user.email}/{instance.document_kind}/{filename}"


class File(models.Model):
    class Meta:
        abstract = True

    file = models.FileField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    file_type = models.CharField(
        choices=FileType.choices,
        max_length=8,
        default=FileType.pdf.value,
        editable=False,
    )
    approved = models.BooleanField(default=False)
    document_kind = models.CharField(
        choices=DocumentKind.choices, max_length=32, default=DocumentKind.invoice.value
    )
    created = models.DateTimeField(auto_now_add=True)
    red = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name


class CSV(File):
    file_type = models.CharField(
        choices=FileType.choices,
        max_length=8,
        default=FileType.csv.value,
        editable=False,
    )
    document_kind = models.CharField(
        choices=DocumentKind.choices, max_length=32, default=DocumentKind.cdr_user
    )
    activated = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)


class PDF(File):
    pdf_generator = None

    def setup_pdf_generator(
        self, template_path, css_path, crs, save=True, file_name="unknown"
    ):
        self.pdf_generator = PdfGenerator(
            self.user,
            template_path,
            css_path,
            context_requirements=crs,
            save=save,
            file_path=user_directory_path(
                self, f"{file_name}.{self.file_type}"),
        )

    def create_file(self, context):
        pdf_file = self.pdf_generator.create_file_in_storage(
            context=context, save=False
        )
        self.file.save(
            self.pdf_generator.get_file_name(), ContentFile(pdf_file), save=True
        )
        return pdf_file

    def create_file_response(self, file, attach):
        return self.pdf_generator.create_file_response(file, attach)
