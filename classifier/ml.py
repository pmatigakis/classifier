import logging

from classifier import reqparsers


logger = logging.getLogger(__name__)


def extract_page_contents():
    args = reqparsers.classification_request.parse_args()
    return args.content


def page_classification_result_processor(result):
    return {"categories": result}
