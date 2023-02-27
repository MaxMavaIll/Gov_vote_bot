import json, time
import funtion as f
import logging as log
# from apscheduler.schedulers.background import BackgroundScheduler

get_data_txhash = {}

def main():
    log.basicConfig(
        level=log.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config, vote_last_moment = f.check_config()

    for network, configs in config.items():
        log.info("Name wallet: {}, Network: {}\n".format(configs["from"].replace("--from ", ""), network))

        id_vote_proposols = f.get_vote_id_and_last_time("{} q gov proposals {} --reverse --limit 20 -o json ".format(configs["bin"], configs["node"]), configs, vote_last_moment, network)

        for id in id_vote_proposols:
            log.info(f"Proposol_id: {id}")

            if network not in get_data_txhash:
                get_data_txhash[network] = {}

            position = f.get_variant_with_more_votes("{} q gov votes {} {} {} -o json".format(configs["bin"], id, configs["chain_id"], configs["node"]))

            get_data_txhash[network][id] = f.vote_for_proposal("{} tx gov vote {} {} {} {} {} {} {} -o json -y".format(configs["bin"], id,
                                                                                        position, configs["fees"], 
                                                                                        configs["node"], configs["chain_id"],
                                                                                        configs["keyring"], configs["from"]),
                                                                                        configs, network, id )
  #          time.sleep(10)

    f.send_to_server(get_data_txhash)

            
if __name__ == "__main__":
    main()