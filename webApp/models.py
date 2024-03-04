from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, user_id, email, password_hash, state_id, role_id):
      self.id = user_id
      self.email = email
      self.password = password_hash
      self.state_id = state_id
      self.role_id = role_id
