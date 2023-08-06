import openai
import pickle
import platform
from functools import reduce

# function for asking chatgtp about a command


def getComand(description, temporalPrefix, numberOfOptions=1, includeDesriptions=False, includeExamples=False):

    # get the user config
    config = pickle.load(open("config.pkl", "rb"))

    prefix = config['prefix']
    openai.api_key = config['key']
    userOs = platform.system()
    platform.release()

    try:

        messages = [
            {"role": "system", "content": temporalPrefix or prefix},
            {"role": "system", "content": "The following messages on this request will give you more context on the user requirements"},
            {"role": "system",
             "content": "The user is unsing {}".format(userOs)},
            {"role": "system",
             "content": "Please provide {} options for the comand searched".format(numberOfOptions)},
            {"role": "system", "content": "Include the examples for the comands" if (
                includeExamples) else "Do not include the examples for the commands"},
            {"role": "system", "content": "Include the descriptions for the comands" if (
                includeDesriptions) else "Do not include the descriptions for the commands "},
            {"role": "system", "content": "Separate comands with a new line"},
            {"role": "system", "content": "Please don't repeat commands in your answer"},
            {"role": "user", "content": description}
        ]

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return {
            'ok': True,
            'comands': list(map((lambda x: x.message.content), result.choices))
            }
    except Exception as e:
        return {
            'ok': False,
            'error': e
        }
