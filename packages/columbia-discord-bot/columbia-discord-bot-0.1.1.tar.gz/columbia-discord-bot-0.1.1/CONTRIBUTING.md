# Contributing

## Prerequisites
<<<<<<< HEAD
1. Have ```python``` installed
2. Have your own Discord token, this can be obtained at the Discord development portal.
3. You've installed the discord module in python using ```pip install discord```

## Getting Started
1. Fork this repo's main branch
2. Then, clone this repo in your local environment by typing ```git clone https://github.com/<your_username>/columbia-discord-bot.git.
3. Install necessary dependencies by using ```make develop```
4. Create a branch for your changes by using ```git checkout -b <branch_name>
=======
1. Have ```Python 3.7``` or greater installed
2. Have your own Discord token, which can be obtained at the Discord development portal.
3. You've installed the discord module in Python using the command ```pip install discord``` or something similar in your local environment.

## Getting Started
1. Fork this repo's main branch
2. Clone this repo using the command: ```git clone https://github.com/<your_username>/columbia-discord-bot.git.```
3. Install necessary dependencies by using ```make develop```
4. Create a branch for your changes by using ```git checkout -b <branch_name>```
>>>>>>> 3f8e6ed43ce9602a7028ac8cdb1b87f8ddb20cb0
5. You need to create your own ```config.json``` file in the project folder. In that file, write ```{"token": "Your-Discord-Token"}```. Replace "Your-Discord-Token" with your Discord token.

## Pull Requests
Make sure to run these commands before opening a pull request:
<<<<<<< HEAD
1. ```make lint```
2. ```make format```
3. ```make check```
4. ```make tests```

If all pass, you are ready to commit your changes and open a pull request.
=======
1. Run the linter ```make lint``` to run a static analysis.
2. You can use ```make format``` to auto format.
3. Run ```make check``` to check that the packages are all correct.
4. Run ```make tests``` to make sure your code passes all tests.

Once you have ran these commands, you are ready to commit your changes and open a pull request.
>>>>>>> 3f8e6ed43ce9602a7028ac8cdb1b87f8ddb20cb0

In your PR, please provide a title and a description of your changes.
