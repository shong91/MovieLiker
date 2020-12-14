from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.utils.translation import ugettext_lazy as _


# Custom manager of User model - has the helper methods (in addition to the methods provided by BaseUserManager)
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set. ')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # password=None means that None is default value for password, but it could still be provided by caller
    # When you don't provide password for new user or you pass None for password Django will create user with unusable password,
    # that means, user won't be able to log in with username and password.

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


# customized User class
class User(AbstractBaseUser, PermissionsMixin):
    """
      customized User (superclass: AbstractBaseUser)
      1) not need to created 'password' column
      2) username field(id) will be replaced with email field as below. you need to mention 'USERNAME_FIELD = 'email')
    """
    username = models.CharField(max_length=30)
    email = models.EmailField(verbose_name=_('email_id'),
                              max_length=64,
                              unique=True,
                              help_text='EMAIL ID: ')

    # groups = models.ForeignKey(Group)

    is_staff = models.BooleanField(verbose_name=_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin site.')
                                   )
    is_superuser = models.BooleanField(verbose_name=_('superuser status'),
                                       default=False,
                                       help_text=_('Designates whether the user is superuser')
                                       )
    is_active = models.BooleanField(verbose_name=_('active'),
                                    default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.')
                                    )
    created_at = models.DateTimeField(verbose_name=_('date joined'),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('date updated'),
                                      auto_now=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    # verbose_name: 사용자가 읽기 쉬운 모델 객체의 이름으로 관리자 화면 등에서 표시된다. 영어를 기준으로 단수형이다.
    #               옵션을 지정하지 않으면 CamelCase 클래스 이름을 기준으로 camel case 이와 같이 모두 소문자로 변경한다.
    # verbose_name_plural: 사용자가 읽기 쉬운 모델 객체의 이름으로 관리자 화면 등에서 표시된다. 영어를 기준으로 복수형이다. (한국어에서는 굳이 단수와 복수를 구별해 사용하지 않으므로 verbose_name과 동일하게 쓸 수 있다.
    #                      옵션을 지정하지 않으면 verbose_name에 s를 붙인다.

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # = java .tostring() ?
    def __str__(self):
        return self.username

    # Returns the first_name.
    def get_short_name(self):
        return self.email
