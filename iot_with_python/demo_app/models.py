from django.db import models


class ActionDevice(models.Model):
    name = models.CharField(
        max_length=255,
    )

    topic = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f'{self.name} ({self.topic})'


class ConsumerDevice(models.Model):
    name = models.CharField(
        max_length=255,
    )

    topic = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f'{self.name}: {self.topic}'


class Action(models.Model):
    action_device = models.ForeignKey(
        ActionDevice,
        on_delete=models.CASCADE,
    )

    consumer_devices = models.ManyToManyField(
        to=ConsumerDevice,
    )

    payload = models.JSONField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.action_device.name} => {", ".join(x.name for x in self.consumer_devices.all())}'


class ActionCondition(models.Model):
    EQ_OPERATION = 'eq'
    NE_OPERATION = 'ne'
    LT_OPERATION = 'lt'
    LE_OPERATION = 'le'
    GT_OPERATION = 'gt'
    GE_OPERATION = 'ge'

    OPERATIONS = (
        (EQ_OPERATION, EQ_OPERATION),
        (NE_OPERATION, NE_OPERATION),
        (LT_OPERATION, LT_OPERATION),
        (LE_OPERATION, LE_OPERATION),
        (GT_OPERATION, GT_OPERATION),
        (GE_OPERATION, GE_OPERATION),
    )

    VALUE_TYPE_NUMBER = 'number'
    VALUE_TYPE_STRING = 'string'
    VALUE_TYPE_BOOLEAN = 'boolean'

    VALUE_TYPES = (
        (VALUE_TYPE_STRING, VALUE_TYPE_STRING),
        (VALUE_TYPE_NUMBER, VALUE_TYPE_NUMBER),
        (VALUE_TYPE_BOOLEAN, VALUE_TYPE_BOOLEAN),
    )

    name = models.CharField(
        max_length=255,
    )

    payload_key = models.CharField(
        max_length=30,
    )

    value = models.CharField(
        max_length=255,
    )

    value_type = models.CharField(
        max_length=max(len(x) for x, _ in VALUE_TYPES),
        choices=VALUE_TYPES,
    )

    operation = models.CharField(
        max_length=max(len(x) for x, _ in OPERATIONS),
        choices=OPERATIONS,
    )

    payload = models.JSONField()

    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
    )
