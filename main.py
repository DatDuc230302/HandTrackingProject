from modules import di_chuyen_chuot
from modules import nhan_dien_ban_tay
import mediapipe as mp

print('MENU')
print('--------------------')
print('1. Nhan dien ban tay')
print('2. Di chuyen tro chuot')
print('--------------------')
print(mp.solutions.hands.Hands())
choice = input('Moi ban chon: ')
print(input)

if(choice == "1"):
    nhan_dien_ban_tay()
if(choice == "2"):
    di_chuyen_chuot()


