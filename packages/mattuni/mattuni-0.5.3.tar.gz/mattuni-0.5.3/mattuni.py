import requests
import json

from dataclasses import dataclass

import mstuff


mstuff.warn_if_old("mattuni")


_ran_x_times = []


_url_prefix = 'https://teach-anya.herokuapp.com'


print("test update")

@dataclass
class Challenge:
    number: int

    def __post_init__(self):
        self.req = str.encode(json.dumps({
            "q": self.number,
        }))

    def prompt(self):
        response = requests.get(f'{_url_prefix}/prompt', data=self.req)
        print(response.text)


    def input(self):
        print(f"Getting json input for question {self.number} ...")
        response = requests.get(f'{_url_prefix}/get-big-input', data=self.req)
        r = response.text
        print(f"Got json input (number of characters={len(response.text)}) Don't forget to decode it!")
        return r


    def send_answer(self,answer):
        print()
        print()
        global _ran_x_times
        if self.number in _ran_x_times:
            print(f"Challenge {self.number} Failed. You can only call send_answer one time per challenge.")
        else:
            _ran_x_times.append(self.number)
            if (len(answer) < 200):
                print(f"Sending answer for question {self.number}: \"" + answer + "\" ...")
            else:
                print(f"Sending the (very long) answer for question {self.number}...")
            j = json.dumps({
                "q": self.number,
                "answer": answer
            })
            response = requests.get(f'{_url_prefix}/send', data=str.encode(j))
            print(response.text)
            print()
            print()


