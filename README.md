# Pollinator Camera Pre Deploy Checklist (WIP)


1. **Is all the hardware present?**
    - [ ] Raspberry Pi with WittyPi attached (small black circuit board on top of larger green circuit board)
    - [ ] MicroSD card inserted into Raspberry pi
    - [ ] Ribbon cable securely connected to Raspberry Pi
    - [ ] HQ camera present, with ribbon cable securely connected
    - [ ] Large Battery Pack (Voltaic V75) 
        - [ ] Small USB-A to C cable attached from one of the top USB ports to the USB C port **on the WittyPi**
        - [ ] Longer USB cable is connected to USB C port **on the side of the battery pack** **VERY IMPORTANT!!**
    - [ ] 18650 (cylindrical) battery secured and connected to little white JST port on the WittyPi
    - [ ] USB Flash Drive plugged into Raspberry Pi
    - **If it's a night camera:**
        - [ ] USB 5V to 12V cable present and connected to USB A port on Raspberry Pi
        - [ ] 12V IR Light (external)

2. **Connecting to the Camera**
    **Turn On The Camera**
    - If the Battery Pack isn't dead or low the camera can just be turned on. Otherwise plug the long cable into a wall charger capable of supplying at least 2A of power (not a computer's usb port)
    - Turn on the Camera via the little button on end of the WittyPi (furthest side from the USB ports)
        - **Sometimes the camera doesn't register the first click. You'll know the camera is on if you see two *solid* red lights, one on the black circuit board and one on the green one. If They're blinking it's not on. There will also be a green light the will be blinking at random intervals**
        - If connecting via HDMI to monitor, sometimes the screen may not work if the raspberry pi is already on when the cable is connected
    **Accessing the Desktop/Terminal**
    - The most straight forward way to access the camera is to connect via HDMI to an external monitor and connect a mouse and keyboard to the USB-A ports on the back of the Raspberry Pi, this will give you access to the desktop
    - If you don't have access to a monitor or HDMI, you can use SSH to connect remotely via a computer or even phone, which will give you access to the terminal
3. **First Time Setup**
    - Feel free to skip this if this camera has already run before
    - Currently, the camera's need to have a few setting adjusted before it will work properly
        1. Change the hostname
            - Type sudo raspi-config in to terminal
            - select system information
            - select hostname
            - enter new hostname that has either the word night somewhere in it for a night camera, same for day camera
            - exit raspi-config and reboot
        2. Tweak Witty software
            - type witty into terminal
            - type 8, for toggle Auto on when 5v connected
                - set to no
            - type 11


4. **Checking Functionality**
    - [ ] Is the Camera Capturing Video?
        - This requires one of the TP-LInk routers as it requires the camera to be connected to a network.
          It is the same process used to view the camera feed in the field so I wont type it out here
        - Once you have a video feed going, wave your hand infront of the camera. You'll know it's recording if the botton left of the video feed says something like "hold" with a countdown.
    
    - [ ] Does The Camera correctly recognize the usb flash drive?
        - If you're connected to the desktop, click on the icon labeled 64 GB volume, if it's populated with folders such as: archive, loop, stills, videos, the you're good. The recorded videos will be in the folder called videos. There will be at least a few of you setting up the camera already in there :P.
        - If those folders aren't present, restarting the camera should fix it.
        - If that doesn't work, try another usb drive.

    - [ ] Is the Time set correctly?
    - [ ] Is wake up / shutdown cycle setup?
     
        - Open a terminal window (ctrl+alt+t) or Start -> Accessories -> Terminal
        - Run the Pre_Deploy.py Script by typing **PreDeploy** into the terminal and press enter
            - if the hostname does not match the type of camera this is, change it before running PreDeploy (see # 3)
        - This Script allows you to view the time of the raspberry pi and the real time clock, and update them if necessary. It will also allow you to change, relative to sunrise and sunset, the time in which to wakeup / shutdown the camera
    - [ ] Is the silver battery on?
        - This Camera will turn on even if the silver battery is turned off. And so it is important to check that it is actually on before leaving it out in the field.
        - Perhaps the easiest way to check if the silver battery is on is to just plug a phone into it (assuming it's usb-c) if your phone starts to charge, it's on.
        - Another way is to see if the blue light on the wittypi 4 is on, which means the blue rtc battery is charging. However, this does turn off when that battery is fully charged.
        - **IF I'ts off** the there is a silver button on the long side, opposite the charging port.
5. **Finishing**
    - It is now safe to turn off the camera via the same button used to turn it on. Wait until the red light are no longer solidly lit before unplugging any batteries.


