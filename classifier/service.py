import hashlib


def generate_service_id(service_name, host, port):
    """Create the service id for consul
    :param str service_name: the service name
    :param str host: the service address
    :param int port: the port on which the service listens to
    :rtype: str
    :return: the service id
    """
    service_info = "{}-{}-{}".format(service_name, host, port).encode("utf-8")

    return "{}".format(hashlib.md5(service_info).hexdigest())
