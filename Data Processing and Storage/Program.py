class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.transaction = False
        self.changes = {}

    def get(self, key):
        # get(key) will return the value associated with the key or null if the key doesn’t exist.
        return self.data.get(key, None)

    def put(self, key, val):
        #put(key, val) is called when a transaction is not in progress throw an exception
        if not self.transaction:
            raise Exception("Error: No transaction in progress")
        self.changes[key] = val

    def begin_transaction(self):
        # begin_transaction() starts a new transaction.
        if self.transaction:
            raise Exception("Transaction already in progress")
        self.transaction = True
        self.changes = {}

    def commit(self):
        # commit() applies changes made within the transaction to the main state. Allowing any future gets() to “see” the changes made within the transaction
        if not self.transaction:
            raise Exception("No transaction in progress")
        self.data.update(self.changes)
        self.transaction = False
        self.changes = {}

    def rollback(self):
        # rollback() should abort all the changes made within the transaction and everything should go back to the way it was before.
        if not self.transaction:
            raise Exception("No transaction in progress")
        self.transaction = False
        self.changes = {}

# Example usage
inmemoryDB = InMemoryDB()
print(inmemoryDB.get("A"))  #Should return none, because A doesn’t exist in the DB yet

try:
    inmemoryDB.put("A", 5)
except Exception as e:
    print(e)  # should throw an error because a transaction is not in progress

inmemoryDB.begin_transaction() #starts a new transaction

inmemoryDB.put("A", 5)  # set’s value of A to 5, but it's not committed yet
print(inmemoryDB.get("A"))  # should return None, because updates to A are not committed yet

inmemoryDB.put("A", 6)  # update A’s value to 6 within the transaction

inmemoryDB.commit()  # commits the open transaction
print(inmemoryDB.get("A"))  # should return 6, that was the last value of A to be committed

try:
    inmemoryDB.commit()
except Exception as e:
    print(e)  # throws an error, because there is no open transaction

try:
    inmemoryDB.rollback()
except Exception as e:
    print(e)  # throws an error because there is no ongoing transaction

print(inmemoryDB.get("B"))  # should return None because B does not exist in the database

inmemoryDB.begin_transaction() #starts a new transaction
inmemoryDB.put("B", 10)  # Set key B’s value to 10 within the transaction

inmemoryDB.rollback()  # Rollback the transaction - revert any changes made to B

print(inmemoryDB.get("B"))  # Should return None because changes to B were rolled back
