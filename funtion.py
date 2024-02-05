import subprocess
import json
import toml
import logging
from os.path import exists, abspath
from user_socket.user import usr_server
from dateutil import parser
from datetime import timedelta, datetime


path_file_out=abspath("out.json")
# get_data_txhash = {}

def terminal(cmd: str = None, password: str = "None"):
    try:
        cmd = cmd.split()
        p1 = subprocess.Popen(["echo", password], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=p1.stdout)
        output = p2.communicate()
        p1.stdout.close()
        p2.stdout.close()
        if output[0].decode('utf-8') != '':
            return output[0].decode('utf-8')
        elif output[1].decode('utf-8') != '':
          return output[1].decode('utf-8')[:200]
    except Exception as error:
        logging.error("error Terminal\n", error)


def get_config() -> json:
    with open("config.json", "r") as file:
        jsn = json.load(file)
        toml.load(file)
    
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

def check_right_key(proposol: dict):

    try:
        return int(proposol["proposal_id"])
    except:
        return int(proposol["id"])

def get_vote_id_and_last_time(str_terminal: str, config: dict, vote_last_time: bool, network: str):
    logging.debug(f"{str_terminal}")
    get_votes = json.loads(terminal(str_terminal, config["pass"]))

    validator_add = config["addr"]

    with open(path_file_out, "r") as file:
        data = json.load(file)


    id = [] 
    for proposol in get_votes["proposals"]:
        
        proposal_id = check_right_key(proposol)

        a = proposal_id not in data[network]

        if proposol["status"] == "PROPOSAL_STATUS_VOTING_PERIOD" and a:
                
            logging.info("This proposle {} has been voted: {}".format(proposal_id, proposal_id in data[network]))

            b = check_last_time_vote(proposol["voting_end_time"], proposol["voting_start_time"], vote_last_time)
            c = no_vote_validator("{} q gov vote {} {} {} {} -o json".format(config["bin"], proposal_id, validator_add, config["node"], config["chain_id"]), config, proposal_id, network)


            if b and c:

                id.append(proposal_id)
                
    return id

def get_json_file(path: str, mode: str):
    with open(path, mode) as file:
        return file

def no_vote_validator(str_terminal: str, config: dict, id: str | int, network: str):
    try:
        logging.debug(f"{str_terminal}")
        votes = json.loads(terminal(str_terminal))#.format(config["bin"], config["from"], config["keyring"]))
        votes = votes["options"][0]["option"].title().replace("_", "")
        logging.info("He has already voted {} from {} | False\n".format(votes, id))
        with open("out.json", "r") as file:
            date = json.load(file)

        if id not in date[network]:
            date[network].append(id)
            date[network].sort(reverse=True)
        
        with open("out.json", "w") as file:
            json.dump(date, file)
        
        return False
    
    except:

        logging.info(f"He hasn`t voted for {id} proposol yet | True\n")
        return True

# def in_five_hour_start(time_isoparse: str, vote_last_time: bool):
    
#     if not vote_last_time:
#         date = parser.isoparse(time_isoparse).replace(tzinfo=None)
#         now = datetime.utcnow()

#         if now - date >= 5:
#             return True
        
#         return False
#     else:

#         return False

def check_config():
    config = get_config()
    save = config["vote_last_moment"]
    del config["vote_last_moment"]

    

    for network in config.keys():
        i = 0

        if "|" in config[network]["fees"]:
            config[network]["fees"] = config[network]["fees"].replace('|', '')
            
        elif config[network]["fees"] != "":
            config[network]["fees"] = "--fees " + config[network]["fees"]

        if config[network]["node"] != "":
            config[network]["node"] = "--node " + config[network]["node"]

        if config[network]["chain_id"] != "":
            config[network]["chain_id"] = "--chain-id " + config[network]["chain_id"]

        if config[network]["from"] != "":
            config[network]["from"] = "--from " + config[network]["from"]
            
        if config[network]["keyring"] != "":
            config[network]["keyring"] = "--keyring-backend " + config[network]["keyring"]
        
        config[network]["addr"] = terminal("{} keys show {} -a {} ".format(config[network]["bin"], config[network]["from"].replace("--from ", ""), config[network]["keyring"]), config[network]["pass"]).replace("\n", "")
    

        check_existing_file(network)
    return config, save



