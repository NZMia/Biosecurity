from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, user_id, email, password_hash, state, role_id):
      self.id = user_id
      self.email = email
      self.password_hash = password_hash
      self.state = state
      self.role_id = role_id
