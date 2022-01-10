# SecureChat-In-Python: A CLI Chatting Tool

SecureChat-In-Python provides you to communicate with your local friends and your Hamachi network friends when they are online.
It is a multiple network platform that supports both 'local' and 'hamachi' profiles.

To run the program, simply type "./deploy.sh" to your commandline and hit Enter.
The rest is automated and you'll see the ">>> " prompt in seconds.

There are predefined commands in the program and you can reach them if you type 'help' when the program prompt is available.
For the sake of simplicity, I've added those commands in the README.md as well.

### Python Version: Python 3.8.6

## Help:

This application is developed for LAN chatting.
When you run 'discover', a discovery signal will be sent
for all possible LAN IP addresses to receive a response
After receiving a response, the user that has responded
to you will become online for you to start chatting.
Users inside the program are stored with their <user-tag>
that is a composition of their names and their last part
of their LAN IP address.
- For Local Users:
e.g. ozgurcan-<last_octet>: ozgurcan@192.168.1.<last_octet>
- For Hamachi Users:
e.g. ozgurcan-<first_three_octet>: ozgurcan@25.<first_three_octet>

### GENERAL COMMAND LIST

- help: Opens general command.
- switch <env>: Changes into any environment, either to 'hamachi' or 'local'.
- discover: Discovers the clients in the network.
- profile: Shows your profile.
- refresh: Refreshes and syncs with the current state.
- whoall: Shows all users' profiles.
- impall: Shows all imposters' profiles.
- imptags: Shows all imposters' tags.
- whoshow <user_tag>: Shows the profile of user with tag <user_tag>.
- impshow <imp_tag>: Shows the profile of imposter with tag <imp_tag>.
- whoisonline: Shows all available users in LAN.
- sendmsg <user_tag> <your_msg>: Sends message to the user with tag <user_tag>
    - sendmsg can send messages with length at most 140 characters.
- respond <imp_tag>: Sends respond to a known impostor as <imp_tag>
- validate <imp_tag>: Validate a known impostor known as <imp_tag> to a user known as <user_tag>
- chathist <user_tag>: Opens chat history with <user_tag>
- dumphist <user_tag>: Dumps chat history in a .txt file