def check_existing_file(network: str):
    # path_file = abspath(path_file_out)
    if not exists(path_file_out):
        mass = {}
        mass[network] = []
    else:
        with open(path_file_out, "r") as file:
            mass = json.load(file)

        if network not in mass:
            mass[network] = []
    

    with open(path_file_out, "w") as file:
        json.dump(mass, file)
    



# def check_voted(network: str, id: str, configs: list | str):

   
#     with open(path_file_out, "r") as file:
#         data = json.load(file)
#     # print(type(configs), type(list))
#     if type(configs) == type(list()):
#         for index, vol in enumerate(configs):
#             if int(configs[index][0]) == id and len(configs[index]) == 2:
#                 vote = configs[index][1]
#             elif int(configs[index][0]) == id and len(configs[index]) == 3:
#                 answer = False
#                 vote = configs[index][1]
#                 return answer, vote
#     elif type(configs) == type(str()):
#         vote = configs
#     #     if vote[index][0] == id and vote[index][1] == 'none':
#     #         return True

#     if network in data:
#         for out_id in data[network]:
#             if out_id == int(id) :
#                 logging.info(f"I voted for this proposol {id}")
#                 answer = True
#     else:
#         answer = False


#     return answer, vote
    
# def save_vote(network: str, id: str):
#     if exists(path_file_out):
#         pass


def vote_for_proposal(str_terminal: str, config: dict, network: str, id: str):
    

    try:
        logging.debug(f"{str_terminal}")
        output = terminal(str_terminal, config["pass"])
        data = json.loads(output)

        if data["raw_log"] != "[]":
            logging.info("Proposol error: Raw_log\n {}".format(data["raw_log"]))
            output = data["raw_log"]
            int("m")

        write_file(network, id)
         
        logging.info("I vote {}: {} Success".format(id, data["txhash"]))

    
    except Exception as error:
        name = config["from"].replace("--from ", "")
        addr = config["addr"]
        logging.info(f"Proposol {id} not vote\nValidator: {name} | {addr}")


def check_last_time_vote(time_isoparse_finish: str, time_isoparse_start: str, vote_last_time: bool):

    if vote_last_time:
        date = parser.isoparse(time_isoparse_finish).replace(tzinfo=None)
        now = datetime.utcnow()
        date = date - now

        if date <= timedelta(hours=2):
            logging.info(f"less than 2 hours until the end of time | True")

            return True
        
        logging.info(f"more than 2 hours until the end of time | False")

        return False
    else:
        date = parser.isoparse(time_isoparse_start).replace(tzinfo=None)
        now = datetime.utcnow()
        date = now - date

        if date >= timedelta(hours=5):
            logging.info(f"More than 5 hours have passed | True")

            return True
        
        logging.info(f"it hasn't been 5 hours yet | False")
        return False


def get_num_vote(votes: json):

    mass = {}

    for num, value in enumerate( votes["votes"]):
        gov = value["options"][0]["option"]

        t_v_vote = gov.split("_", 2)[-1]
        if t_v_vote not in mass.keys():
            mass[t_v_vote] = 0

        mass[t_v_vote] += 1

    return mass

def get_variant_with_more_votes(str_terminal: str) -> str:
    logging.debug(f"{str_terminal}")
    votes = json.loads(terminal(str_terminal))

    num_variant = get_num_vote(votes)

    max_votes = max(list(num_variant.values()))

    for key in num_variant.keys():
        if num_variant[key] == max_votes:
            position = key.title().replace("_", "")
            logging.info(f"Position: {position}")
            return position

