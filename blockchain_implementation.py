import datetime
import random
import string
import hashlib
import json
import timeit
from unittest import case

from numpy import block

class Block:
	def __init__(self, index, proof, previous_hash):
		self.children = []
		self.data = {
			'index': index,
			'timestamp': str(datetime.datetime.now()),
			'transaction': ''.join(random.choices(string.ascii_lowercase, k=50)),
			'proof': proof,
			'previous hash': previous_hash
		}

	# def generate_rand_trans(self):
	# 	return ''.join(random.choices(string.ascii_lowercase, k=50))

class Blockchain:
	def __init__(self):
		# Initialize genesis block
		self.first_block = Block(0, 1, '0')
		self.length = 1
		self.last_block = self.first_block

		# Find the appropriate number of hash zeros
		print("Calculating appropriate puzzle complexity for this hardware...")
		# self.num_zeros = self.calc_zeros()
		self.num_zeros = 4 #for trial purposes only TODO change this shit
		print("Determined complexity is", self.num_zeros, "zeros for successful hash mine")
	

	# Functions that help initialize the num_zeros variable that controls complexity
	def proof_of_work_test(self, N):
		proof = 0
		dummy_block = {
			'index': 9,
			'timestamp': str(datetime.datetime.now()),
			'transactions': ''.join(random.choices(string.ascii_lowercase, k=50)),
			'proof': proof,
			'previous_hash': 69841654198}

		check_proof = False
		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(json.dumps(dummy_block, sort_keys=True)).encode()).hexdigest()
			
			if hash_operation[:N] == '0'*N:
				check_proof = True
			else:
				# proof += 1
				dummy_block['proof']+=1


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
			Block(
				self.last_block.data['index'] + 1,
				0,
				self.hash(self.last_block)))
		self.proof_of_work(self.last_block.children[0])
		self.last_block = self.last_block.children[0]
		self.length+=1
	

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


	def print_chain(self, block):
		output = []
		output.append(block.data)
		if(len(block.children) == 0):
			return output
		elif(len(block.children) == 1):
			output += self.print_chain(block.children[0])
			return output
		else:
			branches = {}
			for i in range(len(block.children)):
				key = 'branch ' + str(i)
				branches[key] = self.print_chain(block.children[i])
			output.append(branches)
			return output

	
	def attempt_hash(self, block):
		hash_operation = hashlib.sha256(
			str(block.data).encode()).hexdigest()

		if hash_operation[:self.num_zeros] == ('0' * self.num_zeros):
			return True
		else:
			block.data['proof'] += 1
			return False


	def proof_race(self, attack_block, good_block):
		attacker_success = False
		good_success = False
		while(attacker_success != True and good_success != True):
			if(self.attempt_hash(attack_block)): 
				attacker_success = True
				break
			if(self.attempt_hash(attack_block)): 
				attacker_success = True
				break
			if(self.attempt_hash(good_block)): 
				good_success = True
				break
		if(attacker_success): return 1
		if(good_success): return 0

	
	def simulate_attack(self):
		branch_block = self.last_block
		branch_block.children.append(
			Block(
				self.last_block.data['index'] + 1,
				0,
				self.hash(self.last_block)))
		last_good_block = branch_block.children[0]
		# good_block not verified
		branch_block.children.append(
			Block(
				self.last_block.data['index'] + 1,
				0,
				self.hash(self.last_block)))
		branch_block.children[1].data['transaction'] = "This is a transaction made by the attacker"
		last_attack_block = branch_block.children[1]
		
		# start of the proof race
		attack_success = self.proof_race(last_attack_block, last_good_block)
		
		while(True):
			new_block = Block(
						0,
						0,
						0)
			if(attack_success):
				new_attack_block = new_block
				new_attack_block.data['index'] = last_attack_block.data['index'] + 1
				new_attack_block.data['previous_hash'] = self.hash(last_attack_block)
				last_attack_block.children.append(new_block)
				# last_attack_block.children[0].data['transaction'] = "This is a transaction made by the attacker"
				last_attack_block = last_attack_block.children[0]
			else:
				new_good_block = new_block
				new_good_block.data['index'] = last_good_block.data['index'] + 1
				new_good_block.data['previous_hash'] = self.hash(last_good_block)
				last_good_block.children.append(new_good_block)
				last_good_block = last_good_block.children[0]
			attack_success = self.proof_race(last_attack_block, last_good_block)
			if((attack_success and last_attack_block.data['index'] >= branch_block.data['index'] + 3)
				or( (not attack_success) and last_good_block.data['index'] >= branch_block.data['index'] + 3)):
				break
		
		if(attack_success):
			# print("attack success")
			last_good_block.data['transaction'] += "    Failed to prove"
			
			self.last_block = last_attack_block
			self.length = last_attack_block.data['index'] + 1
			return True
		else:
			# print("valid success")
			last_attack_block.data['transaction'] += "    Failed to prove"

			self.last_block = last_good_block
			self.length = last_good_block.data['index'] + 1
			return False


if __name__ == '__main__':
	bc = Blockchain()
	# bc.add_block()
	# bc.add_block()
	# bc.add_block()
	# bc.add_block()
	# attack_success = bc.simulate_attack()
	# bc.add_block()
	# print(json.dumps({'Blockchain': bc.print_chain(bc.first_block)}, indent=4))
	# if(attack_success): print("Attack successful")
	while(True):
		command = input("Please enter commend(add/simulate attack/print/exit):")
		if(command == 'add'):
			bc.add_block()
		elif(command == 'simulate attack'):
			bc.simulate_attack()
		elif(command == 'print'):
			print(json.dumps({'Blockchain': bc.print_chain(bc.first_block)}, indent=4))
		elif(command == 'exit'):
			break
		else:
			print("Command not recognized")