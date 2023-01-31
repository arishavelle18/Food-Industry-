from unicodedata import name
from django.urls import path

from . import views
urlpatterns = [
    path("",views.menu,name="menu"),
    path("qr-code",views.qrCode,name="qr-code"),
    path("qr-validation",views.qrValidation,name="qr-validation"),
    path("add-employee",views.addEmployee,name="add-employee"),
    path("test",views.test,name="test"),
    path("test2",views.test2,name="test2"),
    path("get-attendance",views.getAttendance,name="get-attendance"),
    path("get-update",views.getUpdate,name="get-update"),
    path("view-attendance",views.viewAttendance,name="view-attendance"),
    path("scan-timeout",views.scanTimeout,name="scan-timeout"),
    path("timeout-validation",views.timeoutValidation,name="timeout-validation"),
    path("time-check",views.timeCheck,name="time-check"),
    path("breaktime-out",views.breaktimeOut,name="breaktime-out"),
    path("breaktime-in",views.breaktimeIn,name="breaktime-in"),
    path("breaktime-out-validation",views.breaktimeOutValidation,name="breaktime-out-validation"),
    path("breaktime-in-validation",views.breaktimeInValidation,name="breaktime-in-validation"),
    path("scanner",views.scanner,name="scanner"),
    path("scanner-validation",views.scannerValidation,name="scanner-validation"),
    path("scanner-inspect",views.scannerInspect,name="scanner-inspect"),
    path("scanner-get-update",views.scannerGetUpdate,name="scanner-get-update"),
    path("update-attendance",views.updateAttendance,name="update-attendance"),
    path("get-equipment",views.getEquipment,name="get-equipment")
]