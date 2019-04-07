import os
#directory = "/Volumes/Video"
#if not os.path.exists(directory): os.makedirs(directory)
#os.system("open afp://nadina:Sherlock69@Rocinante._afpovertcp._tcp.local/BackUp")

os.system("/usr/bin/osascript -e \"try\" -e \"mount volume \\\"smb://nadina:Sherlock69@Rocinante/Video\\\"\" -e \"end try\"")
