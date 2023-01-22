import json
import funtion as f
import logging as log

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
        log.info(f"network {network}")
        to_terminal = "{} q gov proposals {} --reverse --limit 20 -o json ".format(configs["bin"], configs["node"])
        for id in f.get_vote_id(json.loads(f.terminal(to_terminal))):
            if not f.check_voted(network, id):
                to_terminal = "{} tx gov vote {} yes {} {} {} {} {} -o json -y".format(configs["bin"], id, configs["fees"], configs["node"], 
                                                                        configs["chain_id"], configs["keyring"], configs["from"])
                log.info(f"Command {to_terminal}")
                f.form_request(f.terminal(to_terminal), network, id, config[network]['explorer'])


            else:
                log.info(f"I voted for this proposol {id}")
        f.send_to_server()
            
if __name__ == "__main__":
    main()