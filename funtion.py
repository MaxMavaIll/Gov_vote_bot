import subprocess
import json
import logging
from os.path import exists, abspath
from user_socket.user import usr_server

path_file_out=abspath("out.json")
get_data_txhash = {}

def terminal(cmd: str = None, password: str = None):
    try:
        print("start")
        cmd = cmd.split()
        p1 = subprocess.Popen(["echo", password], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=p1.stdout)
        output, err = p2.communicate()
        print("erro1", err)
        p1.stdout.close()
        p2.stdout.close()
        return output.decode('utf-8')
    except Exception as error:
        logging.error("error\n", error)


def get_config() -> json:
    with open("config.json", "r") as file:
        jsn = json.load(file)
    
    return jsn

def write_file(network: str, id: str):
    with open(path_file_out, "r") as file:
        data = json.load(file)
    
    if network in data:
        if int(id) not in data[network]:
            data[network].append(int(id))
    else:
        data[network] = [int(id)]
    
    data[network].sort(reverse=True)
    with open(path_file_out, "w") as file:
        json.dump(data, file)

def get_vote_id(dict: dict):
    id = []
    for proposol in dict["proposals"]:
        if proposol["status"] == "PROPOSAL_STATUS_VOTING_PERIOD":
            id.append(proposol["proposal_id"])

    return id


def check_config(dict: dict):
    mass = ["", "--fees ", "--node ", "--chain-id ", "--from ", "--keyring-backend ", "", "", ""]
    for network, configs in dict.items():
        i = 0
        for key in configs:
            if configs[key] != "":
                dict[network][key] = mass[i] + configs[key]
            i+=1

        dict[network]["explorer"] = dict[network]["explorer"].replace(" ", "").split(",")
        if dict[network]["vote"].lower() in ['none', 'yes', 'no'] :
            dict[network]["vote"] = dict[network]["vote"].lower()

        else:
            data = dict[network]["vote"].lower().replace(" ", "").split(",")
            for index in range(len(data)):
                data[index] = data[index].split("-")
        
            dict[network]["vote"] = data

def check_existing_file(path_from_main_dir: str = ""):
    path_file = abspath(path_from_main_dir)
    if not exists(path_file):
        with open(path_file, "w") as file:
            json.dump({}, file)
   
    return True
    



def check_voted(network: str, id: str, configs: list | str):
    vote = answer = 'yes'
    if check_existing_file("out.json") and configs != "none":
        with open(path_file_out, "r") as file:
            data = json.load(file)
        print(type(configs), type(list))
        if type(configs) == type(list()):
            for index, vol in enumerate(configs):
                if int(configs[index][0]) == id and len(configs[index]) == 2:
                    vote = configs[index][1]
                elif int(configs[index][0]) == id and len(configs[index]) == 3:
                    answer = False
                    vote = configs[index][1]
                    return answer, vote
        elif type(configs) == type(str()):
            vote = configs
        #     if vote[index][0] == id and vote[index][1] == 'none':
        #         return True

        if network in data:
            for out_id in data[network]:
                if out_id == int(id) :
                    logging.info(f"I voted for this proposol {id}")
                    answer = True
        else:
            answer = False


        return answer, vote
    else:
        return answer, None

def save_vote(network: str, id: str):
    if exists(path_file_out):
        pass


def form_request(text: bytes, network: str, id: str, url_explorer_tx: str,
                url_explorer_proposol: str, name:str):
    
    try:
        data = json.loads(text)
        get_data_txhash[id] = {"txhash": url_explorer_tx + data["txhash"],
                                "name": name, 
                                "proposol": url_explorer_proposol + id}

        write_file(network, id)
        logging.info(f"Proposle {id} {data}")
    except Exception as error:
        logging.error("error\n", error)

def send_to_server():
    global get_data_txhash
    logging.info(f"{get_data_txhash != {}}")
    if get_data_txhash != {}:
        usr_server(get_data_txhash)
        get_data_txhash = {}
