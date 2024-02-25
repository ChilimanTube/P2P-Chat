# Peer To Peer Chat
### Author: Vojtěch Král

## How to run the program
1. Open terminal
2. Enter the following code:
    ```bash 
    ssh -p 20462 jouda@dev.spsejecna.net
    ```
3. Enter the password ```jooouda```
4. Enter the following code:
    ```bash
    # This will start the chat 
    sudo systemctl start chat 
    # This will show the logs of the chat
    journalctl -fu chat 
    # This will stop the chat 
    sudo systemctl stop chat
    ```
   
## Additional information
- You can find the source code in the ```/home/jouda/P2P-Chat``` directory
- If `sudo systemctl start chat` doesn't work, run ```python3 main.py``` in the ```/home/jouda/P2P-Chat``` directory
- You can configure the program in the `config.json` file in the project directory