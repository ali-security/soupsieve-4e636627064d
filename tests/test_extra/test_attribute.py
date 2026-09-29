"""Test attribute selectors."""
from .. import util
import soupsieve as sv


class TestAttribute(util.TestCase):
    """Test attribute selectors."""

    MARKUP = """
    <div id="div">
    <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre id="pre">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    def test_attribute_not_equal_no_quotes(self):
        """Test attribute with value that does not equal specified value (no quotes)."""

        # No quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!=\\35]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_quotes(self):
        """Test attribute with value that does not equal specified value (quotes)."""

        # Quotes
        self.assert_selector(
            self.MARKUP,
            "body [id!='5']",
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_double_quotes(self):
        """Test attribute with value that does not equal specified value (double quotes)."""

        # Double quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!="5"]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def assert_syntax_error_no_timeout(self, pattern):
        """Assert that compiling the pattern fails for syntax error, not timeout error."""

        import signal

        if not hasattr(signal, 'SIGALRM'):
            # `SIGALRM` is not available on all platforms (Windows).
            with self.assertRaises(sv.SelectorSyntaxError):
                sv.compile(pattern)
            return

        def timeout_handler(signum, frame):
            raise TimeoutError

        previous = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(3)

        passed = False
        try:
            with self.assertRaises(sv.SelectorSyntaxError):
                sv.compile(pattern)
            passed = True
        except TimeoutError:
            pass
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous)
        self.assertTrue(passed)

    def test_bad_attribute_unclused(self):
        """Test bad attribute fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout('[a="' + ('x' * 300))

    def test_bad_attribute_unclosed_single_quote(self):
        """Test bad attribute with unclosed single quote fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout("[a='" + ('x' * 300))

    def test_bad_contains_unclosed(self):
        """Test bad `:-soup-contains()` value fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout(':-soup-contains("' + ('x' * 300))

    def test_bad_lang_unclosed(self):
        """Test bad `:lang()` value fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout(":lang('" + ('x' * 300))
