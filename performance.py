#!/usr/bin/python3
import subprocess,datetime,pymysql

conn = pymysql.connect(database="BC",user="admin",password="admin",host="localhost")
cur=conn.cursor()

print("Temperature \n")
temp=subprocess.check_output("vcgencmd measure_temp | awk 'NR==1 {print $1}'", shell=True)
temp=temp[5:9]
print(temp)

print("Available-RAM")
RAM=subprocess.check_output("free | awk 'NR==2 {print $7}'",shell=True)
print(RAM)

print("CPU usage in %")
print("\n")
CPU=subprocess.check_output("top -n1 | awk '/Cpu\(s\):/ {print $2}'",shell=True)
print(CPU)

print("Disk Usage in %")
disk=subprocess.check_output("df -h --total | awk 'NR==11 {print $5}'",shell=True)
#disk=disk[:2]
print(disk)

data={'temp':temp,'CPU':CPU,'RAM':RAM,'disk':disk}
cur.execute("INSERT INTO performance (temp,RAM,CPU,disk) VALUES (%(temp)s,%(RAM)s,%(CPU)s,%(disk)s);",data)
conn.commit()
conn.close()
