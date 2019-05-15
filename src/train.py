
import sys
import json
import datetime

from ns_log import NsLog
from json2arff import json2arff
from traceback import format_exc
from domain_parser import domain_parser
from rule_extraction import rule_extraction

from tqdm import tqdm


class Train:
    def __init__(self):
        self.logger = NsLog("log")

        self.json2arff_object = json2arff()
        self.parser_object = domain_parser()
        self.rule_calculation = rule_extraction()

        self.path_input = "../input/"
        self.path_arff = "../output/arff/"
        self.path_features = "../output/features/"
        self.path_parsed_domain = "../output/domain_parser/"

    def txt_to_list(self, txt_object):

        lst = []

        for line in txt_object:
            lst.append(line.strip())

        txt_object.close()

        return lst

    def domain_parser(self, param):

        parsed_domains = []

        for i in range(1, len(param), 2):
            try:
                if param[i + 1] == 'phish' or param[i + 1] == 'legitimate':

                    #dataset = self.txt_to_list(open("{0}{1}".format(self.path_input, param[i]), "r"))  # txt read
                    dataset = json.loads(open("{0}{1}".format(self.path_input, param[i]), "r").read())  # json read

                    parsed_domains = parsed_domains + self.parser_object.parse(dataset, param[i + 1],
                                                                               len(parsed_domains))

                else:
                    self.logger.debug("class labels must be entered one of (phish, legitimate)")

            except:
                self.logger.error("an error is occurred  : {0}".format(format_exc()))
                self.logger.debug("an error occurred when | {0}.txt | file was processing".format(param))

        self.logger.info("Domain Parse process is done {0} unique URLs are parsed".format(len(parsed_domains)))

        return parsed_domains

    def json_to_file(self, name, path, data):
        time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = name+"_" + time_now + ".txt"
        file = open(path + file_name, "w")
        file.write(json.dumps(data))
        file.close()
        self.logger.info("{0} Written to File.".format(name))

    def arff_to_file(self, name, path, data):
        time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = name + "_" + time_now + ".txt"
        file = open(path + file_name, "w")
        file.write(data)
        file.close()
        self.logger.info("{0} Written to File.".format(name))
        
    def conv_2_feat(self, urls):
        parsed_domains = self.parser_object.parse(urls, 'unknown', len(urls))
        features = self.rule_calculation.extraction(parsed_domains)
        return features


def main():

    """
    loop according to dataset and class parameter entered from console
    If the dataset is entered as a paramter, the domains are parsed
    they are all collected in a single variable (parsed_domain).
    The entered parameters are checked.

    python main.py must be entered in dataset1 class1 dataset2 class2 ...
    e.g.
    python train.py ../input/data_legitimate_36400.json legitimate ../input/data_phishing_37175.json phish

    The entered class names must be phish or legitimate. Otherwise it is not.

    The fields that are parsed are given to the rule_calculation object.
    output of domains

    to test the calculated property values ​​with weka
    arff format
    """

    tr_obj = Train()
    parsed_domains = tr_obj.domain_parser(sys.argv)
    # tr_obj.json_to_file("parse", tr_obj.path_parsed_domain, parsed_domains)

    features = tr_obj.rule_calculation.extraction(parsed_domains)
    # tr_obj.json_to_file("features", tr_obj.path_features, features)
    
    tr_obj.logger.info('Convert features to DataFrame')
    import pandas as pd
    info_df = []
    feat_df = []
    for feature in tqdm(features):
        info_df.append(feature['info'])
        feat_df.append(feature['url_features'])
    info_df = pd.DataFrame(info_df)
    feat_df = pd.DataFrame(feat_df)
    data_df = pd.concat([info_df, feat_df], axis=1)
    data_df.to_csv('../output/digest_result/data.csv', index=False, encoding='utf8')
    tr_obj.logger.info('Convert done')

    #features = json.loads(open("../output/features/gsb.txt", "r").read())

    # arff_str = tr_obj.json2arff_object.convert_for_train(features, '') # todo active_features icin -a param girilecek
    # tr_obj.arff_to_file("arff", tr_obj.path_arff, arff_str)


if __name__=="__main__":
    main()
