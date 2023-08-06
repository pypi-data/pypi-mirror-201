from vripper.parser._common import parse


# @parser("")
def p(url, timeout):
    return parse(url, timeout, "//img")
