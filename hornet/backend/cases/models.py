from django.db import models
from projects.models import Project


class Module(models.Model):
    """
    模块(节点)表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, null=False, default="")
    parent_id = models.IntegerField("父级ID", default=0)
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    """
    测试用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    url = models.TextField("URL", null=False)
    method = models.CharField("请求方法", max_length=10, null=False)  # GET/POST/DELETE/PUT
    header = models.TextField("请求头", null=True, default="{}")
    params_type = models.CharField("参数类型", max_length=10, null=False)  # GET: params POST: form/json
    params_body = models.TextField("参数内容", null=True, default="{}")
    response = models.TextField("响应", null=True, default="{}")
    assert_type = models.CharField("断言类型", max_length=10, null=True)  # include/equal
    assert_text = models.TextField("断言结果", null=True, default="{}")
    is_delete = models.BooleanField("状态", default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name


class TestExtract(models.Model):
    """
    测试提取器
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    case_id = models.IntegerField("用例ID", null=False, default=0)
    name = models.CharField("名称", max_length=50, null=False)
    extract = models.CharField("提取规则", max_length=200, null=False)
    vlue = models.CharField("提取值", max_length=200, null=True, default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name




