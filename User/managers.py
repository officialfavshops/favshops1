from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self,mobile_number,password,is_staff,is_superuser,**extra_fields):

        if not mobile_number:
            raise ValueError('The given mobilif not mobile_number must be set')

        #email = self.normalize_email(email)
        user = self.model(mobile_number=mobile_number,is_staff=is_staff,is_active=True,is_superuser=is_superuser,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_user(self,mobile_number,password=None,**extra_fields):
        return self._create_user(mobile_number,password,False,False,**extra_fields)

    def create_superuser(self,mobile_number,password,**extra_fields):
        return self._create_user(mobile_number,password,True,True,**extra_fields)
