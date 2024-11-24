from collections import Counter

def CharCode(chars):
    if(len(chars)==2):
        chars[0][2]='1'
        chars[1][2]='0'
        return chars
    else:
        sortedCharsByPriority = sorted(chars, key=lambda x: x[1], reverse=True)
        new_node = [
            sortedCharsByPriority[-2][0] + sortedCharsByPriority[-1][0],  
            sortedCharsByPriority[-2][1] + sortedCharsByPriority[-1][1],  
            "" 
        ]
        newChars = sortedCharsByPriority[:-2] + [new_node]
        newChars = CharCode(newChars)
        newChars[-1][0] = sortedCharsByPriority[-2][0]
        newChars[-1][1] = sortedCharsByPriority[-2][1]
        newChars.append([sortedCharsByPriority[-1][0],sortedCharsByPriority[-1][1],newChars[-1][2]+"1"])
        newChars[-2][2] = newChars[-2][2]+'0'
        for char in chars:
            for new_char in newChars:
                if char[0] == new_char[0] and char[1] == new_char[1]:
                    char[2] = new_char[2]
        
        return chars



def StandardHuffmanEncode(string):

    chars=[]
    charsPriority=[]

    # Calculate frequency of each character
    char_priority = Counter(string)

    for char, priority in char_priority.items():
        chars.append([char,priority/len(string),''])
        charsPriority.append([char,priority/len(string)])

    chars = CharCode(chars)
    code=""
    result = {char[0]: char[2] for char in chars}
    for char in string:
        code += result[char]
    return code ,charsPriority



def StandardHuffmanDecode(code,charsPriority):

    for char in charsPriority:
        char.append('')

    chars = CharCode(charsPriority)

    string=""
    result = {char[2]: char[0] for char in chars}
    i = 0
    while i < len(code):
        c = ""
        j = i
        while j < len(code):
            c += code[j] 
            if c in result:
                string += result[c]
                break
            j += 1  
        i = j + 1
    return string 




def SaveBinaryFile(code, charsPriority):

    with open("compressed_output.bin", 'wb') as file:

        for charPriority in charsPriority:
            char, priority = charPriority

            file.write(f"{char}:{priority}\n".encode())
        file.write(b"---\n")


        padding = (8 - len(code) % 8) % 8
        file.write(f"PAD:{padding}\n".encode())

        for i in range(0, len(code), 8):

            byte_value = int(code[i:i+8].ljust(8, '0'), 2).to_bytes(1, byteorder='big')
            file.write(byte_value)


def readBinaryFile():
    charsPriority = []
    code = ""
    with open("compressed_output.bin", 'rb') as file:
        while True:
            line = file.readline()
            if line.strip() == b"---":  
                break
            charPriority = line.decode().strip()
            char, priority = charPriority.split(':')
            charsPriority.append([char, float(priority)])  
        line = file.readline()
        if line.startswith(b"PAD:"):
            padding = int(line.decode().strip().split(":")[1])
        binary_data = file.read()
        for byte in binary_data:
            code += f"{byte:08b}" 

    if padding:
        code = code[:-padding]
    return code, charsPriority


with open('input.txt', 'r') as file:
    string = file.readline()

code,charsPriority =StandardHuffmanEncode(string)
SaveBinaryFile(code,charsPriority)


code,charsPriority=readBinaryFile()
string = StandardHuffmanDecode(code,charsPriority)

with open('decode.txt', 'w') as file:
    file.write(f"{string}")    
