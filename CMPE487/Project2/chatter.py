import os
import re
import copy
import json
import time
import emoji
import queue
import socket
import threading
import netifaces
from datetime import datetime


profile_dict = {}
chat_dict = {}
msg_formats = {}
ip_dict = {}
new_msg_dict = {}

msg_queue = queue.Queue()
profile_struct = {"tag": "", "name": "", "ip": "", "isActiveStatus": False}

isSelfOnline = True
isExit = False
isNotified = True
isLocal = True
listenPid = 5
PORT = 12345


def entry():
    print("Welcome to Chat-In-Python!")
    print("It is a local area chatting application on the commandline.")
    print("P.S. : Environment set 'local' by default.")
    print("For further help, type 'help' and Enter.")
    print("To exit, type 'exit' and Enter.")


def helpy():
    print("- This application is developed for LAN chatting.")
    print("- When you become online, a discovery signal will be sent")
    print("for all possible LAN IP addresses to receive a response")
    print("- After receiving a response, the user that has responded")
    print("to you will become online for you to start chatting.")
    print("- Users inside the program are stored with their <user-tag>")
    print("that is a composition of their names and their last part")
    print("of their LAN IP address.")
    print("e.g. {} ozgurcan-25: ozgurcan@192.168.1.25".format(emoji.emojize(":bust_in_silhouette:")))
    print("-" * 56)
    print(" - GENERAL COMMAND LIST - ")
    print("help:\t\t\t\t Opens general command.")
    print("switch <env>:\t\t\t Changes into any environment.")
    print("\t\t\t\t Either to 'hamachi' or 'local'.")
    print("discover:\t\t\t Discovers the clients in the network.")
    print("profile:\t\t\t Shows your profile.")
    print("whoall:\t\t\t\t Shows all users' profiles.")
    print("show <user_tag>:\t\t Shows the profile of user with")
    print("\t\t\t\t tag <user_tag>.")
    print("whoisonline:\t\t\t Shows all available users in LAN.")
    print("sendmsg <user_tag> <your_msg>:\t Sends message to the user with")
    print("\t\t\t\t tag <user_tag> and message between asterisks.")
    print("chathist <user_tag>:\t\t Opens chat history with <user_tag>")
    print("dumphist <user_tag>:\t\t Dumps chat history in a .txt file")


def ip_extractor():
    ip_list = []
    for if_name in netifaces.interfaces():
        for ip in netifaces.ifaddresses(if_name).get(netifaces.AF_INET, ()):
            ip_list.append(ip["addr"])
    return ip_list


def ip_regex(ip_list):
    global ip_dict
    local_pat = re.compile("^192.168.1.[0-9]{1,3}$")
    hamachi_pat = re.compile("^25.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$")
    for ip in ip_list:
        hamachi_match = hamachi_pat.match(ip)
        local_match = local_pat.match(ip)
        if hamachi_match is not None:
            ip_dict["hamachi"] = hamachi_match.group()
        if local_match is not None:
            ip_dict["local"] = local_match.group()


def switch(env):
    global isLocal
    if env == "local":
        isLocal = True
        env_params("local")
    elif env == "hamachi":
        isLocal = False
        env_params("hamachi")
    else:
        print("Invalid environment. Set to 'local' by default.")
        isLocal = True
        env_params("local")


def hamachi_ip_extract():
    hamachi_ip_file = open("./hamachi_ip_list.txt", "r")
    hamachi_ipl = [hip.strip() for hip in hamachi_ip_file.readlines()]
    hamachi_ip_file.close()
    return hamachi_ipl


def discover():
    if isLocal:
        local_discover()
    else:
        hamachi_discover(hamachi_ip_list)


def env_params(env):
    global profile_dict, ip_dict
    ip_regex(ip_extractor())
    user_name = os.getenv("USER")
    user_ip = ip_dict[env]
    if env == "hamachi":
        user_identifier = ".".join(user_ip.split(".")[1:])
    elif env == "local":
        user_identifier = user_ip.split(".")[-1]
    else:
        raise ValueError("There's no suitable IP address in this platform. Aborted.")

    user_tag = str(user_name).upper() + "-" + str(user_identifier)
    profile_dict["self"] = {"tag": user_tag, "isActiveStatus": False, "name": user_name, "ip": user_ip}
    msg_formatting("self")


