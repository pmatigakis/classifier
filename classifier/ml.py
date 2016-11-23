import logging

from classifier import reqparsers


logger = logging.getLogger(__name__)


def extract_text_data():
    args = reqparsers.classifier_data.parse_args()
    return [args.data]
