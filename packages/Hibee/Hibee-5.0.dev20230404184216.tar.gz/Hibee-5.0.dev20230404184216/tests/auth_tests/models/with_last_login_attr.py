from hibeecontrib.auth.base_user import AbstractBaseUser


class UserWithDisabledLastLoginField(AbstractBaseUser):
    last_login = None
