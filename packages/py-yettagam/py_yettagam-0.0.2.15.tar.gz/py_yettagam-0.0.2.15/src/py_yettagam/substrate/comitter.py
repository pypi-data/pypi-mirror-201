# MetariumTopicCommitter for a substrate chain

# standard imports
import logging
import ipaddress
import json
import os
import time
# third party imports
from blake3 import blake3
import paramiko
from substrateinterface import SubstrateInterface, Keypair
import sshpubkeys
from sshpubkeys import SSHKey, InvalidKeyError
from tinydb import TinyDB, Query
# local imports
from .decorators import skip_if_committing, skip_if_uploading
from .exceptions import ChainConnectionRefusedError, AriKuriAlreadyExistsError


logging.basicConfig(format='%(process)d : %(asctime)s : %(levelname)s\n%(message)s\n',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class SubstrateCommitter(object):

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    def __init__(self, config_path: str = None) -> None:
        # set config_path
        self.__config_path = config_path or None
        # verify config_path
        if self.__config_path is not None:
            assert os.path.exists(self.__config_path)
        # get config
        self.__config = self.__get_config()
        # get key_path from config
        key_path = self.__config.get("key_path", None)
        assert key_path is not None
        # check if key_path exists
        if not os.path.exists(key_path):
            error_message = f"key_path {key_path} does not exist!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)
        # get chain_spec_path from config
        chain_spec_path = self.__config.get(
            "chain_spec_path", None)
        assert chain_spec_path is not None
        # check if chain_spec_path exists
        if not os.path.exists(chain_spec_path):
            error_message = f"chain_spec_path {chain_spec_path} does not exist!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)
        # get chain_url from config
        chain_url = self.__config.get("chain_url", None)
        assert chain_url is not None
        # check if chain_url is valid
        if not isinstance(chain_url, str):
            error_message = f"chain_url {chain_url} is not a string!"
            logging.error(error_message)
            raise TypeError(error_message)
        # get ssh_private_key_path from config
        ssh_private_key_path = self.__config.get("ssh_private_key_path", None)
        assert ssh_private_key_path is not None
        # check if ssh_private_key_path is valid
        if not isinstance(ssh_private_key_path, str):
            error_message = f"ssh_private_key_path {ssh_private_key_path} is not a string!"
            logging.error(error_message)
            raise TypeError(error_message)
        if not os.path.exists(ssh_private_key_path):
            error_message = f"ssh_private_key_path {ssh_private_key_path} does not exist!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)
        # get ssh_private_key_passphrase from config
        ssh_private_key_passphrase = self.__config.get(
            "ssh_private_key_passphrase", None)
        # check if ssh_private_key_passphrase is valid
        if not isinstance(ssh_private_key_passphrase, str):
            error_message = f"ssh_private_key_passphrase {ssh_private_key_passphrase} is not a string!"
            logging.error(error_message)
            raise TypeError(error_message)
        # get listener_threshold from config
        listener_threshold = self.__config.get(
            "listener_threshold", 3)
        # check if listener_threshold is valid
        if not isinstance(listener_threshold, int):
            error_message = f"listener_threshold {listener_threshold} is not an integer!"
            logging.error(error_message)
            raise TypeError(error_message)
        if listener_threshold < 1:
            error_message = f"listener_threshold {listener_threshold} is less than 1!"
            logging.error(error_message)
            raise ValueError(error_message)
        # get key from key_path file
        with open(key_path, "r") as key_file:
            # create keypair from key
            self.__key = Keypair.create_from_mnemonic(key_file.read())
        # create a blake3 hash of the chain_spec_path file
        self.__chain_spec_hash = self._file_hash(chain_spec_path)
        # set ssh_private_key_path
        self.__ssh_private_key_path = ssh_private_key_path
        # set ssh_private_key_passphrase
        self.__ssh_private_key_passphrase = ssh_private_key_passphrase
        # set listener_threshold
        self.__listener_threshold = listener_threshold
        reconnection_attempts = 1
        while True:
            try:
                self.__chain = SubstrateInterface(url=chain_url)
            except ConnectionRefusedError:
                if reconnection_attempts == self.__class__.MAX_RECONNECTION_ATTEMPTS:
                    logging.error(
                        f"Chain connection terminated after {reconnection_attempts} attempts.")
                    logging.exception(ChainConnectionRefusedError)
                logging.warning(
                    f"Chain connection refused. Retrying in {self.__class__.RECONNECTION_WAIT_DURATION_SECONDS} seconds ...")
                reconnection_attempts += 1
                time.sleep(self.__class__.RECONNECTION_WAIT_DURATION_SECONDS)
                continue
            break
        connected_message = f"\n\n\nConnected to {self.__chain.name} {self.__chain_spec_hash} as Committer {self.__key.ss58_address}!\n\n\n"
        logging.info(f"{'*' * 100}\n{connected_message}{'*' * 100}")

        self._is_committing = False
        self._is_uploading = False

    ############################## CONFIG LOGIC ##############################

    def __get_config(self) -> dict:
        if self.__config_path is None:
            return {}
        with open(self.__config_path, "r") as config_file:
            return json.load(config_file)

    ############################## INPUT VERIFICATION FOR COMMIT/RE-UPLOAD FUNCTONS ##############################

    def __verify_topic_id(self, topic_id: int) -> None:
        if not isinstance(topic_id, int):
            logging.error(f"topic_id {topic_id} is not an integer!")
            raise TypeError
        if topic_id < 0:
            logging.error(f"topic_id {topic_id} is less than 0!")
            raise ValueError

    def __verify_file_location_path(self, file_location_path: str) -> None:
        if not isinstance(file_location_path, str):
            logging.error(
                f"file_location_path {file_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(file_location_path):
            logging.error(
                f"file_location_path {file_location_path} does not exist!")
            raise FileNotFoundError

    ############################## COMMIT FUNCTONS ##############################

    def __start_committing(self):
        self._is_committing = True

    def __stop_committing(self):
        self._is_committing = False

    @skip_if_committing
    def commit(self, topic_id: int = None,
               file_location_path: str = None) -> None:
        # check if topic_id is valid
        self.__verify_topic_id(topic_id)
        # check if file_location_path is valid
        self.__verify_file_location_path(file_location_path)
        self.__start_committing()
        # set topic_id
        self.__topic_id = topic_id
        # set file_location_path
        self.__file_location_path = file_location_path
        # create the kuri from the file
        kuri = self._arikuri_hash(file_path=self.__file_location_path)
        # check if kuri already exists
        query_result = self.__chain.query(
            module="Metarium",
            storage_function="Arikuris",
            params=[self.__topic_id, kuri],
        )
        # if kuri already exists, raise error
        if query_result.serialize() is not None:
            self.__stop_committing()
            raise AriKuriAlreadyExistsError(
                f"Kuri {kuri }already exists for the topic {self.__topic_id}")
        # if kuri does not exist, upload it
        logging.info(f"Uploading Kuri {kuri} to topic {self.__topic_id} ...")
        # prepare the transaction call
        call = self.__chain.compose_call(
            call_module="Metarium",
            call_function="arikuri_added",
            call_params={
                "topic_id": self.__topic_id,
                'kuri': kuri,
            }
        )
        # get the nonce for the account
        nonce = self.__chain.get_account_nonce(
            self.__key.ss58_address)
        # generate the signature payload for the transaction call
        signature_payload = self.__chain.generate_signature_payload(
            call=call, nonce=nonce)
        # sign the payload
        signature = self.__key.sign(signature_payload)
        # create the signed transaction call to the chain
        transaction = self.__chain.create_signed_extrinsic(
            call=call,
            keypair=self.__key,
            signature=signature,
            nonce=nonce
        )
        logging.info(f"{transaction = }")
        # submit the transaction call to the chain
        receipt = self.__chain.submit_extrinsic(
            transaction,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        if receipt.is_success:
            logging.info(
                f"Kuri {kuri} for topic {self.__topic_id} successfully committed to chain with transaction hash {receipt.extrinsic_hash}")
            self.__upload()
        else:
            logging.error(
                f"Transaction failed\n\n{receipt.error_message}\n\n")
        self.__stop_committing()

    ############################## UPLOAD FUNCTONS ##############################

    def __start_uploading(self):
        self._is_uploading = True

    def __stop_uploading(self):
        self.__file_location_path = None
        self.__topic_id = None
        self._is_uploading = False

    def __upload_file(self, ip_address: str = None) -> None:
        # check if ip_address is valid
        if not isinstance(ip_address, str):
            logging.error(
                f"ip_address {ip_address} is not a string!")
            raise TypeError
        if not self._is_valid_ip_address(ip_address):
            logging.error(
                f"ip_address {ip_address} is not a valid IP address!")
            raise ValueError
        # get the file name
        file_name = os.path.basename(self.__file_location_path)
        # upload the file to the ip_address via SFTP
        logging.info(
            f"Initiating file upload to {ip_address} ...")
        # setup the ssh client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username="writer",
                           pkey=paramiko.RSAKey.from_private_key_file(
                               self.__ssh_private_key_path, password=self.__ssh_private_key_passphrase))
        # setup the sftp client
        sftp_client = ssh_client.open_sftp()
        # upload the file
        sftp_client.put(
            localpath=self.__file_location_path,
            remotepath=f"/home/.metarium/inbox/{self.__chain_spec_hash}/{file_name}",
            confirm=True)
        # close the sftp client
        sftp_client.close()
        # close the ssh client
        ssh_client.close()
        logging.info(
            f"file {file_name} successfully uploaded to IP address {ip_address}!")

    def __upload(self) -> None:
        self.__start_uploading()
        # get the topic from the chain
        topic_from_chain = self.__topic_from_chain(self.__topic_id)
        # get the listeners from the topic
        listeners = topic_from_chain.get("listener_nodes", [])
        # get listeners with a valid IP address
        valid_listeners = []
        # get the node info from the chain
        for listener in listeners:
            node_info = self.__node_info_from_chain(listener)
            ip_address = node_info.get("ip_address", None)
            ssh_pub_key = node_info.get("ssh_pub_key", None)
            if ip_address is not None and self._is_valid_ip_address(ip_address):
                valid_listeners.append({
                    "node": listener,
                    "ip_address": ip_address,
                    "ssh_pub_key": ssh_pub_key
                })
        # check if there are enough valid listeners
        if len(valid_listeners) < self.__listener_threshold:
            # if there are not enough valid listeners, raise a warning
            logging.warning(
                f"Only {len(valid_listeners)} valid listeners for topic {self.__topic_id}. Threshold is {self.__listener_threshold}")
        # upload the file to the listeners
        for listener in valid_listeners:
            # upload the file to the listener
            self.__upload_file(ip_address=listener["ip_address"])
        self.__stop_uploading()

    @skip_if_uploading
    def re_upload(self, topic_id: int = None,
                  file_location_path: str = None) -> None:
        # check if topic_id is valid
        self.__verify_topic_id(topic_id)
        # check if file_location_path is valid
        self.__verify_file_location_path(file_location_path)
        self.__start_committing()
        # set topic_id
        self.__topic_id = topic_id
        # set file_location_path
        self.__file_location_path = file_location_path
        # upload the file
        self.__upload()

    ############################## CHAIN QUERYING ##############################

    def __topic_from_chain(self, topic: int):
        # query the chain for the topic
        topic = self.__chain.query(
            module="Metarium", storage_function="Topics", params=[topic])

        topic = topic.serialize()

        if topic == None:
            topic = {}

        return topic

    def __node_info_from_chain(self, node: str):
        # query the chain for the node
        node = self.__chain.query(
            module="Metarium", storage_function="NodeInfoMap", params=[node])

        node = node.serialize()
        if node == None:
            node = {}

        return node

    ############################## UTILITY FUNCTONS ##############################

    def _file_hash(self, file_path: any = None) -> str:
        # check if file_path is valid
        if not isinstance(file_path, str):
            logging.error(f"file_path {file_path} is not a string!")
            raise TypeError
        if not os.path.exists(file_path):
            logging.error(f"file_path {file_path} does not exist!")
            raise FileNotFoundError
        # create a blake3 hash of the content
        hasher = blake3(max_threads=blake3.AUTO)
        with open(file_path, "rb") as f:
            counter = 0
            while True:
                counter += 1
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)

        return hasher.hexdigest()

    def _arikuri_hash(self, file_path: any = None) -> str:
        return f"|>blake3|{self._file_hash(file_path=file_path)}"

    def _is_valid_ip_address(self, ip_address: str = None) -> bool:
        # check if ip_address is valid
        if not isinstance(ip_address, str):
            logging.error(f"ip_address {ip_address} is not a string!")
            raise TypeError
        # check if ip_address is valid
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False

    def _is_valid_ssh_pub_key(self, ssh_pub_key: str = None) -> bool:
        # check if ssh_pub_key is valid
        if not isinstance(ssh_pub_key, str):
            logging.error(f"ssh_pub_key {ssh_pub_key} is not a string!")
            raise TypeError
        # check if ssh_pub_key is valid
        ssh = SSHKey(ssh_pub_key, strict=True)
        try:
            ssh.parse()
        except InvalidKeyError as err:
            return False
        except NotImplementedError as err:
            return False
        return True
