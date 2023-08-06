import sys, time

class copyright:
	__Version__ = "1.0.0"
	Z = '\033[1;31m' #قرمز
	X = '\033[1;33m' #زرد
	F = '\033[2;32m' #سبز
	C = "\033[1;97m" #سفید 
	B = '\033[2;36m'#ابی کم رنگ
	E  ="\033[0;90m" #خاکستری
	b = '\033[34m' 
	text=(f"\n\t\t{C}[+] {B}PyRobi {b}library {B}version {Z}1.0.0\n{C}\t\t[+] {B}Channel{b}Rubika  {B}@BotRobikpy\n\t\t{C}[+] {B}Copyright By Rubika ID: {b}@CuTe_MaNoo{C}\n\n")
	for txt in text:
		sys.stdout.write(txt)
		sys.stdout.flush()
		time.sleep(0.01)
