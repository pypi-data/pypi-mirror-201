from PyObjCTools.TestSupport import TestCase, min_sdk_level
import WebKit


class TestWebPolicyDelegate(TestCase):
    def test_enum_types(self):
        self.assertIsEnumType(WebKit.WebNavigationType)

    def testConstants(self):
        self.assertIsInstance(WebKit.WebActionNavigationTypeKey, str)
        self.assertIsInstance(WebKit.WebActionElementKey, str)
        self.assertIsInstance(WebKit.WebActionButtonKey, str)
        self.assertIsInstance(WebKit.WebActionModifierFlagsKey, str)
        self.assertIsInstance(WebKit.WebActionOriginalURLKey, str)

        self.assertEqual(WebKit.WebNavigationTypeLinkClicked, 0)
        self.assertEqual(WebKit.WebNavigationTypeFormSubmitted, 1)
        self.assertEqual(WebKit.WebNavigationTypeBackForward, 2)
        self.assertEqual(WebKit.WebNavigationTypeReload, 3)
        self.assertEqual(WebKit.WebNavigationTypeFormResubmitted, 4)
        self.assertEqual(WebKit.WebNavigationTypeOther, 5)

    def testProtocols(self):
        self.assertProtocolExists("WebPolicyDecisionListener")

    @min_sdk_level("10.11")
    def testProtocols10_11(self):
        self.assertProtocolExists("WebPolicyDelegate")
