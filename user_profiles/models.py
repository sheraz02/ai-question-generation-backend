from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin



class TestSession(models.Model):
    DIFFICULTIES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sessionId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    topicsName = models.CharField(max_length=255, null=False, blank=False)
    noOfQuestions = models.IntegerField(default=10)
    difficultyLevel = models.CharField(max_length=15, choices=DIFFICULTIES)
    questionsSet = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.user.name}"