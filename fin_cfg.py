
def creation_texte_fin(router, ip_version, file):
    '''
    fonction qui crée le texte de la fin du fichier de configuration
    paramètres : hostname du routeur, id du routeur, as_rp du routeur, version de IP
    renvoi : texte
    '''
    ospf = False
    rip = False
    if ip_version == 4 :
        for interface in router.interfaces :
            if "OSPF" in interface.protocols and not ospf :
                ospf = True
                ecriture_fichier(file, "router ospf " + router.hostname[1:] + "\n")
                ecriture_fichier(file, " router-id " + router.id + "\n")
            if "OSPF" in interface.protocols and "eBGP" in interface.protocols :
                ecriture_fichier(file, " passive-interface " + interface.name + "\n")
        ecriture_fichier(file, "!\nip forward-protocol nd\n" + "!\n"*2)
        ecriture_fichier(file, "no ip http server\nno ip http secure-server\n")
    
    elif ip_version == 6 :
        ecriture_fichier(file, "ip forward-protocol nd\n" + "!\n"*2)
        ecriture_fichier(file, "no ip http server\nno ip http secure-server\n!\n")
        for interface in router.interfaces :
            if "RIP" in interface.protocols and not rip :
                rip = True
                ecriture_fichier(file, "ipv6 router rip ripng\n redistribute connected\n")
            elif "OSPF" in interface.protocols and not ospf :
                ospf = True
                ecriture_fichier(file, "ipv6 router ospf " + router.hostname[1:] + "\n")
                ecriture_fichier(file, " router-id " + router.id + "\n")
            if "OSPF" in interface.protocols and "eBGP" in interface.protocols :
                ecriture_fichier(file, " passive-interface " + interface.name + "\n")
            
    ecriture_fichier(file, "!\n"*4 + "control-plane\n" + "!\n"*2)

    ecriture_fichier(file, "line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")
    ecriture_fichier(file, "line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")

    ecriture_fichier(file, "line vty 0 4\n login\n" + "!\n"*2)
    ecriture_fichier(file, "end\n")

    return

def ecriture_fichier(file,text):
    file.write(text)