# GameNightBot

GameNightBot is a Discord bot that provides powerful utilities and record keeping for servers hosting community game nights.

## Features

### Queryable Game Data

GameNightBot utilizes a SQLite3 database to store data on players, games, and game outcomes. This allows individual server members to receive automated answers to common queries such as:

* What game did we play last week?

* Who picked that game we played on Saturday?

* Have we really never played Catan?

![Adding a game to the played games database](img/gameHistory.png)

### Scheduling

GameNightBot provides scheduling tools to ensure nobody ever misses a game night again! Automated reminders and game master rotations provide all players with the information they need to come to each night prepared to play.

![Scheduling the next game night date and setting the game master](img/setTurn.png)

### Intuitive Emoji Input

GameNightBot gladly accepts Discord reactions as user input to commands. If prompted for verification, simply click the check mark!
