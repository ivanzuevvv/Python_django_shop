import sys
from django.apps import AppConfig
from .utils import SettingFileLoader
from project_aggregator import settings


class AppConfigurationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_configurations'
    verbose_name = 'Настройки сайта'

    def ready(self):
        SiteSettings = self.get_model('SiteSettings')
        if ('makemigrations' not in sys.argv) and ('migrate' not in sys.argv):
            setting_conf = SettingFileLoader(settings.APP_SETTINGS_PATH)
            SiteSettings.objects.get_or_create(**setting_conf.config)
