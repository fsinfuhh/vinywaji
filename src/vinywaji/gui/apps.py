from django.apps import AppConfig

class GuiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vinywaji.gui"
    label = "vinywaji_gui"

class ThemeConfig(AppConfig):
    name = 'vinywaji.gui'