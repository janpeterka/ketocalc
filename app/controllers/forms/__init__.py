# This is needed for ExtendedFlaskView to automatically import all Form classes

from .diets import DietsForm  # noqa: F401
from .feedback import FeedbackForm  # noqa: F401
from .ingredients import IngredientsForm  # noqa: F401
from .login import LoginForm  # noqa: F401
from .password_recovery import NewPasswordForm  # noqa: F401
from .password_recovery import GetNewPasswordForm  # noqa: F401
from .register import RegisterForm  # noqa: F401
from .users import UserForm  # noqa: F401
from .users import PasswordForm  # noqa: F401
