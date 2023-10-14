import hashlib
import time
from blockchain import models

class Block:
    def __init__(self, index=0, proof_no=0, prev_hash=0, data=None,users_hash=0,timestamp=time.time()):
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.users_hash = users_hash
        self.addBlock()

    def addBlock(self):
        newBlock = models.block(
            index = self.index,
            proof = self.proof_no,
            prevHash = self.prev_hash,
            data = self.data,
            timestamp = self.timestamp,
            usershash = self.users_hash,
            current_hash = self.calculate_hash()
        )
        newBlock.save()
        
    @staticmethod
    def convertModel(model):
        block = Block(
            index= model.index,
            proof_no=models.proof,
            prev_hash=models.prevHash,
            data=models.data,
            timestamp=models.timestamp,
            users_hash=models.users_hash
        ) 
        return block
        
    @property
    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}{}".format(self.index, self.proof_no,self.prev_hash, self.data,self.timestamp,self.users_hash)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return "Index: {} - Proof No: {} - Prev Hash: {} - Data: {} - Timestamp: {} - Users Hash{}".format(self.index, self.proof_no,self.prev_hash, self.data,self.timestamp,self.users_hash)
