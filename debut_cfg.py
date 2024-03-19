def creation_texte_debut(router, ip_version, file):
    '''
    fonction qui crée un texte. Dans notre cas, ce texte sera réécrit plus tard dans le fichier de configuration, et il correspond au début du fichier de configuration
    paramètres : routeur, version de IP utilisée pour notre réseau
    renvoi : texte
    '''
    ecriture_fichier(file, "!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\n")
    ecriture_fichier(file, "hostname "+ router.hostname + "\n!\n")

    ecriture_fichier(file, "boot-start-marker\nboot-end-marker\n" + "!\n"*3)

    ecriture_fichier(file,"no aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n" + "!\n"*6)

    if ip_version == 6 :
        ecriture_fichier(file, "no ip domain lookup\nipv6 unicast-routing\nipv6 cef\n")
    elif ip_version == 4 :
        ecriture_fichier(file, "no ip domain lookup\nno ipv6 cef\n")
    
    ecriture_fichier(file,"!\n"*2)

    ecriture_fichier(file, "multilink bundle-name authenticated\n" + "!\n"*9)
    ecriture_fichier(file, "ip tcp synwait-time 5\n" + "!\n"*12)
    return

def ecriture_fichier(file,text):
    file.write(text)
