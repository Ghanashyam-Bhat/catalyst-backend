from django.shortcuts import render
from chain import BlockChain
from block import Block
from blockchain import models

# Create your views here.
def transferCrypto():
    blockchain = BlockChain()
    
    data = blockchain.new_data(
        sender=None,
        recipient=None,
        quantity=None,
        note=None
    )
    
    last_block = blockchain.latest_block
    
    last_proof_no = last_block.proof_no
    proof_no = blockchain.proof_of_work(last_proof_no)
    
    last_hash = last_block.calculate_hash
    users_hash = blockchain.get_users_hash()
    
    block = blockchain.construct_block(proof_no, last_hash,users_hash,data)
    
def verifyUsersData():
    blockchain = BlockChain()
    latest_block = blockchain.latest_block()
    result = blockchain.verifyUsersHash(latest_block)
    return result
    
def verifyChainData():
    chain = models.block.objects.all()
    for i in range(1,len(chain)):
        prev = Block.convertModel(chain[i-1])
        pres = Block.convertModel(chain[i])
        result = BlockChain.check_validity(pres,prev)
        if result == False:
            return False
    return True
        
def verifyLatestBlock():
    blockchain = BlockChain()
    latest_block = blockchain.latest_block()
    lastHash = latest_block.calculate_hash()
    
    if blockchain.hash != lastHash:
        return False
    return True
    
        
def verifyBlockchain():
    result =  verifyLatestBlock() and verifyUsersData() and verifyBlockchain()
    return result