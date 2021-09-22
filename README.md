# Cryptography
Extended a simple blockchain example to cover key generation, digital signing, and transaction and block validations.
This is a minimal example and may not follow some standard practices
● The focus is on the main flow, with minimal error handling. 
● This has basic blockchain semantics. It doesn’t follow bitcoin transaction’s multiple
sender/receiver complexity. It stores a running balance like Ethereum, instead of a UTXO
based structure like bitcoin.

● Block.py: This class implements a basic Block including some mandatory attributes like
previous block hash, index, creation timestamp, transactions, hash target, nonce, and the final
block hash. The hash_block method generates a hash for the block including all relevant components. 
● Account.py: This class implements a blockchain account including some mandatory
attributes like id, balance, nonce, and private/public keys encoded in pem format strings.
The id is just a text string here, instead of a large hexadecimal address. Uniqueness is
assumed but not enforced. It keeps a running balance of value, unlike bitcoin.
● Blockchain.py: This class implements a basic Blockchain including some mandatory
attributes like the actual chain of blocks, pending transactions, known accounts, and the
current target hash. Genesis block is automatically created during initialization.
● main.py: This is the main driver program. It creates some accounts, a blockchain instance
and blocks. It also triggers a full blockchain validation and prints the blockchain and the
current account balances.

1. Implemented the cryptographic functionalities for the blockchain account
a. Implemented private/public key pair generation in __generate_key_pair private method in
Account class and assign them to _private_pem and _public_pem attributes. 
b. Completed the create_transaction method in Account class:
i. Generated the private key object from the pem created in 1.a
ii. Generated the hash of the transaction message
iii. Digitally sign the hash with the private key
iv. Handled formatting appropriately for hashing and signing inputs
v. Converted the signature from ‘bytes’ to an appropriate string
based format. Base64 is an appropriate choice, base64 library is already
imported.
c. Completed the __validate_transaction method in Blockchain class:
i. Generated the public key object using the public pem from the account
ii. Hashed the transaction message with a similar process as while signing
iii. Digitally verified the generated hash with the signature
iv. Handle formatting appropriately for hashing and verification inputs
2. Implemented validations at various levels
a. Implemented __process_transactions method in Blockchain class. For each transaction,
checked that there is enough balance in the sender account and then
appropriately transfer correct value from the sender to the receiver
b. Implemented validate_blockchain method and the methods called within.
