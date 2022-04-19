
class FingerManager:
  def __init__(self):
    self.object_tracker = {}
    pass

  def get_values(self, key):
    if not key:
      return None

    return self.object_tracker[key] if key in self.object_tracker else None

  def set_values(self, key, values):
    self.object_tracker[key] = values
    print(f'{key} => {values}')
    return

  def append(self, key, value):
    vals = self.get_values(key)
    if not vals:
      return self.set_values(key, [value])
    vals.append(value)
    self.set_values(key, vals)

  def remove(self, key, value):
    vals = self.get_values(key)
    if not vals:
      return None

    vals.remove(value)
    self.set_values(key, vals)

  def clear_values(self, key):
    self.set_values(key, [])

finger_manager = FingerManager()
