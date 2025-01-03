#Smart Sequence
Smart Sequence is based on the board game, Sequence.

It’s a 2 player game where the human will play against the computer and there are outlines of images on the board and a random card generator where they each pick cards, there are 7 cards allowed at once. To play the card, the user has to correctly enter the answer and the topic it corresponds to. The user attempts to get two sequences of 5 of topics on the board in order to win. For more context here’s a video demoing how the game is played:  https://youtu.be/jrjPYo0YhgA. One of the features is board generation - there will be a new setup of the states every time so it can be easier or more difficult to get a sequence. Additionally the computer will be playing against a human, so I have to essentially make Game AI, evaluate what the best move is at any time - also whether to block the human’s move or not. There will be a home page and a main page where the game is played. The user will be able to look at their hand by clicking at the cards symbol at the bottom of the screen, and then play their card from there. The computer will determine whether there is a win or not as well as if there is a stalemate. Another feature is users can linke Google Drive files of information (rtf) and Google Drive folders of images and they can play their own custom game.


Images necessary for this project are linked here: https://drive.google.com/drive/folders/1OYKWlWJyC83RQqGZVLiv7u4BzLm0Qvj_?usp=sharing

When running the file in the command line one should run main.py. Additionally, these are the following libraries that need to be installed: cmu_graphics, os, copy, random, pydrive, and striprtf.

ShortCut Commands: once you get two the two player game screen or player versus computer screen if you press the key 'w' or 'W' it will take you the win screen. Additionally, simply clicked the back button to navigate to the home screen will restart the game. If you press the key 's' or 'S', it will take you to the stalemate screen. On the load files screen pressing the 'up' arrow will automatically fill in a default link


To run the drive link portion you need to be enabled on My Google Auth. In that case, you can set up your own client_secrets.json on the Google Cloud Developer Platform and enable your email address to test it.
