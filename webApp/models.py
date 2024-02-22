from flask_login import UserMixin

class User(UserMixin):
  def __init__(self, user_id, password_hash, email, created_at, updated_at, status):
      self.id = user_id
      self.password_hash = password_hash
      self.email = email
      self.created_at = created_at
      self.updated_at = updated_at
      self.status = status

  