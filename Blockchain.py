"""
/*
 * This  File is modified/created by Arafat Chaghtai for educational purposes.
 * The author could be contacted at: arafatc@gmail.com for any clarifications.
 *
 * Licensed under GNU General Public License v3.0
 *
 * This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS 
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */
 """
import json
import hashlib
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import utils

from Block import Block


class Blockchain:
    # Basic blockchain init
    # Includes the chain as a list of blocks in order, pending transactions, and known accounts
    # Includes the current value of the hash target. It can be changed at any point to vary the difficulty
    # Also initiates a genesis block
    def __init__(self, hash_target):
        self._chain = []
        self._pending_transactions = []
        self._chain.append(self.__create_genesis_block())
        self._hash_target = hash_target
        self._accounts = {}

    def __str__(self):
        return f"Chain:\n{self._chain}\n\nPending Transactions: {self._pending_transactions}\n"

    @property
    def hash_target(self):
        return self._hash_target

    @hash_target.setter
    def hash_target(self, hash_target):
        self._hash_target = hash_target

    # Creating the genesis block, taking arbitrary previous block hash since there is no previous block
    # Using the famous bitcoin genesis block string here :)  
    def __create_genesis_block(self):
        genesis_block = Block(0, [], 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks',
                              None, 'Genesis block using same string as bitcoin!')
        return genesis_block

    def __validate_transaction(self, transaction):
        # Digitally verify the signature against hash of the message to validate authenticity
        # Return False otherwise
        sender_account = self.get_account_details(transaction['message']['sender'])
        public_key = serialization.load_pem_public_key(sender_account.public_key, backend=None)

        transaction_string = json.dumps(transaction['message'], sort_keys=True).encode('utf-8')
        message = hashlib.sha256(transaction_string).digest()

        # Recovering Base64 encoded string to bytes
        signature = base64.b64decode(transaction['signature'].encode('utf-8'))

        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )

        return True

    def __process_transactions(self, transactions):
        # Appropriately transfer value from the sender to the receiver
        # For all transactions, first check that the sender has enough balance. 
        # Return False otherwise
        for transaction in transactions:
            sender_account = self.get_account_details(transaction['message']['sender'])
            receiver_account = self.get_account_details(transaction['message']['receiver'])

            if sender_account.balance >= transaction['message']['value']:
                sender_account.decrease_balance(transaction['message']['value'])
                receiver_account.increase_balance(transaction['message']['value'])
            else:
                txn_message = transaction['message']
                print(f'ERROR: Transaction: {txn_message} failed account balance validation')
                return False

        return True

    # Creates a new block and appends to the chain
    # Also clears the pending transactions as they are part of the new block now
    def create_new_block(self):
        new_block = Block(len(self._chain), self._pending_transactions, self._chain[-1].block_hash, self._hash_target)
        if self.__process_transactions(self._pending_transactions):
            self._chain.append(new_block)
            self._pending_transactions = []
            return new_block
        else:
            return False

    # Simple transaction with just one sender, one receiver, and one value
    # Created by the account and sent to the blockchain instance
    def add_transaction(self, transaction):
        if self.__validate_transaction(transaction):
            self._pending_transactions.append(transaction)
            return True
        else:
            print(f'ERROR: Transaction: {transaction} failed signature validation')
            return False

    def __validate_chain_hash_integrity(self):
        # Run through the whole blockchain and ensure that previous hash is actually the hash of the previous block
        # Return False otherwise
        for index in range(1, len(self._chain)):
            if self._chain[index].previous_block_hash != self._chain[index - 1].hash_block():
                print(f'Previous block hash mismatch at block index: {index}')
                return False
        return True

    def __validate_block_hash_target(self):
        # Run through the whole blockchain and ensure that block hash meets hash target criteria, and is the actual
        # hash of the block Return False otherwise
        for index in range(1, len(self._chain)):
            if int(self._chain[index].hash_block(), 16) >= int(self._chain[index].hash_target, 16):
                print(f'Hash target not achieved at block index: {index}')
                return False
            if self._chain[index].block_hash != self._chain[index].hash_block():
                print(f'Hash block mismatch with stored block at block index: {index}')
                return False
        return True

    def __validate_complete_account_balances(self):
        # Run through the whole blockchain and ensure that balances never become negative from any transaction
        # Return False otherwise
        return True

    # Blockchain validation function
    # Runs through the whole blockchain and applies appropriate validations
    def validate_blockchain(self):
        # Call __validate_chain_hash_integrity and implement that method. Return False if check fails
        # Call __validate_block_hash_target and implement that method. Return False if check fails
        # Call __validate_complete_account_balances and implement that method. Return False if check fails

        validation_result_chain = self.__validate_chain_hash_integrity()
        validation_result_block = self.__validate_block_hash_target()
        validation_result_complete = self.__validate_complete_account_balances()

        if not validation_result_chain:
            return False
        if not validation_result_block:
            return False
        if not validation_result_complete:
            return False

        return True

    def add_account(self, account):
        self._accounts[account.id] = account

    def get_account_balances(self):
        return [{'id': account.id, 'balance': account.balance} for account in self._accounts.values()]

    def get_account_details(self, entity):
        for account in self._accounts.values():
            if account.id == entity:
                return account