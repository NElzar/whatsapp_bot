from django.db import models


class Script(models.Model):
    title = models.CharField(max_length=64)
    steps = models.ManyToManyField('bot.Step', related_name='script')

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text


class Step(models.Model):
    next = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return self.text


class Result(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE, null=True)
    user_phone = models.CharField(max_length=24)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return self.script.title

