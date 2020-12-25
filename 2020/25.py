door_pub = 15113849
card_pub = 4206373
m = 20201227


def break_pubkey(key):
    candidate = 1
    rounds = 0
    while candidate != key:
        candidate *= 7
        candidate %= m
        rounds += 1
    return rounds


door_private_key = break_pubkey(door_pub)
card_private_key = break_pubkey(card_pub)

enc_key = 1
for _ in range(card_private_key):
    enc_key *= door_pub
    enc_key %= m

print(enc_key)
