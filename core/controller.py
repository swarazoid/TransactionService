from collections import defaultdict
import json
import enum

class Status(enum.Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500

class Transaction:
    def __init__(self, params):
        self.transaction_id = params.get("transaction_id")
        self.amount = params.get("amount")
        self.type = params.get("type")
        self.parent_id = params.get("parent_id")
        self.sum_of_related_transactions = params.get("amount")

class TransactionCoordinator:
    instance = None

    # creating a singleton class
    class __OnlyOne:
        def __init__(self):
            # self.types will keep a dict where key will be type and value will be an array of ids with this type
            self.types = defaultdict(list)
            # self.transactions will keep a dict where key is transaction id and value will be Transaction class object
            self.transactions = {}

    def __init__(self):
        if not TransactionCoordinator.instance:
            TransactionCoordinator.instance = TransactionCoordinator.__OnlyOne()

    def update_transaction(self, transaction):
        try:
            if transaction.transaction_id == transaction.parent_id:
                raise ValueError("Transaction_id can not be same as transaction's parent_id")
            if transaction.parent_id and transaction.parent_id not in self.instance.transactions:
                raise ValueError("Invalid Parent ID")
            if transaction.transaction_id in self.instance.transactions:
                raise ValueError("Transaction already exists")
            # Add the transaction to respective type
            self.instance.types[transaction.type].append(transaction.transaction_id)
            self.instance.transactions[transaction.transaction_id] = transaction
            amount = transaction.amount
            # Keep updating the sum_of_related_transactions for each transaction that comes in the path of the 
            # current transaction till the root(parent) transaction
            # Basically, add the new transaction as a leaf node in tree and update all the nodes value from root to this leaf
            while transaction.parent_id and transaction.parent_id in self.instance.transactions:
                parent_transaction = self.instance.transactions[transaction.parent_id]
                parent_transaction.sum_of_related_transactions += amount
                transaction = parent_transaction
            return {"status": "OK"}, Status.SUCCESS.value
        except ValueError as e:
            return {"message": str(e)}, Status.BAD_REQUEST.value
        except Exception as e:
            return {"message": str(e)}, Status.INTERNAL_SERVER_ERROR.value

    def get_transaction(self, transaction_id):
        try:
            if transaction_id in self.instance.transactions:
                return self.instance.transactions[transaction_id].__dict__, Status.SUCCESS.value
            else:
                return {"message": "Invalid Transaction ID"}, Status.BAD_REQUEST.value
        except Exception as e:
            return {"message": str(e)}, Status.INTERNAL_SERVER_ERROR.value
    
    def get_transactions_of_a_type(self, type):
        try:
            if type in self.instance.types:
                return self.instance.types[type], Status.SUCCESS.value
            else:
                return {"message": "Type does not exist"}, Status.BAD_REQUEST.value
        except Exception as e:
            return {"message": str(e)}, Status.INTERNAL_SERVER_ERROR.value

    def get_sum_of_related_transactions(self, transaction_id):
        try:
            if transaction_id in self.instance.transactions:
                return self.instance.transactions[transaction_id].sum_of_related_transactions, Status.SUCCESS.value
            else:
                return {"message": "Transaction ID does not exist"}, Status.BAD_REQUEST.value
        except Exception as e:
            return {"message": str(e)}, Status.INTERNAL_SERVER_ERROR.value
