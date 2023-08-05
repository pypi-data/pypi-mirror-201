/*
 * This file is generated by objective.metadata
 *
 * Last update: Fri May 15 15:22:17 2015
 */

static void __attribute__((__used__)) use_protocols(void)
{
    PyObject* p __attribute__((__unused__));
#if PyObjC_BUILD_RELEASE >= 1010

#if defined(MAC_OS_X_VERSION_10_6)                                                       \
    && MAC_OS_X_VERSION_MIN_REQUIRED >= MAC_OS_X_VERSION_10_6
    /* Looks like a bug in the 10.11 SDK, these definitions aren't available unless
     * the deployment target is 10.6 or later.
     */
    p = PyObjC_IdToPython(@protocol(IKCameraDeviceViewDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(IKDeviceBrowserViewDelegate));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(IKScannerDeviceViewDelegate));
    Py_XDECREF(p);
#endif
    p = PyObjC_IdToPython(@protocol(IKFilterCustomUIProvider));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(IKImageEditPanelDataSource));
    Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(IKSlideshowDataSource));
    Py_XDECREF(p);
#endif /* PyObjC_BUILD_RELEASE >= 1010 */
}
