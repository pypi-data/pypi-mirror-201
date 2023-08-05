from random import random
from math import exp
from time import time

class NeyroNet:
	def __init__(self, n_inputs, hiddens_layer, n_outputs):
		self.network = list()
		
		self.n_outputs = n_outputs
	
		hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(hiddens_layer[0])]
		self.network.append(hidden_layer)
		
		for layer in hiddens_layer[1:]:
			hidden_layer = [{'weights':[random() for i in range(len(self.network[-1])+1)]} for i in range(layer)]
			self.network.append(hidden_layer)
			
		output_layer = [{'weights':[random() for i in range(hiddens_layer[-1] + 1)]} for i in range(n_outputs)]
		self.network.append(output_layer)
	
	def activate(self, weights, inputs):
		activation = weights[-1]
		for i in range(len(weights)-1):
			activation += weights[i] * inputs[i]
		return activation
	
	def transfer(self, activation):
		return 1.0 / (1.0 + exp(-activation))
	
	def forward_propagate(self, row):
		inputs = row
		for layer in self.network:
			new_inputs = []
			for neuron in layer:
				activation = self.activate(neuron['weights'], inputs)
				neuron['output'] = self.transfer(activation)
				new_inputs.append(neuron['output'])
			inputs = new_inputs
		return inputs
	
	def transfer_derivative(self, output):
		return output * (1.0 - output)
	
	def backward_propagate_error(self, expected):
		for i in reversed(range(len(self.network))):
			layer = self.network[i]
			errors = list()
			if i != len(self.network)-1:
				for j in range(len(layer)):
					error = 0.0
					for neuron in self.network[i + 1]:
						error += (neuron['weights'][j] * neuron['delta'])
					errors.append(error)
			else:
				for j in range(len(layer)):
					neuron = layer[j]
					errors.append(expected[j] - neuron['output'])
			for j in range(len(layer)):
				neuron = layer[j]
				neuron['delta'] = errors[j] * self.transfer_derivative(neuron['output'])
	
	def update_weights(self, row, l_rate):
		for i in range(len(self.network)):
			inputs = row[:-1]
			if i != 0:
				inputs = [neuron['output'] for neuron in self.network[i - 1]]
			for neuron in self.network[i]:
				for j in range(len(inputs)):
					neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
				neuron['weights'][-1] += l_rate * neuron['delta']
	
	def train_network(self, train, l_rate, n_epoch, err_val_threshold=0, say=True):
		errors = []
		for epoch in range(n_epoch):
			timer = time()
			sum_error = 0
			for row in train:
				outputs = self.forward_propagate(row)
				expected = [0 for i in range(self.n_outputs)]
				expected[row[-1]] = 1
				sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
				self.backward_propagate_error(expected)
				self.update_weights(row, l_rate)
			v = 1 / (time() - timer)
			t = (n_epoch - epoch) / v
			m = int(t/60)
			s = int(t - m * 60)
			pdat = '>epoch=%d, lrate=%.1f, error=%.10f, %.1f' % (epoch, l_rate, sum_error, epoch/n_epoch*100) + '%, ' + f'time={m}m {s}s'
			if(say):
				print(pdat, end='\r')
			errors.append(sum_error)
			if(sum_error < err_val_threshold):
				if(say):
					print(' ' * len(pdat), end='\r')
					print('THRESHOLD WITH EPOCH > ' + str(epoch))
				break
		return errors
	
	def predict(self, row):
		outputs = self.forward_propagate(row)
		return outputs.index(max(outputs))

	def save(self, filename):
		with open(filename, 'w') as sv:
			sv.write(str(self.network))
			sv.close()

	def load(self, filename):
		with open(filename, 'r') as sv:
			data = sv.read()
			sv.close()
		self.network = eval(data)
		self.n_outputs = len(self.network[-1])
