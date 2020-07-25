###############################################################################
#                                                                             #
#                                                                             #
# Opdrachtgever:    Pieter Frans                                              #
#                                                                             #
# Bouwer:           P.F. van der Vlugt                                        #
#                                                                             #
# Directory:        -                                                         #
#                                                                             #
# User:             -                                                         #
#                                                                             #
# Doel:             Present a class for a Neural Network.                     #
#                   This was created bij the book by Tariq Rashid:            #
#                   Make your own neural network                              #
#                                                                             #
# Gebruik:          -                                                         #
#                                                                             #
# Output:           -                                                         #
#                                                                             #
# Exitcode:         none                                                      #
#                   e.g. 10 - Verkeerd startopties. geen bestanden opgegeven. #
#                                                                             #
# Afhankelijkheden: -                                                         #
#                                                                             #
# Initial version:  0.0.1 - P.F. van der Vlugt                                #
#                   01-05-2018 - Initial version                              #
#        Modified:                                                            #
#                                                                             #
###############################################################################

import secrets
import numpy
# scfypy.special for the sigmoid function expit()
import scipy.special

# Neural network class definition
class neuralNetwork:

    # initialise the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # initialise the neural network
        # Set number of nodes in each input, hidden en output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        # learning rate
        self.lr = learningrate
        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)
        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to
        # node j in the next layer
        # w11 w21
        # w12 w22
        # self.wih = (numpy.random.rand(self.hnodes, self.inodes) - 0.5)
        # self.who = (numpy.random.rand(self.onodes, self.hnodes) - 0.5)
        # or updated version of the random weights
        self.wih = numpy.random.normal(0.0, pow(self.hnodes, -0.5),
                                       (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, -0.5),
                                       (self.onodes, self.hnodes))

    # train the neural network
    def train(self, inputs_list, targets_list):
        # train the neural network
        # convert inputs list to 2D array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        # error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors split by weights, recombined
        # at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)
        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors *
                                         final_outputs *
                                         (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))
        # update the weights for the links between the input and the hidden
        # layers
        self.wih += self.lr * numpy.dot((hidden_errors *
                                         hidden_outputs *
                                         (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs))

    # query the neural network
    def query(self, inputs_list):
        # query the neural network
        # convert inputs list to 2D array
        inputs = numpy.array(inputs_list, ndmin=2).T
        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

