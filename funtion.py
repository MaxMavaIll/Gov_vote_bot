import subprocess
import json
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
        p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=p1.stdout)
        output, err = p2.communicate()
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

def get_vote_id_and_last_time(str_terminal: str, config: dict, vote_last_time: bool, network: str):
    get_votes = json.loads(terminal(str_terminal, config["pass"]))

    validator_add = config["addr"]

    with open(path_file_out, "r") as file:
        data = json.load(file)


    id = [] 
    for proposol in get_votes["proposals"]:
        
        if proposol["status"] == "PROPOSAL_STATUS_VOTING_PERIOD":
                

            a = proposol["proposal_id"] not in data[network]
            b = check_last_time_vote(proposol["voting_end_time"], proposol["voting_start_time"], vote_last_time)
            c = no_vote_validator("{} q gov vote {} {} {} {} -o json".format(config["bin"], proposol["proposal_id"], validator_add, config["node"], config["chain_id"]), config, proposol["proposal_id"], network)

            if a and b and c:
                try:
                    id.append(proposol["proposal_id"])
                except:
                    id.append(proposol["id"])

    return id

def get_json_file(path: str, mode: str):
    with open(path, mode) as file:
        return file

def no_vote_validator(str_terminal: str, config: dict, id: str | int, network: str):
    try:
        votes = json.loads(terminal(str_terminal))#.format(config["bin"], config["from"], config["keyring"]))
        votes = votes["options"]["option"].title().replace("_", "")
        logging.info("Validator: {} | {} has already voted {} from {}".format(config["from"], config["addr"], votes, id))
        with open("out.json", "r") as file:
            date = json.load(file)
        
        date[network].append(id)
        with open("out.json", "w") as file:
            json.dump(date, file)
        
        return False
    
    except:
        logging.info("Validator: {} | {} hasn`t voted {} from {} yet")
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

        if config[network]["fees"] != "":
            config[network]["fees"] = "--fees " + config[network]["fees"]
        if config[network]["node"] != "":
            config[network]["node"] = "--node " + config[network]["node"]
        if config[network]["chain_id"] != "":
            config[network]["chain_id"] = "--chain-id " + config[network]["chain_id"]
        if config[network]["from"] != "":
            config[network]["from"] = "--from " + config[network]["from"]
        if config[network]["keyring"] != "":
            config[network]["keyring"] = "--keyring-backend " + config[network]["keyring"]
        

        config[network]["explorer"] = config[network]["explorer"].replace(" ", "").split(",")
        
        config[network]["addr"] = terminal("{} keys show {} -a {} ".format(config[network]["bin"], config[network]["from"].replace("--from ", ""), config[network]["keyring"]), config[network]["pass"])
    

        check_existing_file(network)
        
        # config[network]["vote"] = get_variant_with_more_votes()

        # vote_split = config[network]["vote"].split(",")
        # if len(config[network]["vote"].split(",")) == 1:
        #     if "".sw

        # if config[network]["vote"].lower() in ['none', 'yes', 'no'] :
        #     config[network]["vote"] = config[network]["vote"].lower()

        # else:
        #     data = config[network]["vote"].lower().replace(" ", "").split(",")
        #     for index in range(len(data)):
        #         data[index] = data[index].split("-")
        
        #     config[network]["vote"] = data
    # dict["vote_last_moment"] = save
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
    



def check_voted(network: str, id: str, configs: list | str):

   
    with open(path_file_out, "r") as file:
        data = json.load(file)
    # print(type(configs), type(list))
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
    
def save_vote(network: str, id: str):
    if exists(path_file_out):
        pass


def vote_for_proposal(str_terminal: str, config: dict, network: str, id: str):
    

    try:
        output = terminal(str_terminal, config["pass"])
        data = json.loads(output)

        write_file(network, id)
        
        return {"txhash": config['explorer'][0] + data["txhash"],
                                "name": config["from"].replace("--from ", ""), 
                                "proposol": config['explorer'][1] + id}
    except Exception as error:
        name = config["from"]
        addr = config["addr"]
        logging.info(f"Proposol {id} not vote\nValidator: {name} | {addr}")
        return {"txhash": f"Proposol {id} not vote\nValidator: {name} | {addr}", 
                "name": config["from"].replace("--from ", ""),
                "proposol": config['explorer'][1] + id}

def send_to_server(get_data_txhash: dict):
    
    logging.info(f"{get_data_txhash != {}}")
    if get_data_txhash != {}:
        try:
            usr_server(get_data_txhash)
            get_data_txhash = {}
        except Exception as error:
            logging.info(f"Error server:\n{error}")
            logging.info(f"I save get_data_txhash\n{get_data_txhash}")

def check_last_time_vote(time_isoparse_finish: str, time_isoparse_start: str, vote_last_time: bool):

    if vote_last_time:
        date = parser.isoparse(time_isoparse_finish).replace(tzinfo=None)
        now = datetime.utcnow()
        date = date - now

        if date <= timedelta(hours=2):
            return True
        
        return False
    else:
        date = parser.isoparse(time_isoparse_start).replace(tzinfo=None)
        now = datetime.utcnow()
        date = now - date

        if date >= timedelta(hours=5):
            return True
        
        return False


def get_num_vote(votes: json):

    mass = {}

    for num, value in enumerate( votes["votes"]):
        gov = value["options"][0]["option"]
        print(f"{num}. {gov}")

        t_v_vote = gov.split("_", 2)[-1]
        if t_v_vote not in mass.keys():
            mass[t_v_vote] = 0

        mass[t_v_vote] += 1

    return mass

def get_variant_with_more_votes(srt_terminal: str) -> str:
    votes = json.loads(terminal(srt_terminal))

    num_variant = get_num_vote(votes)

    max_votes = max(list(num_variant.values()))

    for key in num_variant.keys():
        if num_variant[key] == max_votes:
            return key.title().replace("_", "")