def msg_formatting(user_tag):
    global msg_formats
    profile = profile_dict[user_tag]
    discovery = {"NAME": profile["name"], "MY_IP": profile["ip"], "TYPE": "DISCOVER", "PAYLOAD": ""}
    response = {"NAME": profile["name"], "MY_IP": profile["ip"], "TYPE": "RESPOND", "PAYLOAD": ""}
    message = {"NAME": profile["name"], "MY_IP": profile["ip"], "TYPE": "MESSAGE", "PAYLOAD": ""}
    msg_formats["discovery"] = discovery
    msg_formats["response"] = response
    msg_formats["message"] = message


def cmd_input_analysis(cmd_input):
    input_tokens = str(cmd_input).split()
    if len(input_tokens) == 0:
        return
    input_tokens[0] = input_tokens[0].lower()
    if input_tokens[0] == "profile":
        profile_disp()
    elif input_tokens[0] == "refresh":
        print("{} Checking for new messages."
              .format(emoji.emojize(":tropical_drink:")))
    elif input_tokens[0] == "help":
        helpy()
    elif input_tokens[0] == "switch":
        switch(input_tokens[1].lower())
    elif input_tokens[0] == "discover":
        discover()
    elif input_tokens[0] == "whoisonline":
        who_is_online()
    elif input_tokens[0] == "whoall":
        who_all()
    elif input_tokens[0] == "show":
        show_profile(input_tokens[1].lower())
    elif input_tokens[0] == "sendmsg":
        send_message(" ".join(input_tokens[1:]))
    elif input_tokens[0] == "chathist":
        chat_history(input_tokens[1].lower())
    elif input_tokens[0] == "dumphist":
        dump_history(input_tokens[1].lower())
    else:
        print("Invalid input. Try again!")


def tag_generator(name, ip):
    hamachi_pat = re.compile("^25.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$")
    local_pat = re.compile("^192.168.1.[0-9]{1,3}$")
    if local_pat.match(ip) is not None:
        ip_identifier = str(ip).split(".")[-1]
        return "-".join([name, ip_identifier])
    else:
        if hamachi_pat.match(ip) is not None:
            ip_identifier = ".".join(str(ip).split(".")[1:])
            return "-".join([name, ip_identifier])


def profile_disp():
    if isSelfOnline:
        print(emoji.emojize("Status Information: Online :green_apple:"))
        print("Number of Active Chats: {}".format(count_active_chat()))
    else:
        print(emoji.emojize("Status Information: Offline :red_circle:"))
    print(emoji.emojize(" - PROFILE INFO :eyes: -"))
    print("{} User Tag:\t\t\t {}".format(emoji.emojize(":thumbs_up:"), str(profile_dict["self"]["tag"]).upper()))
    print("{} User Name:\t\t\t {}".format(emoji.emojize(":thumbs_up:"), profile_dict["self"]["name"]))
    print("{} User IP:\t\t\t {}".format(emoji.emojize(":thumbs_up:"), profile_dict["self"]["ip"]))


def show_profile(user_tag):
    print(emoji.emojize(" - PROFILE INFO :eyes: -"))
    print("{} User Tag:\t\t\t {}".format(emoji.emojize(":thumbs_up:"), str(profile_dict[user_tag]["tag"]).upper()))
    print("{} User Name:\t\t\t {}".format(emoji.emojize(":thumbs_up:"), profile_dict[user_tag]["name"]))
    print("{} User IP:\t\t\t {}".format(emoji.emojize(":thumbs_up:"), profile_dict[user_tag]["ip"]))


def who_all():
    for tag in profile_dict.keys():
        if tag != "self":
            p = profile_dict[tag]
            print("{} User Tag:{}\t User Name:{}\t User IP:{}"
                  .format(emoji.emojize(":eyes:"), p["tag"], p["name"], p["ip"]))


def count_active_chat():
    active_tags = [tag for tag, chat in chat_dict.items() if len(chat) != 0 and profile_dict[tag]["isActiveStatus"]]
    return len(active_tags)


def who_is_online():
    active_users = [user["tag"] for tag, user in profile_dict.items() if tag != "self" and user["isActiveStatus"]]
    for user in active_users:
        print(emoji.emojize(":bust_in_silhouette: {}".format(user)))


