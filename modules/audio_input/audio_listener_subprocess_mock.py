from time import sleep

# pitch of current frame
freq = 5000.00
ticks = 1000

# main loop
while True:
    ticks = (ticks - 1) % 20
    
    freq = 5000.00
    # compute energy of current block
    energy = ticks / 2
    # do something with the results
    print("{:10.4f} {:10.4f}".format(freq,energy))
    sleep(0.025)
    
