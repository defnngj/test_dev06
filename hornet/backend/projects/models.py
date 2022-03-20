from django.db import models


# Create your models here.
class Project(models.Model):
    """
    项目管理表
    """
    name = models.CharField("名称", max_length=50, null=False)
    describe = models.TextField("描述", null=True, default="")
    is_delete = models.BooleanField("状态", null=True, default=False)
    image = models.CharField("图片", max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
