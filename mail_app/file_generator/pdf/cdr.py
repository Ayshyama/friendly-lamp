from enums.custom import DocumentKind, FileType
from loguru import logger
from mail_app.models import PDF

pdf_crs = {
    "template": "cdr_user.html",
    "context_parameters": [
        # basic data
        "operator_company",
        "operator_address",
        "customer_name",
        "customer_address",
        "customer_id",
        "date_of_creation",
        "intro_text",
        # filter parameter
        "start_date",
        "end_date",
        # 'chargepoints',
        "id_tag_list",
        "user_list",
        # transactions
        "cdr_transactions",
        "cdr_sum",
        "transaction_sum",
    ],
}

template_path = "pdf/cdr_user.html"
css_path = "ChargePointHandler/assets/css/invoice.css"


def generate_cdr_user(user, file_name, context):
    logger.debug("Create CDR-PDF")

    # return pdf_generator.create_file_response(pdf_context, attach=False, save=False)
    pdf_model = PDF(
        user=user,
        file_type=FileType.pdf.value,
        document_kind=DocumentKind.cdr_user,
    )
    pdf_model.setup_pdf_generator(
        template_path, css_path, pdf_crs, save=True, file_name=file_name
    )
    pdf = pdf_model.create_file(context)
    return pdf_model.create_file_response(pdf, attach=True)
