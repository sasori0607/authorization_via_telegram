# Telegram Bot Registration
Our web application allows users to register through a Telegram bot. Users can visit our website where they will see a registration form and a link to our Telegram bot. After the user fills out the form and confirms their information, they will receive a notification from the bot on Telegram confirming their registration.

### Technologies Used
We use Python and Django to create our web application, and python-telegram-bot to create our Telegram bot. We also use a PostgreSQL database to store information about registered users.

### How it Works
When the user fills out the registration form on our website, their information is sent to the server, where it is verified and stored in the database. Then, the bot on Telegram receives a notification of a new registered user and sends a message to them confirming their registration.

Thus, our web application allows users to register through a Telegram bot, making the registration process fast and convenient.

### Getting Started
Copy code
##### Create .env.dev and .env.dev.db files in the root directory of the project and specify the required environment variables.

# Build and run the containers
docker-compose up --build

# Apply Django migrations
After running these commands, the application should be up and running on http://localhost:4444/.

##### You can check how it works by visiting our Telegram bot at https://t.me/Test_TEB_bot. You can interact with the bot by typing in commands or following the registration process. Once you have completed the registration process, you will receive a confirmation message from the bot in Telegram.
