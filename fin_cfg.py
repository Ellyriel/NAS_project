
def creation_texte_fin(hostname, id, as_rp, list_interfaces, ip_version, file):
    '''
    fonction qui crée le texte de la fin du fichier de configuration
    paramètres : hostname du routeur, id du routeur, as_rp du routeur, version de IP
    renvoi : texte
    '''
    if ip_version == 4 :
        ecriture_fichier(file, "router ospf " + hostname[1:] + "\n")
        ecriture_fichier(file, " router-id " + id + "\n!\n")
    else :
        print("ERROR : improper IP version")
        return
    
    ecriture_fichier(file, "ip forward-protocol nd\n" + "!\n"*2)
    ecriture_fichier(file, "no ip http server\nno ip http secure-server\n")
    
    ecriture_fichier(file, "!\n"*4 + "control-plane\n" + "!\n"*2)

    ecriture_fichier(file, "line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")
    ecriture_fichier(file, "line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")

    ecriture_fichier(file, "line vty 0 4\n login\n" + "!\n"*2)
    ecriture_fichier(file, "end\n")

    return

def ecriture_fichier(file,text):
    file.write(text)