# Description: This file contains the CommandContext class which is used to store the key store, info store, and client store
# objects. This class is used to pass these objects to the command classes so that they can interact with the data stores
from src.app.clientstore import ClientStore
from src.app.infostore import InfoStore
from src.app.keystore import KeyStore


class CommandContext:
    def __init__(self, key_store: KeyStore, info_store: InfoStore, client_store: ClientStore):
        self.key_store = key_store
        self.info_store = info_store
        self.client_store = client_store
        self.slaves = []
