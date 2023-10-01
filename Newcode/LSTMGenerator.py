#Model Architecture

import torch
import torch.nn as nn

class LSTMGenerator(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMGenerator, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.output_layer = nn.Linear(hidden_size, output_size)
    
    def forward(self, input, hidden):
        output, hidden = self.lstm(input, hidden)
        output = self.output_layer(output)
        return output, hidden

#Training Loop

def train(model, data_loader, num_epochs, learning_rate):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(num_epochs):
        hidden = None
        for inputs, targets in data_loader:
            optimizer.zero_grad()
            output, hidden = model(inputs, hidden)
            loss = criterion(output.view(-1, output.size(2)), targets.view(-1))
            loss.backward()
            optimizer.step()
