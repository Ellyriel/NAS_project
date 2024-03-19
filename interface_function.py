def ecriture_fichier(file,text):
    file.write(text)

def configureinterface(router, ip_version, file):
    for interface in router.interfaces:
        ecriture_fichier(file, "interface " + interface.name + "\n")
        
        if ip_version == 4 :
            ecriture_fichier(file, " ip address " + interface.ip_address + "\n")
            if "OSPF" in interface.protocols :
                process_id = router.hostname[1:]
                ecriture_fichier(file," ip ospf " + process_id + " area " + router.area + "\n")
            if interface.name != "Loopback0":
                ecriture_fichier(file, " negociation auto\n")
            if "LDP" in interface.protocols :
                ecriture_fichier(file, " mpls ip\n")
            ecriture_fichier(file,"!\n")
        
        elif ip_version == 6:
            ecriture_fichier(file," no ip address \n")
            if interface.name != "Loopback0":
                ecriture_fichier(file, " negociation auto\n")
            ecriture_fichier(file, " ipv6 address " + interface.ip_address + "\n")
            ecriture_fichier(file," ipv6 enable\n")
            if "RIP" in interface.protocols :
                ecriture_fichier(file," ipv6 rip ripng enable \n")
            if "OSPF" in interface.protocols :
                process_id = router.hostname[1:]
                ecriture_fichier(file," ipv6 ospf " + process_id + " area " + router.area + "\n")
            ecriture_fichier(file,"!\n")
        
        
        
        
       
