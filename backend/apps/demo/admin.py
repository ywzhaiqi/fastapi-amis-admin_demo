import time
from fastapi import Request
from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp
from core.adminsite import site

# from .models import Category

@site.register_admin
class DemoApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Demo', icon='fa fa-bolt')
    router_prefix = '/demo'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # self.register_admin(CategoryAdmin)
        self.register_admin(HelloWorldPageAdmin, CurrentTimePageAdmin, AmisPageAdmin, GitHubLinkAdmin, ReDocsAdmin)


# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     page_schema = amis.PageSchema(label='Category', icon='fa fa-folder')
#     model = Category
#     search_fields = [Category.name]


class HelloWorldPageAdmin(admin.PageAdmin):
    page_schema = 'Hello World Page'
    # 通过page类属性直接配置页面信息;
    page = amis.Page(title='标题', body='Hello World!')


class CurrentTimePageAdmin(admin.PageAdmin):
    page_schema = 'Current Time Page'

    # 通过get_page类方法实现动态获取页面信息.
    async def get_page(self, request: Request) -> amis.Page:
        page = await super().get_page(request)
        page.body = '当前时间是: ' + time.strftime('%Y-%m-%d %H:%M:%S')
        return page


class AmisPageAdmin(admin.PageAdmin):
    page_schema = 'Amis Json Page'
    page = amis.Page.parse_obj(
        {
            "type": "page",
            "title": "表单页面",
            "body": {
                "type": "form",
                "mode": "horizontal",
                "api": "/saveForm",
                "body": [
                    {
                        "label": "Name",
                        "type": "input-text",
                        "name": "name"
                    },
                    {
                        "label": "Email",
                        "type": "input-email",
                        "name": "email"
                    }
                ]
            }
        }
    )


class GitHubLinkAdmin(admin.LinkAdmin):
    # 通过page_schema类属性设置页面菜单信息;
    # PageSchema组件支持属性参考: https://baidu.gitee.io/amis/zh-CN/components/app
    page_schema = amis.PageSchema(label='AmisLinkAdmin', icon='fa fa-github')
    # 设置跳转链接
    link = 'https://github.com/amisadmin/fastapi_amis_admin'


class ReDocsAdmin(admin.IframeAdmin):
    # 设置页面菜单信息
    page_schema = amis.PageSchema(label='Redocs', icon='fa fa-book')

    # 设置跳转链接
    @property
    def src(self):
        return self.app.site.settings.site_url + '/redoc'