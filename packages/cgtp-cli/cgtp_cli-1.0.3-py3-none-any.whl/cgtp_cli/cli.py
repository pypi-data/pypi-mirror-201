# ls.py v2
from pathlib import Path
import os
import pickle
import argparse
import sys
from . import chatGPT

__version__ = "1.0.3"


def main():

    parser = argparse.ArgumentParser(
        prog='cgtp-cli',
        description="Ask chat gtp for the command you need. You'll need an API key, get one at https://platform.openai.com/account/api-keys, use the -k flag to update the key",
    )

    # Arguments

    # Command description
    parser.add_argument("command_description",
                        help="The command description you want to search for",
                        nargs='?')

    # argument for including the comands descriptions in the output
    parser.add_argument("-d", "--description", action="store_true",
                        help="Include the command descriptions in the output",
                        default=False)

    # argument for showing many options
    parser.add_argument("-o", "--options",
                        help="Show many options for the command you search for",
                        type=int, choices=range(1, 10),
                        default=1)

    # argument for including examples
    parser.add_argument("-e", "--examples", action="store_true",
                        help="Include examples for the command you search for",
                        default=False)

    # update the chatgtp api key
    parser.add_argument("-k", "--key",
                        help="Update the chatgtp api key")

    # update the chatgtp prefix
    parser.add_argument("-P", "--Prefix",
                        help="Update the chatgtp prefix",
                        nargs='?'
                        )

    # update the chatgtp prefix for this command description
    parser.add_argument("-p", "--prefix",
                        help="Update the chatgtp prefix for this command description",
                        nargs="*")

    # show the config
    parser.add_argument("-c", "--config", action="store_true",
                        help="Show the current config",
                        default=False)

    # version
    parser.add_argument("-v", "--version", action="version",
                        version="cgtp_cli {}".format(__version__) , help="Show the version of the program")

    # read the arguments from the command line
    args = parser.parse_args()

    comand_description = args.command_description
    includeDescriptions = args.description
    permanetPrefix = args.Prefix
    temporalPrefix = args.prefix
    numberOfOptions = args.options
    includeExamples = args.examples
    key = args.key
    showConfig = args.config

    # 1. If requested update the key
    if (key):
        config = {}
        if (os.path.exists('config.pkl') and os.path.getsize('config.pkl') > 0):
            config = pickle.load(open("config.pkl", "rb"))
        config['key'] = key
        pickle.dump(config, open("config.pkl", "wb"))

    # 2. If requested update the prefix
    if (permanetPrefix):
        config = {}
        if (os.path.exists('config.pkl') and os.path.getsize('config.pkl') > 0):
            config = pickle.load(open("config.pkl", "rb"))
        config['prefix'] = permanetPrefix
        pickle.dump(config, open("config.pkl", "wb"))

    # 3. If requested show the config
    if (showConfig):
        config = {}
        if (os.path.exists('config.pkl') and os.path.getsize('config.pkl') > 0):
            config = pickle.load(open("config.pkl", "rb"))
        print(config)

    # 4. Get the command from chatgtp

        # 4.1 if no description is given and not permanet prefix or key is given then exit
    if (not comand_description and (not permanetPrefix or not key) and not showConfig):
        print("No command description given, you can update the prefix with -p or -P")
        sys.exit()

        # 4.2 if no description is given and -p or -P is given then update the prefix

    if (comand_description):

        print('Loading...', end="\r")
        result = chatGPT.getComand(
            comand_description, temporalPrefix, numberOfOptions, includeDescriptions, includeExamples)

        if (result['ok']):
            for option in result['comands']:
                print(option)
        else:
            print("Error:", result['error'])
