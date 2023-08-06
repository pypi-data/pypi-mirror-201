def bytes_to_str(src, encoding='utf-8'):
    """
    字节流转化为字符串
    :param src:
    :param encoding:
    :return:
    """
    return src.decode(encoding=encoding) if isinstance(src, bytes) else src


def str_to_bytes(src, encoding='utf-8'):
    """
    字符串转字节流
    :param src:
    :param encoding:
    :return:
    """

    return src if isinstance(src, bytes) else src.encode(encoding=encoding)
