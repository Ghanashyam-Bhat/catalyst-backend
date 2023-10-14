from block import Block
import hashlib
from blockchain import models
from home.models import student

class BlockChain:
    def __init__(self):
        try:
            model = models.block.objects.latest('index')
            self.latest = Block.convertModel(model=model)
            self.hash = model.current_hash
        except:
            self.latest = self.construct_genesis()
            self.hash = self.latest.calculate_hash()
            
    def construct_genesis(self):
        block = Block()
        return block

    def construct_block(self, proof_no, prev_hash, users_hash,data):
        block = Block(
            index=self.latest.index+1,
            proof_no = proof_no,
            prev_hash = prev_hash,
            data = data,
            users_hash = users_hash
            )
        self.latest = block
        return block

    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False
        elif prev_block.calculate_hash != block.prev_hash:
            return False
        elif not BlockChain.verifying_proof(block.proof_no,prev_block.proof_no):
            return False
        elif block.timestamp <= prev_block.timestamp:
            return False
        return True

    def new_data(self, sender, recipient, quantity,note):
        data = {
            "sender":sender,
            "recipient":recipient,
            "quantity":quantity,
            "note": note
        }
        return data
    
    @staticmethod
    def proof_of_work(last_proof):
        '''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
         f is the previous f'
         f' is the new proof
        '''
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1
        return proof_no
    
    @staticmethod
    def get_users_hash():
        studentList = student.objects.all()
        string = ""
        for itr in studentList:
            string += "{}{}".format(itr.srn,itr.crypto)
        user_hash =  hashlib.sha256(string.encode()).hexdigest()
        return user_hash

    @staticmethod
    def verifying_proof(last_proof, proof):
        #verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    @staticmethod
    def verifyUsersHash(lastBlock):
        if lastBlock.latest.users_hash != lastBlock.get_users_hash() : 
            return False
        return True
    
    @property
    def latest_block(self):
        return self.latest
