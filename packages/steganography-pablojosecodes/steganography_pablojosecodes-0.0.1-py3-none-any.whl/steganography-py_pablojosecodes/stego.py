import cv2
import numpy as np


class stego():
    def __init__(self, original):
        # image and iterating values
        self.image = original
        self.height, self.width, self.channels = original.shape
        self.w = 0
        self.h = 0
        self.chan = 0 
        self.or_mask = 1
        self.and_mask = 254
        
    # Update the masking values
    def updateMasks(self):
        self.and_mask -= self.or_mask
        self.or_mask = self.or_mask * 2
    
    # Get the binary version of 'val' with proper length
    def real_binary(self, val, ln):
        realbin = bin(val)[2:]
        while ln > len(realbin):
            realbin = '0' + realbin
        return realbin    
    
    # Hide text in class's image
    def text_hide(self, text):
        length_in_binary = self.real_binary(len(text), 16)
        self.hide_val(length_in_binary)
        for c in text:
            self.hide_val(self.real_binary(ord(c), 8))
        return self.image
    
    # Use mask to update passed in pixel value
    def mask_update(self,pxl, c):
        if int(c) == 0:
            return self.zero_out(pxl)
        else:
            return self.one_in(pxl)
    
    def zero_out(self, pxl):
        return int(pxl) & self.and_mask
    
    def one_in(self, pxl):
        return int(pxl) | self.or_mask

    # Hide pased in bits to current register in image
    def hide_val(self, bits):
        for c in bits:
            self.image[self.h,self.w][self.chan] = self.mask_update(self.image[self.h,self.w][self.chan], c)
            self.iterate()
    
    # Determine whether or not to update current value type (channel, width, height)
    def pu(self, val, maxVal): # possibly update (although really, we update no matter what)
        if (val != maxVal):
            return (val+1,True)
        return (0,False)
    
    # Move to next register
    def iterate(self):
        (self.chan, end) = self.pu(self.chan, self.channels-1)
        if (end):
            return
        
        (self.w, end) = self.pu(self.w, self.width-1)
        if (end):
            return

        (self.h, end) = self.pu(self.h, self.height-1)
        if (end):
            return
        
        # End of registers
        if self.or_mask == 128:
            raise Length("Input too large")
            
        self.updateMasks()
        
        
    # Reveal hidden text
    def text_seek(self):
        revealed = ""
        for i in range(int(self.next_bits(16),2)):
            revealed += chr(int(self.next_char() ,2))
        return revealed

    # Return only the next bit of current register
    def next_bit(self):
        val = self.or_mask & self.image[self.h,self.w][self.chan]
        self.iterate()
        if val == 0:
            return val
        else:
            return "1"
    
    # Get next bits and current current character 
    def next_char(self):
        return self.next_bits(8)
    
    # Return next number of bits, in string format
    def next_bits(self, ln):
        bits = ""
        for i in range(ln):
            bits += str(self.next_bit())
        return bits
    
    
    # Encode the image if fits- first specify dimensions, then add pixels
    def encode_image(self, image):
        width, height, channels = image.shape

        bw = self.real_binary(width,16)
        bh = self.real_binary(height,16)
        
        if width*height*channels > self.width*self.height*self.channels:
            print("NO")
            raise ImageSize("Image not large enough")        
        
        self.hide_val(bw)
        self.hide_val(bh)
        
        for w in range(width):
            for h in range(height):
                for chan in range(channels):
                    val = image[w,h][chan]
                    self.hide_val(self.real_binary(int(val), 8))
                    
        return self.image

    # Decode the image
    def decode_image(self, path):
        width = int(self.next_bits(16),2)
        height = int(self.next_bits(16),2)
        channels = self.channels
        
        recovered = np.zeros((width, height, channels), np.uint8)
        
        for w in range(width):
            for h in range(height):
                for chan in range(channels):
                    recovered[w,h][chan] = int(self.next_char(),2)
        return recovered

    
    class Length(Exception):
        pass
    
    class ImageSize(Exception):
        pass

    