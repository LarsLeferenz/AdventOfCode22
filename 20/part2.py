import pathlib
from tqdm import tqdm
numbers = pathlib.Path("20/input.txt").read_text().splitlines()

numbers = list(map(int, numbers))


class EncryptedList():

    def __init__(self, numbers : list):
        
        self.numbers = numbers
        self.current_position = list(range(len(numbers)))
        self.current_index = 0
        
    def move_item(self):
        
        index = self.current_position[self.current_index]   
        amount = self.numbers[index]
        #print(f"Moving {amount}")
        new_index = (index + amount) % (len(self.numbers)-1) #-1 du to "skipping" nature

        item = self.numbers.pop(index)
        
        for pos_index in range(len(self.current_position)):
            if self.current_position[pos_index] > index:
                self.current_position[pos_index] -= 1
        
        self.numbers.insert(new_index, item)
        
        for pos_index in range(len(self.current_position)):
            if self.current_position[pos_index] >= new_index:
                self.current_position[pos_index] += 1
            
        self.current_position[self.current_index] = new_index
        self.current_index = (self.current_index + 1) % len(self.numbers)
        
    def get_number_wrapping(self, offset : int):
        
        zero_index = self.numbers.index(0)
        return self.numbers[(zero_index+offset)%len(self.numbers)]
        
        
if __name__ == "__main__":
    
    DECRYPTION_KEY = 811589153
    
    numbers = [number * DECRYPTION_KEY for number in numbers]
    
    encrypted_list = EncryptedList(numbers)
    
    print("Decrypting...")
    for _ in tqdm(range(10*len(numbers))):
        encrypted_list.move_item()
    
    print(f"1000th number is {encrypted_list.get_number_wrapping(1000)}")
    print(f"2000th number is {encrypted_list.get_number_wrapping(2000)}")
    print(f"3000th number is {encrypted_list.get_number_wrapping(3000)}")
    
    print(f"Sum = {encrypted_list.get_number_wrapping(1000) + encrypted_list.get_number_wrapping(2000) + encrypted_list.get_number_wrapping(3000)}")