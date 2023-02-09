from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from .models import SiteSettings
from .serializer import SiteSettingsSerializer


class SettingsView(ListModelMixin, GenericAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    def get(self, request):
        return self.list(request)
