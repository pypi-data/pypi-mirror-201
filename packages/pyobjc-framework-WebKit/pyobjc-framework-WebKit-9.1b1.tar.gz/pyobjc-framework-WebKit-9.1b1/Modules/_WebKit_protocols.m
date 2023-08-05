/*
 * This file is generated by objective.metadata
 *
 * Last update: Sun Dec 28 14:22:11 2014
 */

#if PyObjC_BUILD_RELEASE >= 1016
#import <WebKit/WKScriptMessageHandlerWithReply.h>
#endif

static void __attribute__((__used__)) use_protocols(void)
{
    PyObject* p __attribute__((__unused__));
#if PyObjC_BUILD_RELEASE >= 1011
    p = PyObjC_IdToPython(@protocol(WebUIDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebResourceLoadDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebPolicyDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebEditingDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebDownloadDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebFrameLoadDelegate));
    Py_XDECREF(p);
#endif /* PyObjC_BUILD_RELEASE >= 1011 */
    p = PyObjC_IdToPython(@protocol(DOMEventListener));
    Py_XDECREF(p);
#if PyObjC_BUILD_RELEASE >= 1010
    p = PyObjC_IdToPython(@protocol(DOMEventTarget));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(DOMNodeFilter));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(DOMXPathNSResolver));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebDocumentRepresentation));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebDocumentSearching));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebDocumentText));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebDocumentView));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebOpenPanelResultListener));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WebPolicyDecisionListener));
    Py_XDECREF(p);
#endif /* PyObjC_BUILD_RELEASE >= 1010 */
    p = PyObjC_IdToPython(@protocol(WebPlugInViewFactory));
    Py_XDECREF(p);
#if PyObjC_BUILD_RELEASE >= 1010
    p = PyObjC_IdToPython(@protocol(WKNavigationDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WKScriptMessageHandler));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WKUIDelegate));
    Py_XDECREF(p);
#endif /* PyObjC_BUILD_RELEASE >= 1010 */
#if PyObjC_BUILD_RELEASE >= 1013
#if WK_API_ENABLED
    p = PyObjC_IdToPython(@protocol(WKHTTPCookieStoreObserver));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WKURLSchemeTask));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(WKURLSchemeHandler));
    Py_XDECREF(p);
#endif
#endif
#if PyObjC_BUILD_RELEASE >= 1016
    p = PyObjC_IdToPython(@protocol(WKScriptMessageHandlerWithReply));
    Py_XDECREF(p);
#endif
#if PyObjC_BUILD_RELEASE >= 1103
    p = PyObjC_IdToPython(@protocol(WKDownloadDelegate));
    Py_XDECREF(p);
#endif
}
