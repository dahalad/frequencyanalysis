from itertools import combinations
import string
import sys

class Key:
    def __init__(self, key):
        self.key = key
        self.index = 0
        self.length = len(key)

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def next(self):
        cindex = self.index
        self.index += 1
        return self.key[cindex % self.length]


englishLetterFreq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07,
}

LETTERS = string.ascii_lowercase


def getFactors(num):
    allfactors = [num]
    n = num
    pfactors = []
    i = 3
    while n != 1:
        if n % 2 == 0:  # factorize garda 2 le vag janchha ta? gayo vane
            # 2 ko key pailei chha ki chhaina herchha
            pfactors.append(2)  # raichha vane tesko value lai 1 le badhauchha
            n /= 2  # yesko matlab prime factorization garda 2 kati patak repeat hunchha store gareko
        elif n % i == 0:  # aba chai 2 ko satta aru prime number ko palo
            if i != num:
                pfactors.append(i)
                n /= i
                i = 3
            else:
                break
        else:
            i += 2
    for j in range(2, len(pfactors)):
        temp = combinations(pfactors, j)
        for item in temp:
            temp_pr = 1
            for num in item:
                temp_pr *= num
            if temp_pr not in allfactors:
                allfactors.append(temp_pr)
    for fac in pfactors:
        if fac not in allfactors:
            allfactors.append(fac)

    return sorted(allfactors)


def shifter(block,key):
    k = LETTERS.find(key)
    shifted = ''
    for i in block:
        c = LETTERS.find(i)
        diff = c-k
        shifted += LETTERS[(25+diff)%26]
    return shifted


def getScore(block):
    score = 0
    lettercount = getFrequencyOrder(block)
    ks = list(lettercount.keys())
    mostFrequent = ks[:6]
    leastFrequent = ks[-6:]
    for i in 'etaoin':
        if i in mostFrequent:
            score += 1
    for i in 'vkjxqz':
        if i in leastFrequent:
            score+=1
    return score


def combine(lister):
    k = []
    for item in lister[0]:
        k.append(item)
    for item in lister[1:]:
        temp = []
        for let in item:
            for key in k:
                key+=let
                temp.append(key)
        k = temp

    return k


def bruteforce(block):
    # letters = string.ascii_lowercase
    best_key, best_score = '',0
    for i in LETTERS:
        shifted = shifter(block,i)
        score = getScore(shifted)
        if score == best_score:
            best_key += i
        if score > best_score:
            best_score = score
            best_key = i
    return best_key



def partitionTheCipher(block, kl):
    partitions = {}
    for i in range(kl):
        part = ''.join(i for i in block[i::kl])
        partitions[i] = part
    return partitions


def sortDict(values, dict):
    orderedFreqCount = {}
    for val in values:
        for k, v in dict.items():
            if val == v:
                orderedFreqCount[k] = v
    return orderedFreqCount


def getProbableKeyLengths(repeatDict):
    repeatList = []
    for repeatLists in repeatDict.values():
        repeatList += repeatLists
    repeatList = sorted(set(repeatList))
    allfactors = []
    for item in repeatList:
        allfactors += getFactors(item)
    allfactors = sorted(allfactors)
    counts = {}
    for fac in allfactors:
        count = allfactors.count(fac)
        counts[fac] = count
    counts = sortDict(sorted(counts.values(), reverse=True),counts)
    # print(list(counts.keys()))
    rtnval = list(counts.keys())
    return list(filter(lambda x: x>3, rtnval))



def getRepeatedSequence(block):
    repeatedSequences = {}
    for kl in range(4, 7):
        for sequeceStart in range(len(block) - kl):
            sequence = block[sequeceStart:sequeceStart + kl]
            if sequence in repeatedSequences.keys():
                continue
            spacings = []
            allspacings = []
            i = block.index(sequence)
            spacings.append(i)
            temp = len(block) - kl
            for j in range(sequeceStart + kl, temp+1):
                text = block[j:j + kl]
                if sequence == text:
                    position = block.index(sequence, i+1)
                    spacings.append(position)
                    i = position
            for j in range(len(spacings)-1):
                for k in range(j+1, len(spacings)):
                    allspacings.append(spacings[k]-spacings[j])
            if allspacings:
                repeatedSequences[sequence] = allspacings
    return repeatedSequences


def getplainText(cipher, key):
    c = LETTERS.find(cipher) + 1
    k = LETTERS.find(key) + 1
    diff = c-k
    # print(c,k,diff)
    return LETTERS[(25 + diff) % 26]


def getLetterCount(block):
    letterCount = {}
    for letter in LETTERS:
        letterCount[letter] = block.count(letter)
    return letterCount


def getFrequencyOrder(block):
    letterFreqCount = getLetterCount(block)
    vals = sorted(set(letterFreqCount.values()), reverse=True)
    orderedFreqCount = sortDict(vals, letterFreqCount)

    return orderedFreqCount


# corpora = "bpxtbogeinlwbyhwpohlfthwuqkmnjhwnaivjgqhnakisqpchwdvekdrncbljoomwgmytvosoihrpwjluqhrkqbpjhhfvvqsunrrhgqsvikxpuxjgguetvkizfraigqxigbkfvrpeujdxujdx"
corpora = input("Your Text: ")
cipherText = corpora.lower()
cipherText = "".join(l for l in cipherText if l.isalnum())

repeatitions = getRepeatedSequence(cipherText)
if not repeatitions:
    print("Sorry!, I can't decode this!!")
    sys.exit(0)
probableKeyLengths = getProbableKeyLengths(repeatitions)

for ran in probableKeyLengths:
    partitions = partitionTheCipher(cipherText,ran)
    keysss = []
    for v in partitions.values():
        keysss.append(bruteforce(v))
    fkeys = combine(keysss)

    for ks in fkeys:
        ch = Key(ks)
        pText = ''
        for let in cipherText:
            pText += getplainText(let,next(ch))
        print(pText)
        reply = input("Is this the decrypted text? Help me out, I can't differentiate languages [Y/n]: ").lower()
        if reply == 'y':
            print("Thank you for using this module.!! The key was ", ch.key)
            sys.exit(0)
