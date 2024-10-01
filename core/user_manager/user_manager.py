# user_manager/user_manager.py
from utils.debug_utils import debug_print


# Placeholder imports for future modules
# from .authentication import AuthenticationManager
# from .access_control import AccessControlManager
# from .account_creation import AccountCreationManager
# from .password_manager import PasswordManager

class UserManager:
    def __init__(self):
        # Initialize with a default user for now
        self.current_user = User(username="Shanta", is_authenticated=True)
        debug_print(f"Debug: Username is {self.current_user.username}")
        # Placeholder for future initialization of other managers
        # self.auth = AuthenticationManager()
        # self.access_control = AccessControlManager()
        # self.account_creation = AccountCreationManager()
        # self.password_manager = PasswordManager()

    def set_username(self, username):
        self.current_user.username = username

    # Placeholder methods for future implementation
    def login(self, username, password):
        # Implementation to come
        pass

    def logout(self, user_id):
        # Implementation to come
        pass

    def create_account(self, username, email, password):
        # Implementation to come
        pass

    def check_access(self, user_id, resource):
        # Implementation to come
        pass

    def change_password(self, user_id, old_password, new_password):
        # Implementation to come
        pass


# User class for now, will be moved to models later
class User:
    def __init__(self, username, is_authenticated):
        self.username = username
        self.is_authenticated = is_authenticated
        debug_print(f"Debug: Username is {self.username}")



# Create an instance for global access or dependency injection
user_manager = UserManager()


# In user_manager.py
def current_user():
         debug_print(f"Debug: Username is {user_manager.current_user.username}")
         return user_manager.current_user  # Return the User object