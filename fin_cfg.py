
def creation_texte_fin(hostname, id, as_rp, list_interfaces, ip_version, file):
    '''
    fonction qui crée le texte de la fin du fichier de configuration
    paramètres : hostname du routeur, id du routeur, as_rp du routeur, version de IP
    renvoi : texte
    '''
    if ip_version == 4 :
        if as_rp == "OSPF" :
            ecriture_fichier(file, "router ospf " + hostname[1:] + "\n")
            ecriture_fichier(file, " router-id " + id + "\n!\n")
        ecriture_fichier(file, "ip forward-protocol nd\n" + "!\n"*2)
        ecriture_fichier(file, "no ip http server\nno ip http secure-server\n")
    elif ip_version == 6 :
        ecriture_fichier(file, "ip forward-protocol nd\n" + "!\n"*2)
        ecriture_fichier(file, "no ip http server\nno ip http secure-server\n!\n")
        if as_rp == "RIP" :
            ecriture_fichier(file, "ipv6 router rip ripng\n redistribute connected\n")
        if as_rp == "OSPF" :
            ecriture_fichier(file, "ipv6 router ospf " + hostname[1:] + "\n router-id " + id + "\n")
            for interface in list_interfaces :
                if interface.routing_protocols != None and "eBGP" in interface.routing_protocols :
                    ecriture_fichier(file, " passive-interface " + interface.name + "\n")
    
    ecriture_fichier(file, "!\n"*4 + "control-plane\n" + "!\n"*2)

    ecriture_fichier(file, "line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")
    ecriture_fichier(file, "line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")

    ecriture_fichier(file, "line vty 0 4\n login\n" + "!\n"*2)
    ecriture_fichier(file, "end\n")

    return

def ecriture_fichier(file,text):
    file.write(text)