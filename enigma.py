# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 18:48:34 2021

@author: z_p12
"""
class PlugLead:
    """Create a Lead object."""
    def __init__(self, mapping):
        self.mapping = mapping.upper()
        if self.mapping[0] == self.mapping[1] or len(self.mapping)!=2:
            raise ValueError("Please ensure you are only connecting a lead to only 2 slots and that the slots aren't the same!")


    def encode(self, character):
        if character == self.mapping[0]:
            return self.mapping[1]
        elif character == self.mapping[1]:
            return self.mapping[0]
        else:
            return character
        
        
    def __repr__(self):
        return repr(self.mapping)


class Plugboard:
    "Creates a plugboard instance with 10 slots."
    def __init__(self, max_leads = 10):
        self.max_leads = max_leads
        self.connected_leads = []
        if self.max_leads >13:
            raise ValueError("A Plugboard cannot have more than 13 leads connected!")
        
    
    def is_full(self):
        return len(self.connected_leads) >= self.max_leads
    
    
    def is_empty(self):
        return len(self.connected_leads) == 0
    
    
    def add(self,lead):
        """Add a Pluglead to the Plugboard"""
        if self.is_full():
            raise ValueError("All plugboard slots used, cannot add anymore leads!")
        
        if self.is_existing_lead(lead):
            raise ValueError("One of the slots already has a lead connected!")
        
        else:
            self.connected_leads.append(lead)
    
    
    def remove(self,lead):
        """Remove a specific Pluglead from the Plugboard"""
        if self.is_empty():
            return "No leads are connected, cannot remove a lead that doesn't exist!"
        
        if not self.is_existing_lead(lead):
            return "This lead doesn't exist on the plugbaord!"
        
        else:
            for item in self.connected_leads:
                if lead.mapping[0].upper() and lead.mapping[1].upper() in item.mapping:
                    self.connected_leads.remove(item)
                    
            
    def is_existing_lead(self,lead):
        """Check if a slot is already connected"""
        return any(lead.mapping[0].upper() in item.mapping for item in self.connected_leads) or any(lead.mapping[1].upper() in item.mapping for item in self.connected_leads)
    
    
    def encode(self,character):
        """Encode or Decode a character"""
        if any(character.upper() in item.mapping for item in self.connected_leads):
            for item in self.connected_leads:
                if character.upper() in item.mapping:
                    return item.encode(character.upper())
                    break
        else:
            return character.upper()
        
    def __repr__(self):
        return repr(self.connected_leads)


class Rotors:
    """Create a rotor object."""
    
    rotors_available = {"I" :{"Wiring":"EKMFLGDQVZNTOWYHXUSPAIBRCJ","Notch":"Q"},
              "II" : {"Wiring":"AJDKSIRUXBLHWTMCQGZNPYFVOE","Notch":"E"},
              "III" : {"Wiring":"BDFHJLCPRTXVZNYEIWGAKMUSQO", "Notch":"V"},
              "IV" : {"Wiring":"ESOVPZJAYQUIRHXLNFTGKDCMWB", "Notch":"J"},
              "V" :  {"Wiring":"VZBRGITYUPSDNHLXAWMJQOFECK", "Notch":"Z"},
              "Beta" : {"Wiring":"LEYJVCNIXWPBQMDRTAKZGFUHOS","Notch":None},
              "Gamma" : {"Wiring":"FSOKANUERHMBTIYCWLQPZXVGJD","Notch":None}}
    
    input_output = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self,rotor_name):
        try:
            self.name = rotor_name
            self.wiring = self.rotors_available[rotor_name]["Wiring"]
            self.pins = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            self.contacts = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            self.notch = self.rotors_available[rotor_name]["Notch"]
            self.ring_position = 0
        except KeyError:
            raise ValueError(f"Rotor '{rotor_name}' does not exist!")
            
            
    def set_offset(self,letter):
        offset = self.input_output.index(letter)
        self.pins = self.pins[offset:] + self.pins[:offset]
        self.contacts = self.contacts[offset:] + self.contacts[:offset]
    

    def set_ring(self,number):
        number -=1
        self.ring_position = number
            

    
    def encode_right_to_left(self,character):
        index_of_input = self.input_output.index(character)
        pins_offset = self.pins[-self.ring_position:]+self.pins[:-self.ring_position]
        contacts_offset = self.contacts[-self.ring_position:]+self.contacts[:-self.ring_position]
        corresponding_pin = (pins_offset)[index_of_input]
        wire_mapping = self.wiring[self.input_output.index(corresponding_pin)]
        wire_mapping_index = (contacts_offset).index(wire_mapping)
        #print(f"Input {character} lines with pin {corresponding_pin} which wires to contact {wire_mapping}. This lines with pin {self.input_output[wire_mapping_index]} of the next rotor.")
        return self.input_output[wire_mapping_index]
    
    
    def encode_left_to_right(self,character):
        pins_offset = self.pins[-self.ring_position:]+self.pins[:-self.ring_position]
        contacts_offset = self.contacts[-self.ring_position:]+self.contacts[:-self.ring_position]
        index_of_input = self.input_output.index(character)
        corresponding_contact = (contacts_offset)[index_of_input]
        wire_mapping = self.input_output[self.wiring.index(corresponding_contact)]
        wire_mapping_index = (pins_offset).index(wire_mapping)
        #print(f"Input {character} lines with contact {corresponding_contact} which wires to pin {wire_mapping}. This lines with contact {self.input_output[wire_mapping_index]} of the next rotor.")
        return self.input_output[wire_mapping_index]
    
    
    def rotate(self):
        offset = 1%len(self.pins)
        self.pins = self.pins[offset:] + self.pins[:offset]
        self.contacts = self.contacts[offset:] + self.contacts[:offset]
            
    def __repr__(self):
        return repr(self.name)


class Reflector:
    """Create a reflector object."""
    reflectors_available = {"B" : {"Wiring":"YRUHQSLDPXNGOKMIEBFZCWVJAT","Notch":None},
                  "A" : {"Wiring": "EJMZALYXVBWFCRQUONTSPIKHGD", "Notch":None},
                  "C" : {"Wiring": "FVPJIAOYEDRZXWGCTKUQSBNMHL", "Notch":None}}
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self,name):
        try:
            self.name = name
            self.wiring = self.reflectors_available[name]["Wiring"]
            self.pairs = [''.join(item) for item in zip(self.letters,self.wiring)]
        except KeyError:
            raise ValueError(f"Reflector '{name}' does not exist!")      

    def reflect(self,character):
        for pair in self.pairs:
            if character == pair[0]:
                return pair[1]
            elif character == pair[1]:
                return pair[0]        
    
    def __repr__(self):
        return repr(self.name)
    
    
class Enigma:
    """Creates an Enigma machine object without the components installed."""
    
    def __init__(self):
        self.rotors = []
        self.plugboard = Plugboard()
        self.reflector = None
        self.ring_positions = []
    
    
    def reset(self):
        """Removes all the Enigma machine components & settings for the specified instance."""
        self.rotors = []
        self.plugboard = Plugboard()
        self.reflector = None
        
    
    def show_settings(self):
        """Show Enigma settings for the specified instance."""
        positions=''
        ring_settings = ()
        for rotor in self.rotors[::-1]:
            positions+=rotor.pins[0]
            ring_settings+=(rotor.ring_position+1,)
        print(f"Rotors: {tuple(self.rotors[::-1])}\nRotor Positions: {positions}\nRing Settings: {ring_settings}\nReflector: {self.reflector}\nPlugleads: {self.plugboard}")
        
    
    def add_settings(self,plugboard_setting,rotor_positions,ring_positions):
        """ Specify the plugboard leads, rotor positions and ring settings
     
        :param list plugboard_setting: The plug leads to add to the plugboard.  
        :param str rotor_positions: The position of each rotor e.g AAA 
        :param tuple ring_positions: The ring setting for each rotor e.g (1,1,1)  
        :raises ValueError: if no rotors have been added or you specify more ring settings than there are rotors  
             
        """
        if len(self.rotors)==0:
            raise ValueError("No rotors have been added! Cannot set intitial positions!")
        for index, setting in enumerate(rotor_positions[::-1]):
            self.rotors[index].set_offset(setting)

        
        for item in plugboard_setting:
            self.plugboard.add(PlugLead(item))
        
        if len(ring_positions)>len(self.rotors):
            raise ValueError("You've specified more ring settings than there are rotors in the machine!")
            
        for index, number in enumerate(reversed(ring_positions)):
            self.rotors[index].set_ring(number)
    
    
    def add_components(self,reflector,*rotors):
        """ Add reflector and rotors to Enigma machine.
    
        :param str reflector: The reflector to install e.g 'A'  
        :param str *rotors: The rotors to install from leftmost to rightmost e.g 'I','II','III'  
             
        """
        for arg in rotors:
            self.rotors.insert(0,Rotors(arg))
            
        self.reflector = Reflector(reflector) 
            
        
    def check_components(self):
        """Returns a boolean value to indicate whether you have any missing components in your Enigma machine which may stop it from functioning."""
        return len(self.rotors)==0 or self.reflector==None 
    
    
    def rotate_rotors(self):
        """Checks the notch of each rotor and rotates as neccessary"""
        rotors_left_to_right = self.rotors[2::-1]
        
        if len(self.rotors)==1:
            pass
        
        # If there are only 2 rotors, only check if the previous rotor is on its notch.
        elif len(self.rotors)==2:
            if rotors_left_to_right[1].pins[0] == rotors_left_to_right[1].notch:
                rotors_left_to_right[0].rotate()
                rotors_left_to_right[1].rotate()
                
        else:
            for index,rotor in enumerate(rotors_left_to_right):
                if index==len(rotors_left_to_right)-2:
                    break
                # if the previous rotor is on its notch, rotate the current and previous. 
                elif rotors_left_to_right[index+1].pins[0] == rotors_left_to_right[index+1].notch:
                    rotors_left_to_right[index].rotate()
                    rotors_left_to_right[index+1].rotate()
                # if the rotor before the previous is on its notch, rotate the previous.
                elif rotors_left_to_right[index+2].pins[0] == rotors_left_to_right[index+2].notch:
                    rotors_left_to_right[index+1].rotate()
                    
        # always rotate the first rotor.
        self.rotors[0].rotate()
    
           
    def encode_letter(self,character):
        """Encodes a letter"""
        # Check components are installed
        if self.check_components():
            raise ValueError("One ore more components missing! Please ensure you have installed the rotors as well as one reflector.")
        
        if len(str(character))>1:
            raise ValueError("Please specify only one letter to encode!")
            
        self.rotate_rotors()
        
        # Send input through plugboard
        plug_scramble = self.plugboard.encode(character)
        
        # Send plugboard output to rotors
        steps = []
        first = self.rotors[0].encode_right_to_left(plug_scramble)
        steps.append(first)
        for index, rotor in enumerate(self.rotors[1:]):
            result = rotor.encode_right_to_left(steps[index])
            steps.append(result)
            
        steps.append(self.reflector.reflect(steps[-1]))
        
        for index, rotor in enumerate(self.rotors[::-1]):
            result = rotor.encode_left_to_right(steps[len(steps)-1])
            steps.append(result)
            
        # Send ouptut back to plugboard
        output = self.plugboard.encode(steps[-1])
        #print(f"{results[-1]} goes back into the plugboard which encodes into {last}")
        return output
    
    
    def encrypt_decrypt_message(self,message):
        """Accepts a string to encrypt or decrypt."""
        output_message=''
        for character in message:
            output_message+=self.encode_letter(character)
        return output_message
            

if __name__ == "__main__":
    my_enigma = Enigma()
    my_reflector = input("Specify a reflector: ").title()
    my_rotors = tuple(input("Specify the rotors e.g III,II,I : ").split(','))
    my_enigma.add_components(my_reflector, *my_rotors)
    settings = input("Do you want to adjust the enigma settings?: ")
    if settings.title()=="Y":
      my_plugboard = [item for item in input("Specify plugboard settings e.g HL,MO,QV: ").split(',')]
      my_rotor_positions = input("Specify rotor positions e.g ABCD: ")
      my_ring_settings = tuple(map(int,input("Specify ring settings for each rotor e.g 1,1,3,4: ").split(',')))
      my_enigma.add_settings(my_plugboard,my_rotor_positions,my_ring_settings)
    message = input("Enter message to encrypt: ")
    print(my_enigma.encrypt_decrypt_message(message))
    
    
    
    
    
    


    

