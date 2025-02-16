from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Board(Entity):
    name = models.CharField(max_length=255, null=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="boards_created", null=False)

    def add_status(self, name):
        status_exist = Status.objects.filter(board=self, name=name)

        if status_exist != None:
            return "Status already exists"
        
        status = Status(board=self, name=name)
        status.save()
        return ""


class Status(Entity):
    name = models.CharField(max_length=255, null=False)
    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name="status", null=False)


class Workflow(Entity):
    current_status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="current_workflows", null=False)
    next_status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="previous_workflows", null=False)


class Task(Entity):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks_created", null=False)
    current_status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="tasks", null=False)

    def add_comment(self, user, content):
        if not Comment.is_valid(content, user):
            return "Invalid comment."
        
        new_comment = Comment(creator=user, content=content, task=self)
        new_comment.save()
        return ""
    
    
    def change_field_value(self, field, value, user):
        field_value = FieldValue.objects.filter(task=self, field=field)

        if field_value is None:            
            field_value = FieldValue(task=self, field=field)

        history = ValueHistory(field_name=field.name, previous_value=field.value, next_value=value, user=user)
        field_value.value = value
        field_value.save()
        history.save()
        return ""

    
    def change_status(self, new_status, user):
        valid_workflow = Workflow.objects.filter(current_status=self.current_status, next_status=new_status)
        if valid_workflow is None:
            return "Unauthorized status change"
        
        history = ValueHistory(field_name="Status", previous_value=self.current_status.name, next_value=new_status.name, user=user)
        self.current_status = new_status
        self.save()
        history.save()
        return ""


class Comment(Entity):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments", null=False)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name="comments", null=False)
    content = models.CharField(max_length=500, null=False)


class Field(Entity):
    name = models.CharField(max_length=255, null=False)


class FieldValue(Entity):
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name="filed_fields", null=False)
    field = models.ForeignKey(Field, on_delete=models.PROTECT, related_name="filed_values", null=False)
    value = models.CharField(max_length=255, null=True)


class ValueHistory(Entity):
    field_name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="history", null=False)
    previous_value = models.CharField(max_length=255, null=False)
    next_value = models.CharField(max_length=255, null=False)
