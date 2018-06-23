import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message

from models import WPChannelBotModel
from CONSTANTS import *

class WPChannelBot():
	def __init__(self):
		self.model = WPChannelBotModel()	
		self.data = self.model.get_all()	
		self.convs = self.model.get_convs()
		self.convs_state = self.model.get_convs_state()

		self.simple_steps = True
		self.log_file = None

		self.cmd_wait_from = None
		self.cmd_wait = False

		self.profile = "profile"
		self.driver = None

	def start(self):
		print("Iniciando bot...")
		self.driver = WhatsAPIDriver(profile=self.profile)
		time.sleep(3)
		if not self.driver.get_status() == "LoggedIn":
			print("Carregando QRCode")
			self.driver.get_qr("qrcode.png")

			print("Escaneie o QRCode no arquivo qrcode.png")
			self.driver.wait_for_login()

		print("Bot iniciado")
		self.driver.save_firefox_profile()

		self.log_file = time.strftime("log/%Y-%m-%d&%Hh%Mm%Ss.log", time.gmtime())

		while True:
			time.sleep(3)
			for contact in self.driver.get_unread(include_me=False, include_notifications=True, use_unread_count=True):
			#for contact in self.driver.get_unread():
				for message in contact.messages:

					#import pdb;pdb.set_trace()
					if isinstance(message, Message):
						self.new_message(message.content, contact)
						self.driver.chat_send_seen(contact.chat.id)
						time.sleep(3)

	def _to_log(self, log):
		file = open(self.log_file, "a")
		file.write("\n>> %s " % log)
		file.close()
		return

	def _get_conv_nome(self, id):
		for obj in self.data:
			if obj["id"] == id:
				return obj["nome"]

	def _remove_convs(self, id):
		self.convs.remove(id)
		for conv in self.convs_state:
			if conv["id"] == id:
				self.convs_state.remove(conv)
				self.model.conv_delete(id)

	def _proc_etapa(self, id, content, chat, etapa):
		if etapa == 2:
			if isinstance(self.model.get(id), dict):
				chat.send_message("Olá, você já está cadastrado neste canal. Assim que tiver novidade você vai receber!")
			elif content.lower() == CHANNEL_KEYWORD:
				# Efetua registros
				self.convs.append(id)
				self.convs_state.append({
					"id": id,
					"etapa": 4
				})
				self.model.conv_add(id, 4)

				# Introdução do canal - Solicita nome
				chat.send_message(CHANNEL_INTRO)
				chat.send_message(CHANNEL_MSGS[0])
				self._to_log("Iniciando cadastro: %s" % id)
			else:
				chat.send_message(CHANNEL_ASK_KEYWORD)

		elif etapa == 4:
			# Armazena nome - Solicita cidade
			if self.simple_steps:
				self.data.append({
					"id": id,
					"nome": content
				})
				# Salva no banco de dados
				self.model.add(id, content)

				chat.send_message((CHANNEL_MSGS[3] % content))
				self._remove_convs(id)

				self._to_log("Finalizado cadastro: %s - %s" % (id, content))
			else:
				self.data.append({
					"id": id,
					"nome": content,
					"cidade": "",
					"bairro": ""
				})
				chat.send_message(CHANNEL_MSGS[1])
				# Salva no banco de dados
				self.model.add(id, content)

				self._to_log("Registrado nome: %s - %s" % (id, content))
				return 6

		elif etapa == 6:
			# Implementar veficação de validade de cidade
			# Verifica cidade - volta ao 5 : armazena cidade - solicita bairro ou passo
			for obj in self.data:
				if obj["id"] == id:
					obj["cidade"] = content

					self.model.update(id=id, cidade=content)
					chat.send_message(CHANNEL_MSGS[2])

					self._to_log("Registrado cidade: %s - %s" % (id, content))
			return 7
		elif etapa == 7:
			# Implementar veficação de validade de bairro
			if content == "passo":
				# Finaliza caso não seja informado bairro
				chat.send_message((CHANNEL_MSGS[3] % self._get_conv_nome(id)))

				self._remove_convs(id)
				self._to_log("Finalizado cadastro: %s - %s" % (id, content))
			else:
				# Armazena bairro - Finaliza cadastro
				for obj in self.data:
					if obj["id"] == id:
						obj["bairro"] = content
						self.model.update(id=id,bairro = content)

						chat.send_message((CHANNEL_MSGS[3] % self._get_conv_nome(id)))
						
						self._remove_convs(id)
						self._to_log("Finalizado cadastro: %s - %s" % (id, content))


	def _is_cmd(self, content):
		if content[:4] == "/cmd":
			return True
		else:
			return False

	def _run_cmd(self, content, chat):
		cmd = content[5:]

		if cmd == "usuarios":
			self._cmd_usuarios(chat)
		elif cmd == "envio":
			self.cmd_wait = True
			self.cmd_wait_from = chat.id
			chat.send_message("*ENVIE A SEGUIR A MENSAGEM A SER ENVIADA PARA O CANAL*")
		else:
			chat.send_message("*COMANDO NÃO RECONHECIDO*")

	def _cmd_usuarios(self, chat):
		response = "*USUÁRIOS CADASTRADOS*\n\n"

		i = 0
		users = self.model.get_all()
		for user in users:
			i += 1
			response += "\n%d) %s - %s" % (i, user['id'], user['nome'])

		chat.send_message(response)

	def _cmd_envio(self, content, chat):
		i = 0
		users = self.model.get_all()
		for user in users:
			i += 1
			self.driver.send_message_to_id(user['id'], content)

		self.cmd_wait_from = None
		self.cmd_wait = False
		chat.send_message("*MENSAGEM ENVIADA PARA %d USUÁRIOS DO CANAL*" % i)


	def new_message(self, message, contact):
		if not self._is_cmd(message):
			if self.cmd_wait and contact.chat.id == self.cmd_wait_from:
				self._cmd_envio(message, contact.chat)
				
			elif not contact.chat.id in self.convs:		
				self._proc_etapa(contact.chat.id, message, contact.chat, 2)
			else:
				for conv in self.convs_state:
					if conv['id'] == contact.chat.id:
						e = self._proc_etapa(contact.chat.id, message, contact.chat, conv['etapa'])
						conv['etapa'] = e

						self.model.conv_update(contact.chat.id, e)
		else:
			self._run_cmd(message, contact.chat)
