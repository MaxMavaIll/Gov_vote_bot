import json
import funtion as f
import logging as log
import time
from environs import Env

logger = log.getLogger(__name__)

def main():
    log.basicConfig(
        level=log.DEBUG,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    
    config = f.get_config()
    f.check_config(config)
    log.debug(config)
    for network, configs in config.items():
        log.info(f"ne1twork {network}")
        to_terminal = "{} q gov proposals {} --reverse --limit 20 -o json ".format(configs["bin"], configs["node"])
        for index, id in enumerate( f.get_vote_id(json.loads(f.terminal(to_terminal, config[network]["pass"])))):
            answer, vote = f.check_voted(network, id, configs["vote"])
            if not answer:
                to_terminal = "{} tx gov vote {} {} {} {} {} {} {} -o json -y".format(configs["bin"], vote, id, configs["fees"], configs["node"], 
                                                                        configs["chain_id"], configs["keyring"], configs["from"])
                log.info(f"Command {to_terminal}")
                f.form_request(f.terminal(to_terminal, config[network]["pass"]), network, id, config[network]['explorer'][0],
                           config[network]['explorer'][1], config[network]['from'].replace("--from ", ""))
                time.sleep(10)

            else:
                log.info(f"I skip Network {network}. And this proposol {id}")
        f.send_to_server()
            
if __name__ == "__main__":
    main()
