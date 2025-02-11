from enums.custom import DocumentKind, FileType
from loguru import logger
from mail_app.models import PDF

pdf_context_requirements = {
    "template": "invoice.html",
    "context_parameters": [
        "invoice",
    ],
}

template_path = "pdf/invoice.html"
css_path = "ChargePointHandler/assets/css/invoice.css"


def generate_invoice_user(user, file_name, context):
    logger.debug("Create Invoice-PDF")

    # return pdf_generator.create_file_response(pdf_context, attach=False, save=False)
    pdf_model = PDF(
        user=user,
        file_type=FileType.pdf.value,
        document_kind=DocumentKind.cdr_user,
        approved=False,
    )
    pdf_model.setup_pdf_generator(
        template_path,
        css_path,
        pdf_context_requirements,
        save=True,
        file_name=file_name
    )
    pdf = pdf_model.create_file(context)
    return pdf_model.create_file_response(pdf, attach=True)
