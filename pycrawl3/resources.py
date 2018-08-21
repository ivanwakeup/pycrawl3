from import_export import resources
from pycrawl3.models import Email


class EmailResource(resources.ModelResource):
    class Meta:
        model = Email