from dataclasses import dataclass
from typing import Dict


@dataclass
class Cup:
    number: int
    next: 'Cup' = None


inp = [8, 7, 1, 3, 6, 9, 4, 5, 2]
for n in range(10, 1000001):
    inp.append(n)

cups: Dict[int, Cup] = {number: Cup(number) for number in inp}
for i in range(len(inp)):
    previous_cup_num = inp[(i - 1 + len(inp)) % len(inp)]
    next_cup_num = inp[(i + 1) % len(inp)]
    cups[inp[i]].next = cups[next_cup_num]

cut_out_length = 3
rounds = 10000000
current_cup: Cup = cups[inp[0]]
for _ in range(rounds):

    cut_out_numbers = set()

    n = current_cup.next
    first_in_cutout = n
    last_in_cutout = n
    for _ in range(cut_out_length):
        cut_out_numbers.add(n.number)
        last_in_cutout = n
        n = n.next

    after_cutout = n

    desired_destination_number = current_cup.number - 1
    while desired_destination_number in cut_out_numbers or desired_destination_number not in cups:
        if desired_destination_number not in cups:
            desired_destination_number = max(cups.keys())
        else:
            desired_destination_number -= 1

    destination_cup = cups[desired_destination_number]
    current_cup.next = after_cutout
    last_in_cutout.next = destination_cup.next
    destination_cup.next = first_in_cutout

    current_cup = after_cutout

c = cups[1].next.number * cups[1].next.next.number
print(c)
