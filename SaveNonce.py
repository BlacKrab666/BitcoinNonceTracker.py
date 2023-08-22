import pprint
import requests
import time
import threading

# BlacKrab666
# Sharing my practice code as I learn python on my own and try to come up with ideas to help solidify my understanding of the synthax
# I hope someone will find this helpful on their journey of python practice as well

done = False

def GetBitcoinNonce(done):
    while not done:
        cause_of_error = 'Initial Connection'
        bit_hash = hex(0x0)
        api_hash_data = "https://api.blockcypher.com/v1/btc/main" # get height and hash
        nonce_api_link = ""
        hashData = dict()
        count_zeros = 0
        file_buffer = list()

        try:
            hash_file = open('hashfile.txt', 'r')
            for line in hash_file:
                file_buffer.append(line)
                #print(line)
            hash_file.close()

            print(f"Last nonce in file is: {file_buffer[-1]}")
            time.sleep(1)

        except Exception as e:
            print(f"Error: {e}")
            print("Creating new file hashfile.txt please wait..")
            hash_file = open('hashfile.txt', 'w+')
            time.sleep(2)
            for line in hash_file:
                file_buffer.append(line)
            hash_file.close()
            if len(file_buffer) <= 0:
                file_buffer.append("0")
            #break


        try:
            time.sleep(1)
            response = requests.get(url=api_hash_data)
            hashData = dict(response.json())
            pprint.pprint(hashData)
            time.sleep(2)
            print('\n')
            if 'latest_url' in hashData:
                nonce_api_link = hashData['latest_url']
                cause_of_error = 'latest_url'
                response = requests.get(url=nonce_api_link)
                hashData = dict(response.json())
                bit_hash = hashData['hash']
                time.sleep(1)
                print(bit_hash)
                for i in list(bit_hash):
                    if i == '0':
                        count_zeros += 1
                    else:
                        break
                time.sleep(1)
                print(f"Nonce Zeros Count: {count_zeros}\n") # hash leading zeros may be give or take 1 digit
            else:
                cause_of_error = "Initial Connection"
                print("Key not found!")
        except ConnectionError as e:
            print(f"Connection failed: {e} due to {cause_of_error}.")
        time.sleep(1)
        print(f"The current nonce is: {hashData['nonce']}\n")

        if file_buffer[-1] != str(hashData['nonce']):
            hash_file = open("hashfile.txt", 'a+')
            hash_file.write('\n')
            hash_file.writelines(str(hashData['nonce']))      # Save nonce to file
            hash_file.close()
        else:
            time.sleep(1)
            print("Same nonce means no new winner.\n")
            continue
        time.sleep(1)
        file_buffer.clear()


th = threading.Thread(target=GetBitcoinNonce, daemon=True, args=(done,))
th.start()
done = bool(input("Press 'Enter' to terminate process."))
print(done)
print("/nBitcoin Nonce Tracker Terminated..")
