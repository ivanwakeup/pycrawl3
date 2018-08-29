from import_export import resources
from pycrawl3.models import Email, Seed


class EmailResource(resources.ModelResource):
    class Meta:
        model = Email


class SeedResource(resources.ModelResource):
    class Meta:
        model = Seed
        exclude = ('id',)
        import_id_fields = ['url']
