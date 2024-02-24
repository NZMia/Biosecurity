from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, user_id, email, password_hash, status, role_id):
      self.id = user_id
      self.email = email
      self.password_hash = password_hash
      self.status = status
      self.role_id = role_id
