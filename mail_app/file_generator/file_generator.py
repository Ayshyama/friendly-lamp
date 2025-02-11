import datetime

from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from enums.custom import FileType
from loguru import logger
from storages.backends.s3boto3 import S3Boto3Storage
from weasyprint import CSS, HTML

from Central_System.settings.base import STATIC_ROOT

""" Genergate documents such as pdf and csv-files

csv + pdf:
- table of CDRs with price information without any basic fees per user [CDR x CDR-Data]
- aggregated CDRs per location including basic fees [user x cost-types]

pdf:
- offer and invoice (one-time, recurring) [grouped positions x Product-Data]
- SEPA-form

"""

context_requirements_1 = [
    {
        "template": "invoice",
        "context_parameters": ["from_address", "from_"],
    }
]

# css_path ='ChargePointHandler/assets/css/invoice.css'
# template_path = 'pdf_templates/invoice.html'


class MediaStorage(S3Boto3Storage):
    bucket_name = "chargetic-storage"
    location = "media"
    file_overwrite = False
    AWS_DEFAUT_ACL = "public-read"


class FileGenerator:
    def __init__(
        self, user, context_requirements, save=False, file_path="", *args, **kwargs
    ):
        self.user = user
        self.save = save
        self.file_type = FileType.pdf.value
        self.__set_file_path(file_path)  # file_path
        self.__set_file_name()  # file_name
        self.__set_context_requirements(
            context_requirements)  # context_requirements

    def __set_context_requirements(self, context_requirements):
        if isinstance(context_requirements, list):
            if not isinstance(context_requirements[0], dict):
                raise TypeError
            else:
                self.context_requirements = context_requirements
        else:
            if not isinstance(context_requirements, dict):
                raise TypeError
            else:
                self.context_requirements = [context_requirements]

    def __set_file_path(self, file_path):
        main_dir = file_path.split("/")[0]
        logger.warning(main_dir)
        logger.warning(MediaStorage.location)

        if main_dir == MediaStorage.location:
            file_path = file_path.replace(f"{MediaStorage.location}/", "")
            logger.warning(file_path)

        if file_path[-1] == "/":
            raise ValueError

        file_type = file_path.split(".")[-1]
        if file_type == self.file_type:
            self.file_path = file_path
        else:
            if file_type == "":
                self.file_path = f"{file_path}.{self.file_type}"
            else:
                self.file_path = file_path.replace(file_type, self.file_type)
        logger.warning(self.file_path)

    def __set_file_name(self):
        filename = self.file_path.split("/")[-1]
        if filename != "" and "." in filename:
            self.file_name = filename
        else:
            self.file_name = "untitled_file"

    def __get_specific_context_requirements(self):
        return self.context_requirements[0]

    def validate_context_requirements(self, context, crs):
        if not isinstance(context, dict):
            raise TypeError
        if crs == {}:
            return True

        fulfills = True
        context_parameter = list(context.keys())
        for cr in crs.get("context_parameters", []):
            if not cr in context_parameter:
                logger.warning(f"{cr} not in given context")
                fulfills = False
                break
        return fulfills

    def get_file_name(self):
        media_storage = MediaStorage()
        logger.warning(self.file_path)
        if media_storage.exists(self.file_path):
            now = datetime.datetime.now().strftime("%y.%m.%d_%H.%M")
            logger.warning(now)
            new_file_name = self.file_name.replace(
                f".{self.file_type}", f"_{now}.{self.file_type}"
            )
            logger.warning(new_file_name)
            return new_file_name
        else:
            return self.file_name

    def save_file(self, file):
        if self.save:
            media_storage = MediaStorage()
            file_path = self.file_path.replace(
                self.file_name, self.get_file_name())

            with media_storage.open(file_path, "wb") as f:
                f.write(file)
            logger.debug("File saved to storage")

    def __generate_file(self, context):
        pass

    def create_file_in_storage(self, context, attach=False):
        pass

    def create_file_response(self, file, attach=False):
        pass


class PdfGenerator(FileGenerator):
    def __init__(
        self,
        user,
        template_path,
        css_path,
        context_requirements,
        save=False,
        file_path="",
        *args,
        **kwargs,
    ):

        self.__set_template_path(template_path)
        self.__set_css_path(css_path)
        self.__set_template_name()
        self.file_type = FileType.pdf.value

        if self.template_name.split(".")[-1] != "html":
            raise TypeError
        if file_path.split(".")[-1] != self.file_type:
            raise TypeError

        super().__init__(
            user=user,
            context_requirements=context_requirements,
            save=save,
            file_path=file_path,
            *args,
            **kwargs,
        )

    def __set_template_path(self, template_path):
        if not isinstance(template_path, str):
            raise TypeError
        self.template_path = template_path

    def __set_template_name(self):
        self.template_name = self.template_path.split("/")[-1]

    def __set_css_path(self, css_path):
        if not isinstance(css_path, str):
            raise TypeError
        if css_path.split(".")[-1] != "css":
            raise TypeError
        self.css_path = css_path

    def __get_specific_context_requirements(self):
        logger.debug(self.context_requirements)
        for cr in self.context_requirements:
            if cr.get("template") == self.template_name:
                return cr
        raise ValueError

    def __generate_file(self, context):

        if not self.validate_context_requirements(
            context, self.__get_specific_context_requirements()
        ):
            raise ValueError

        html_string = render_to_string(self.template_path, context)
        css = CSS(STATIC_ROOT + self.css_path)
        html = HTML(string=html_string)

        pdf = html.write_pdf(stylesheets=[css], presentational_hints=True)
        return pdf

    def create_file_in_storage(self, context, **kwargs):
        """
        pass save = False as kwarg to suppress the file to be saved
        """

        save = kwargs.get("save", True)
        file = self.__generate_file(context)
        if save:
            self.save_file(file)
        return file

    def create_file_response(self, file, attach=False):
        """
        attach: if the File is attached to the Response
        """

        content_disposition = (
            f"attachment; filename={self.file_name}"
            if attach
            else f"filename {self.file_name}"
        )
        response = HttpResponse(file, content_type="application/pdf")
        response["Content-Disposition"] = content_disposition
        response["Conten-Transfer-Encoding"] = "binary"

        return response
