from django.conf import settings
from django.views.generic import RedirectView, TemplateView

from unicef_security import config
from unicef_security.config import UNICEF_EMAIL


class UnauthorizedView(TemplateView):
    template_name = "unauthorized.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "unicef_user"
        ] = self.request.user.is_authenticated and self.request.user.email.endswith(
            UNICEF_EMAIL
        )
        return context


class UNICEFLogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        base_url = config.AZURE_LOGOUT_BASE_URL
        tenant_id = config.AZURE_TENANT_ID
        host = self.request.get_host()

        return (
            f"https://{base_url}/{tenant_id}/oauth2/v2.0/"
            f"logout?post_logout_redirect_uri={host}/{settings.LOGOUT_URL}"
        )
