import datetime
import random
import string
import hashlib
import json
import timeit

class block:
	def __init__(self, index, proof, previous_hash):
		self.children = []
		self.data = {
			'index': index,
			'timestamp': str(datetime.datetime.now()),
			'transaction': self.generate_rand_trans(),
			'proof': proof,
			'previous hash': previous_hash
		}

	def generate_rand_trans():
		return ''.join(random.choices(string.ascii_lowercase, k=50))

class blockchain:
	def __init__(self):
		# Initialize genesis block
		self.first_block = block(1, 1, '0')
		self.length = 1
		self.last_block = self.first_block

		# Find the appropriate number of hash zeros
		print("Calculating appropriate puzzle complexity for this hardware...")
		self.num_zeros = self.calc_zeros()
		print("Determined complexity is", self.num_zeros, "zeros for successful hash mine")
	
	# Functions that help initialize the num_zeros variable that controls complexity
	def proof_of_work_test(self, N):
		proof = 0
		block = {
			'index': 9,
			'timestamp': str(datetime.datetime.now()),
			'transactions': ''.join(random.choices(string.ascii_lowercase, k=50)),
			'proof': proof,
			'previous_hash': 69841654198}

		check_proof = False
		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(json.dumps(block, sort_keys=True)).encode()).hexdigest()
			
			if hash_operation[:N] == '0'*N:
				check_proof = True
			else:
				proof += 1
				block['proof']+=1

		return block

	def calc_zeros(self):
		for i in range(1,256):
			time = 0
			for j in range(10):
				start = timeit.default_timer()
				self.proof_of_work_test(i)
				finish = timeit.default_timer()
				time += finish - start
			time/=10
			if(time > 1): return i-1
	

	def add_block(self):
		self.last_block.children.append(
			block(
				self.last_block.data['index'] + 1,
				0,
				self.hash(self.last_data.data)))
		self.proof_of_work(self.last_block.children[0])
		self.last_block = self.last_block.children[0]
	
	def hash(self, block):
		# Block argument is the block-class instance we need to hash

		encoded_block = json.dumps(block.data, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def proof_of_work(self, block):
		# Block argument is the block-class instance we need to mine
		
		check_proof = False
		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(block.data).encode()).hexdigest()
			if hash_operation[:self.num_zeros] == ('0' * self.num_zeros):
				check_proof = True
			else:
				block.data['proof'] += 1
