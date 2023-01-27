from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    # delete this
    path('administrator/', admin.site.urls),
    path("admin/",views.loginPage,name="login-page"),
    # path("home/",views.home,name="home"),
    path("",views.home,name="home"),
    path("logout-page/",views.logoutPage,name="logout-page"),
    path('recover-log/',views.recoverLog,name="recover-log"),
    path('recover-validation',views.recoverValidation,name="recover-validation"),
    path("send-otp/<str:name>",views.sendOtp,name="send-otp"),
    path("validate-pass-otp",views.validatePassOtp,name="validate-pass-otp"),
    path("code-checker",views.codeChecker,name="code-checker"),
    path("update-pass/<str:name>",views.updatePass,name="update-pass"),
    path("login-verify/",views.loginVerify,name="login-verify"),
    path("authenticator/",views.authenticator,name="authenticator"),
    path("token-validator/",views.tokenValidator,name="token-validator"),
    path("cancel-auth",views.cancelAuth,name="cancel-auth")
]