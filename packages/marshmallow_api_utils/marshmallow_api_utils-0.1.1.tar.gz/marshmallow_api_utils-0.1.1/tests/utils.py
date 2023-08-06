import re


def minify_string(value: str, minify_comma=False):
    '''
        Minify string
        " { hello    world,   foobar  } " => "{hello world, foobar}"
    '''
    # Minify all whitespace to a single space.
    # e.g.: "hello      world" => "hello world"
    minified_str = re.sub(r'[\s]+', ' ', value)
    # Remove all spaces around brackets
    # e.g.: "{ hello world }" => "{hello world}"
    minified_str = re.sub(r' ?([\{\}\[\]\(\)]) ?', r'\g<1>', minified_str)

    # Remove leading and trailing whitespace
    minified_str = minified_str.strip()

    if minify_comma:
        minified_str = minified_str.replace(', ', ',')

    return minified_str


def assert_string_minified(
    actual: str,
    expected: str,
    minify_comma: bool = True,
    message: str = None,
):
    '''
        Asserts that strings are identical, and ignore whitespace differences.
        This is very useful for comparing generated queries for example, where you
        might want to have a human readable version in your test file.

        Args:
            actual (str):           Actual string to compare against expected.
            expected (str):         The string we expect actual to be equal to.
            minify_comma (bool):    Should we minify commas? e.g.: 'a, b' -> 'a,b'
    '''
    actual = minify_string(actual, minify_comma=minify_comma)
    expected = minify_string(expected, minify_comma=minify_comma)

    if message:
        assert actual == expected, message
    else:
        assert actual == expected
