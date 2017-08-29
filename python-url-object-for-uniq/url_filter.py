'''
针对sql注入的url去重方法
'''

from urllib.parse import ParseResult, parse_qsl, urlencode
from urllib.parse import (
    urlparse as _urlparse,
    urlunsplit as _urlunsplit
)


def dict_key_equal(dict1, dict2):
    '''对两个字典的对比，只对比key是否相同'''
    return not bool(set(dict1.keys()).difference(set(dict2.keys())))


class URL(ParseResult):

    def __eq__(self, other):
        '''对两个URL对象的比较，GET请求只匹配参数。其他的因素全匹配。'''
        if isinstance(other, self.__class__):
            _str_key_lst = ("scheme", "netloc", "path", "params", "fragment")
            _dict_key_lst = ("query",)
            for key in _str_key_lst:
                if getattr(self ,key) != getattr(other ,key):
                    return False
            for key in _dict_key_lst:
                if not dict_key_equal(
                    getattr(self ,key), getattr(other ,key)
                ):
                    return False
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        _lst = list(tuple(self))
        _lst[4] = tuple(sorted(_lst[4].keys()))
        return hash(tuple(_lst))


def urlparse(url, scheme='', allow_fragments=True):
    _presult = _urlparse(
        url, scheme=scheme, allow_fragments=allow_fragments
    )
    _lst = list(_presult)
    _lst[4] = dict(parse_qsl(_lst[4]))
    return URL(*_lst)


def urlunsplit(components):
    _lst = list(components)
    _lst[4] = urlencode(_lst[4])
    return ParseResult(*_lst).geturl()


def test_url_object_equal():
    origin_url = urlparse("http://example.com/x?a=1&b=2")
    for url in (
        urlparse("http://example.com/x?a=1&b=2"),
        urlparse("http://example.com/x?a=1&b=3"),
        urlparse("http://example.com/x?a=2&b=3")
    ):
        assert (origin_url == url) is True
        assert (origin_url != url) is False
        assert len(set((origin_url, url))) is 1

    for url in (
        urlparse("http://example.com/x?a=2&c=3"),
        urlparse("http://aaaa.com/x?a=1&b=2")
    ):
        assert (origin_url == url) is False
        assert (origin_url != url) is True
        assert len(set((origin_url, url))) is 2


if __name__ == '__main__':
    test_url_object_equal()
    print("[*] all tests passed!")
