import random


def up(char: str) -> str:
    return char.upper()


def low(char: str) -> str:
    return char.lower()


def ul_random_shuffle(word: str) -> str:
    chars = list(word)
    for index, char in enumerate(chars):
        if random.randint(0, 1):
            chars[index] = up(char)
        else:
            chars[index] = low(char)
    return ''.join(chars)


def ul_interval_shuffle(word: str) -> str:
    chars = list(word)
    for index, char in enumerate(chars):
        if index & 1:
            chars[index] = up(char)
        else:
            chars[index] = low(char)
    return ''.join(chars)


if __name__ == '__main__':
    article = '''
Joy in living comes from having fine emotions, trusting them, giving them the freedom of a bird in 
the open. Joy in living can never be assumed as a pose, or put on from the outside as a mask. People who have 
this joy do not need to talk about it; they radiate it. They just live out their joy and let it splash its 
sunlight and glow into other lives as naturally as bird sings.
'''
    print(article)
    print(' '.join([ul_random_shuffle(word) for word in article.split(' ')]))
    print(' '.join([ul_interval_shuffle(word) for word in article.split(' ')]))
