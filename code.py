import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
#from git import Repo
from picamera2 import Picamera2

# VARIABLES
THRESHOLD = 0      # Any desired value from the accelerometer
REPO_PATH = "https://github.com/TheJavaScriptWizard/SmallSat.git"     # Your GitHub repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "/Images"   # Your image folder path in your GitHub repo: ex. /Images

# IMU and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()
picam2.start()

def git_push():
    """
    Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        origin.pull()
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        origin.push()
    except Exception as e:
        print('Couldn\'t upload to git:', e)

def img_gen(name):
    """
    Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    #imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    imgname = (f'./pics/{name}{t}.jpg')
    return imgname

def take_photo():
    """
    Takes a photo when the FlatSat is shaken.
    """
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        print(accelx, accely, accelz)
        # Check if any of the acceleration readings are above the threshold
        if accelx > THRESHOLD or accely > THRESHOLD or accelz > THRESHOLD:
            print('take pic')
            # Pause for a moment
            time.sleep(1)
            # Generate a filename based on current time and author's name
            name = "sat"  # Fill in your first name and last initial
            img_path = img_gen(name)
            print(img_path)
            # Take a photo
            picam2.capture_file(img_path)
            print("pic taken")
            # Push the photo to GitHub
            git_push()
            # Pause again to prevent multiple photos being taken in quick succession
            time.sleep(1)

def main():
    print("main")
    take_photo()

if __name__ == '__main__':
    main()
