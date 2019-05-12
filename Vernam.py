import sounddevice as sd
import base64

inputfilename="algebra.pdf"
decodedfilename="d"

def safe(data,name):
    file = open(name, "wb+")
    file.write(base64.decodebytes(data))
    file.close()

def stringXOR(str1,str2):
    strXOR = ""

    for i in range(0,min(len(str1), len(str2))):
        strXOR += str(int(str1[i]) ^ int(str2[i]))
    return strXOR

def getMessage():
    with open(inputfilename, "rb") as pdf_file:
        message = base64.b64encode(pdf_file.read())
    binnary = "".join(["{:08b}".format(x) for x in message])
    return binnary


def getKey(recSize):
    recSize /= 3
    mask = 0b111
    threeBits = []

    samples = sd.rec(int(recSize), channels=1, dtype='int16')
    sd.wait()

    for i in range(int(recSize)):
        threeBits.append('00')
        threeBits[i] += (bin(samples[i][0] & mask)[2:5])
        threeBits[i] = threeBits[i][-3:]

    allBits = ''
    for i in threeBits:
        allBits += i
    return (allBits)


message = getMessage()
key = getKey(len(message))

coded = stringXOR(message, key)

with open("encrypted_file", "w") as coded_file:
    coded_file.write(coded)
    
coded=""

with open("encrypted_file", "r") as coded_file:
    coded=coded_file.read()
        
decoded = stringXOR(coded, key)

decoded_bytes = int(decoded, 2).to_bytes((len(decoded) // 8), byteorder='big')
safe(decoded_bytes,"decoded_algebra.pdf")
