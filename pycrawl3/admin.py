from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Email, Seed
from import_export import resources


class EmailResource(resources.ModelResource):
    class Meta:
        model = Email


class SeedResource(resources.ModelResource):
    class Meta:
        model = Seed
        import_id_fields = ('url',)

# temporary admin class until https://github.com/django-import-export/django-import-export/issues/797 is resolved!
class PycrawlAdmin(ImportExportModelAdmin):

    def get_export_queryset(self, request):
        """
        Returns export queryset.
        Default implementation respects applied search and filters.
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        if self.get_actions(request):
            list_display = ['action_checkbox'] + list(list_display)

        ChangeList = self.get_changelist(request)
        cl = ChangeList(request, self.model, list_display,
                        list_display_links, list_filter, self.date_hierarchy,
                        search_fields, self.list_select_related, self.list_per_page,
                        self.list_max_show_all, self.list_editable, self, None
                        )

        return cl.get_queryset(request)


@admin.register(Email)
class EmailAdmin(PycrawlAdmin):
    resource_class = EmailResource


@admin.register(Seed)
class SeedAdmin(PycrawlAdmin):
    resource_class = SeedResource


