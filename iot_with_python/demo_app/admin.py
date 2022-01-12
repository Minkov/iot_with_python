from django.contrib import admin

from iot_with_python.demo_app.models import ActionDevice, ConsumerDevice, ActionCondition, Action


@admin.register(ActionDevice)
class ConsumerDeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(ConsumerDevice)
class ActionableDeviceAdmin(admin.ModelAdmin):
    pass


class ActionConditionsInlineAdmin(admin.StackedInline):
    model = ActionCondition


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    inlines = (ActionConditionsInlineAdmin,)
