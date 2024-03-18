def ecriture_fichier(file,text):
    file.write(text)

def configureinterface(router, file):
    for interface in router.interfaces:
        ecriture_fichier(file, "interface " + interface.name + "\n")
        ip_ad = interface.ip_address
        if interface.name == "Loopback0" and ip_ad != None :
            ecriture_fichier(file, "ip address " + ip_ad + "\n")
        else : 
            if interface.ip_address != None :
                ecriture_fichier(file, " ip address " + ip_ad + "\n")
                process_id = router.hostname[1:]
                area = interface.area
                if area != None : 
                    ecriture_fichier(file," ip ospf " + process_id + " area " + area + "\n")
            ecriture_fichier(file, " negociation auto\n")
        if "LDP" in interface.routing_protocols :
            ecriture_fichier(file, " mpls ip\n")
        ecriture_fichier(file,"!\n")
