# AIRockPaperScissors
Rock paper scissors against a learning agent. User input is by camera.




https://github.com/user-attachments/assets/00d364eb-4b47-4609-9a39-f7726cc8e43c

Processing, which runs the games GUI, and Python communicate through sockets on the local machine. 

The computer learns the pattern of behaviour using a collection of different models. 

The first model randomly returns any move.

The second model returns the most frequently played move.

Remaining models are Neural Networks. The input to the models will be the last n moves the user has made, and they have varying hidden layers. 
The output of the Neural Networks will always be the next move the model predicts the user will make.