def send_message(msg_info):
    global chat_dict
    msg_info_tokens = msg_info.split()
    recipient_tag = msg_info_tokens[0].lower()
    if recipient_tag not in profile_dict.keys():
        print("The recipient is not recognized. Check the user tag.")
        return
    recipient_profile = profile_dict[recipient_tag]
    msg = " ".join(msg_info_tokens[1:])
    if len(msg) > 140:
        print("Message can be composed with at most 140 characters.")
        return
    chat_dict[recipient_tag].append("+ " + str(msg))
    msg_obj = copy.deepcopy(msg_formats["message"])
    msg_obj["PAYLOAD"] = msg
    msg_obj_srl = json.dumps(msg_obj)

    try:
        socket_send(msg_obj_srl, recipient_profile["ip"])
        print("{} Your message is sent!".format(emoji.emojize(":fire:")))
    except socket.timeout:
        print("{} User with tag {} is not online right now. Try again!"
              .format(emoji.emojize(":no_entry:"), recipient_tag))
        pass


def local_discover():
    global ip_dict
    my_ip = ip_dict["local"].split(".")[-1]
    disc_obj = copy.deepcopy(msg_formats["discovery"])
    disc_obj_srl = json.dumps(disc_obj)
    for ip in range(1, int(my_ip)):
        try:
            socket_send(disc_obj_srl, "192.168.1.{}".format(ip))
        except socket.timeout:
            print("{} User with ip {} is not online right now. Try again!"
                  .format(emoji.emojize(":no_entry:"), "192.168.1.{}".format(ip)))
        except ConnectionRefusedError:
            pass
    for ip in range(int(my_ip)+1, 255):
        try:
            socket_send(disc_obj_srl, "192.168.1.{}".format(ip))
        except socket.timeout:
            print("{} User with ip {} is not online right now. Try again!"
                  .format(emoji.emojize(":no_entry:"), "192.168.1.{}".format(ip)))
        except ConnectionRefusedError:
            pass
    print("{} Local client discovery completed!".format(emoji.emojize(":globe_with_meridians:")))


def hamachi_discover(ip_list):
    hamachi_obj = copy.deepcopy(msg_formats["discovery"])
    hamachi_obj_srl = json.dumps(hamachi_obj)
    for ip in ip_list:
        try:
            socket_send(hamachi_obj_srl, ip)
        except socket.timeout:
            print("{} User with ip {} is not online right now. Try again!"
                  .format(emoji.emojize(":no_entry:"), ip))
        except ConnectionRefusedError:
            pass
    print("{} Hamachi client discovery completed!".format(emoji.emojize(":mushroom:")))


def extract_profile(msg):
    tag = tag_generator(msg["NAME"], msg["MY_IP"])
    new_profile = copy.deepcopy(profile_struct)
    new_profile["tag"] = tag
    new_profile["name"] = msg["NAME"]
    new_profile["ip"] = msg["MY_IP"]
    new_profile["isActiveStatus"] = True
    return new_profile, tag


def discovery_actions(msg):
    new_profile, tag = extract_profile(msg)
    rsp_obj = msg_formats["response"]
    rsp_obj_srl = json.dumps(rsp_obj)
    try:
        socket_send(rsp_obj_srl, msg["MY_IP"])
    except socket.timeout:
        print("{} User with ip {} is not online right now. Try again!"
              .format(emoji.emojize(":no_entry:"), msg["MY_IP"]))
    except ConnectionRefusedError:
        pass
    profile_dict[tag] = new_profile
    chat_dict[tag] = []


def response_actions(msg):
    new_profile, tag = extract_profile(msg)
    profile_dict[tag] = new_profile
    chat_dict[tag] = []


def message_actions(msg):
    global chat_dict, new_msg_dict
    tag = tag_generator(msg["NAME"], msg["MY_IP"])
    message = "- " + str(msg["PAYLOAD"])
    if tag not in chat_dict.keys():
        chat_dict[tag] = []
    chat_dict[tag].append(message)
    if tag not in new_msg_dict.keys():
        new_msg_dict[tag] = 0
    new_msg_dict[tag] += 1


def new_msg_count():
    global isNotified
    if not isNotified:
        print("{} You have new messages!".format(emoji.emojize(":bell:")))
        for tag, nmc in new_msg_dict.items():
            print("{} {} message(s) from {}".format(emoji.emojize(":paperclip:"), nmc, profile_dict[tag]["name"]))


