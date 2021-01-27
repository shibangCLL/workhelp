from import_export import resources

from jietu.models import Doamin


class DoaminResource(resources.ModelResource):

    class Meta:
        model = Doamin
        import_id_fields = ['name', 'expiration_date', 'domaintype']  # 这里决定了update_or_create，可以避免重复导入
