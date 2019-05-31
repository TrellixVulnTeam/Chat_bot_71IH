import MySQLdb

class RestaurantDb():
  def __init__(self):
    self.host = 'localhost'
    self.user = 'root'
    self.passwd = '1998'
    self.db = 'restaurant_bot'

  def check_date(self, booking_date):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}'".format(booking_date))
    if result == 0:
      cur.execute("INSERT INTO booking(date, slot1, slot2, slot3) VALUES('{0}', JSON_ARRAY(true, true, true), JSON_ARRAY(true, true, true), JSON_ARRAY(true, true, true))".format(booking_date))
      conn.commit()
    free_timeslot = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND (JSON_EXTRACT(slot1, '$[2]') OR JSON_EXTRACT(slot2, '$[2]') OR JSON_EXTRACT(slot3, '$[2]'))".format(booking_date))
    if free_timeslot != 0:
      return True
    return False

  
  def free_slot1(self, booking_date):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot1, '$[2]')".format(booking_date))
    if result != 0:
      return True
    return False

  def free_slot2(self, booking_date):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot2, '$[2]')".format(booking_date))
    if result != 0:
      return True
    return False

  def free_slot3(self, booking_date):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot3, '$[2]')".format(booking_date))
    if result != 0:
      return True
    return False

  def free_time1(self, booking_date, slot):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT({1}, '$[0]')".format(booking_date, slot))
    if result != 0:
      return True
    return False

  def free_time2(self, booking_date, slot):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT({1}, '$[1]')".format(booking_date, slot))
    if result != 0:
      return True
    return False

  def book_table(self, booking_date, time_slot, slot):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    cur.execute("UPDATE booking SET {0} = JSON_SET({0}, '$[{2}]', false) WHERE date = '{1}'".format(slot, booking_date, time_slot))
    cur.execute("UPDATE booking SET {0} = JSON_SET({0}, '$[2]', false) WHERE date = '{1}' AND (NOT JSON_EXTRACT({0}, '$[0]')) AND (NOT JSON_EXTRACT({0}, '$[1]'))".format(slot, booking_date))
    conn.commit()

  def book_note(self, booking_date, booking_time, booking_note):
    conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    cur = conn.cursor()
    cur.execute("INSERT INTO booking_note(date, time, note) VALUES('{0}', '{1}', '{2}')".format(booking_date, booking_time, booking_note))
    conn.commit()

  def close(self):
    cur.close()
    conn.close()
    