def chat_history(user_tag):
    global chat_dict, isNotified, new_msg_dict
    isNotified = True
    new_msg_dict[user_tag] = 0
    history = chat_dict[user_tag]
    for msg_line in history:
        print(msg_line)


def dump_history(user_tag):
    global chat_dict
    history = chat_dict[user_tag]
    da_ti = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    f_name = user_tag + "-" + da_ti + ".txt"
    dump = open(f_name, "w")
    for msg in history:
        dump.write(msg)
        dump.write("\n")
    dump.flush()
    dump.close()


def listener_func():
    global isExit
    while True:
        if isExit:
            break
        socket_listen()


def message_parse():
    global isNotified
    raw_message = msg_queue.get()

    dcd_msg = raw_message.decode("utf-8")
    if dcd_msg != "\n" and dcd_msg != "\r":
        message = dcd_msg.strip("\n")
    else:
        return

    try:
        msg = json.loads(message)
    except json.decoder.JSONDecodeError:
        return
    if msg["TYPE"] == "DISCOVER":
        discovery_actions(msg)
    elif msg["TYPE"] == "RESPOND":
        response_actions(msg)
    elif msg["TYPE"] == "MESSAGE":
        isNotified = False
        message_actions(msg)
    else:
        print("Invalid message type")


def messenger_func():
    while True:
        if isExit:
            break
        message_parse()


def socket_listen():
    if isLocal:
        host_ip = ip_dict["local"]
    else:
        host_ip = ip_dict["hamachi"]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host_ip, 12345))
        sock.listen()
        in_conn, addr = sock.accept()
        with in_conn:
            while True:
                in_data = in_conn.recv(1024)
                if in_data:
                    msg_queue.put_nowait(in_data)
                else:
                    break


def socket_send(msg, recp_ip):
    raw_msg = str(msg) + "\n"
    enc_msg = raw_msg.encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(1)
    sock.connect((recp_ip, 12345))
    sock.sendall(enc_msg)
    sock.close()


def terminate():
    for i in range(0, 2):
        print("\r{} | Prepare to shutdown down gracefully...".format(emoji.emojize(":floppy_disk:")), end=" ")
        time.sleep(.3125)
        print("\r{} / Prepare to shutdown down gracefully...".format(emoji.emojize(":floppy_disk:")), end=" ")
        time.sleep(.3125)
        print("\r{} - Prepare to shutdown down gracefully...".format(emoji.emojize(":floppy_disk:")), end=" ")
        time.sleep(.3125)
        print("\r{} \\ Prepare to shutdown down gracefully...".format(emoji.emojize(":floppy_disk:")), end=" ")
        time.sleep(.3125)
    print("\r\n", end=" ")
    print("\r{} You are exiting in 5 seconds...".format(emoji.emojize(":koala:")), end=" ")
    time.sleep(1)
    print("\r{} You are exiting in 4 seconds...".format(emoji.emojize(":penguin:")), end=" ")
    time.sleep(1)
    print("\r{} You are exiting in 3 seconds...".format(emoji.emojize(":boar:")), end=" ")
    time.sleep(1)
    print("\r{} You are exiting in 2 seconds...".format(emoji.emojize(":camel:")), end=" ")
    time.sleep(1)
    print("\r{} You are exiting in 1 seconds...".format(emoji.emojize(":bird:")), end=" ")
    time.sleep(1)
    print("\r\n", end=" ")
    print("\r{} Till next time!".format(emoji.emojize(":monkey:")), end=" ")


if __name__ == "__main__":
    entry()
    hamachi_ip_list = hamachi_ip_extract()
    listen_func = threading.Thread(target=listener_func)
    listen_func.daemon = True
    message_func = threading.Thread(target=messenger_func)
    message_func.daemon = True

    print("Select your environment to work: type 'local' or 'hamachi'.")
    while True:
        usr_env_input = input(">>> ")
        if usr_env_input.strip().lower() == "local":
            switch("local")
            break
        elif usr_env_input.strip().lower() == "hamachi":
            switch("hamachi")
            break
        else:
            print("{} Enter a valid environment.".format(emoji.emojize(":no_entry:")))
    listen_func.start()
    message_func.start()

    while True:
        usr_input = input(">>> ")
        if usr_input == "exit":
            isExit = True
            break
        else:
            cmd_input_analysis(usr_input)
        new_msg_count()
    print("*" * 24)
    message_func.join(1)
    listen_func.join(1)
    terminate()
