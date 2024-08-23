from django.apps import AppConfig

class FaceidConfig(AppConfig):
    """
    Configuration class for the 'faceid' application.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key field 
                                  used for models in the application.
        name (str): The name of the application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "faceid"
