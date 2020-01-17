import requests, json, psutil, platform,time;
url="http://192.168.3.26:5000/api"

while(1):

    #Récupération load average 1min
    un, cinq, quinze = psutil.getloadavg()
    print(un)

    #Récupération de l'OS
    systeme = platform.system()
    
    #Récupération de l'hote
    nomHost = platform.node()
    
    #Récupération de noyau
    version = platform.release()
    
    #Récupération du type cpu
    cpu = platform.processor()
    
    #Récupération de la fréquence cpu
    cpuFre = psutil.cpu_freq().current
    
    # calculate the uptime
    uptime_file = open('/proc/uptime')
    uptime = uptime_file.readline().split()[0]
    uptime_file.close()
    uptime = float(uptime)
    (uptime,secs) = (int(uptime / 60), uptime % 60)
    (uptime,mins) = divmod(uptime,60)
    (days,hours) = divmod(uptime,24)
    uptime = 'up %d jour%s, %d:%02d' % (days, days != 1 and 's' or '', hours, mins)

    tabDisk = []
    listdisk = psutil.disk_partitions()
    for disk in listdisk:
        if (disk.fstype != 'squashfs'):
            detaildisk = psutil.disk_usage(disk.mountpoint)
            tabDisk.append({'fileSystem':disk.device,'size':detaildisk.total,'used':detaildisk.used,'available':detaildisk.free,'pourcentage':detaildisk.percent,'mounted':disk.mountpoint})
    
    with open('/home/rt/test/test.txt','r')as f:
        service=f.read()
        service=json.loads(service)
    
    #Mémoire utilisé
    memoireused = psutil.virtual_memory().used

    #Mémoire free
    memoirefree = psutil.virtual_memory().free


    #Mémoire buffers
    memoirebuffers = psutil.virtual_memory().buffers


    #Mémoire cached
    memoirecached = psutil.virtual_memory().cached

    service["id"]=1
    service["os"]= systeme
    service["nomh"]= nomHost
    service["noyl"]= version
    service["cputype"]= cpu
    service["cpufrequence"]= cpuFre
    service["up"]=uptime
    service["metrique"]=tabDisk
    service["moccupe"]=memoireused
    service["mlibre"]=memoirefree
    service["mbuffer"]=memoirebuffers
    service["mcached"]=memoirecached
    service["total"]=memoireused+memoirefree+memoirebuffers+memoirecached
    print(service)
    
    donnees = json.dumps(service)
    try:
        r = requests.post(url, data=donnees)
    except:
        pass
    time.sleep(60)
