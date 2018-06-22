import mysql.connector

CONFIG = {
  'user': '#####',
  'password': '######',
  'host': '127.0.0.1',
  'database': 'wpchannelbot',
  'raise_on_warnings': True,
}

class WPChannelBotModel():
	def __init__(self):
		self.connection = mysql.connector.connect(**CONFIG)
		self.cursor = self.connection.cursor()

	def _close(self):
		self.connection.close()

	def add(self, id, nome, cidade="", bairro=""):
		sql = ("INSERT INTO channel (id,nome,cidade,bairro) VALUES (%s, %s, %s, %s)")
		self.cursor.execute(sql, (id, nome, cidade, bairro))

		self.connection.commit()

	def update(self, id, nome="", cidade="", bairro=""):
		if not nome == "":
			sql = ("UPDATE channel SET nome = %s WHERE id = %s")
			self.cursor.execute(sql, (nome, id))

		if not cidade == "":
			sql = ("UPDATE channel SET cidade = %s WHERE id = %s")
			self.cursor.execute(sql, (cidade, id))

		if not bairro == "":
			sql = ("UPDATE channel SET bairro = %s WHERE id = %s")
			self.cursor.execute(sql, (bairro, id))

		self.connection.commit()

	def get(self, id):
		sql = ("SELECT id, nome, cidade, bairro FROM channel WHERE id = %s")
		self.cursor.execute(sql, (id, ))
		for (id, nome, cidade, bairro) in self.cursor:
			obj = {
				"id": id,
				"nome": nome,
				"cidade": cidade,
				"bairro": bairro
			}

		return obj

	def get_all(self):
		sql = ("SELECT * FROM channel")
		data = []

		self.cursor.execute(sql)
		for (id, nome, cidade, bairro) in self.cursor:
			data.append({
				"id": id,
				"nome": nome,
				"cidade": cidade,
				"bairro": bairro
			})

		return data

	def conv_add(self, id, etapa):
		sql = ("INSERT INTO convs (id) VALUES (%s)")
		self.cursor.execute(sql, (id, ))

		sql = ("INSERT INTO convs_state (id, etapa) VALUES (%s, %s)")
		self.cursor.execute(sql, (id, etapa))

		self.connection.commit()

	def conv_update(self, id, etapa):
		sql = ("UPDATE convs_state SET etapa = %s WHERE id = %s")
		self.cursor.execute(sql, (id, etapa))

		self.connection.commit()

	def conv_delete(self, id):
		sql = ("DELETE FROM convs WHERE id = %s")
		self.cursor.execute(sql, (id, ))

		sql = ("DELETE FROM convs_state WHERE id = %s")
		self.cursor.execute(sql, (id, ))

	def get_convs(self):
		sql = ("SELECT * FROM convs_state")
		convs = []

		self.cursor.execute(sql)
		for (id, etapa) in self.cursor:
			convs.append(id)

		return convs

	def get_convs_state(self):
		sql = ("SELECT * FROM convs_state")
		convs = []

		self.cursor.execute(sql)
		for (id, etapa) in self.cursor:
			convs.append({
				"id": id,
				"etapa": etapa
			})

		return convs

	def in_conv(self, id):
		try:
			sql = ("SELECT id FROM conv WHERE id = %s")
			self.cursor.execute(sql)

			return True
		except Exception as e:
			raise False





