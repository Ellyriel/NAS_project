def configureBGP(list_routers, router, ip_version, file):

    if router.AS != None :
        texte = "router bgp " + router.AS + "\n"
        texte += " bgp router-id " + router.id + "\n"
        texte += " bgp log-neighbor-changes\n"
        if ip_version == 6 :
            texte += " no bgp default ipv4-unicast\n"

        ecriture_fichier(file,texte)

        iBGP = []
        for interface in router.interfaces :
            if "iBGP" in interface.protocols and iBGP == [] :
                iBGP, routes_AS = neighbors_iBGP(list_routers, router.AS, router.hostname, ip_version)
                for address in iBGP :
                    ecriture_fichier(file," neighbor " + address + " remote-as " + router.AS + "\n")
                    ecriture_fichier(file," neighbor " + address + " update-source Loopback0\n")

        eBGP = [] 
        for interface in router.interfaces :
            if "eBGP" in interface.protocols and eBGP == []:
                eBGP = neighbors_eBGP(list_routers, router.hostname)
                for address in range(0, len(eBGP)-1, 2) :
                    ecriture_fichier(file, " neighbor " + eBGP[address] + " remote-as " + eBGP[address+1] + "\n")
        
        if ip_version == 6 :
            texte = " !\n" + " address-family ipv4\n" 
            texte += " exit-address-family\n"+" !\n"
            texte += " address-family ipv6\n"

        elif ip_version == 4 :
            texte = " !\n" + " address-family vpnv4\n"

        ecriture_fichier(file, texte)

        if eBGP != [] :
            if ip_version == 6 :
                prefixes = networks(routes_AS)
                for p in prefixes : 
                    ecriture_fichier(file,"  network " + p + "\n")
                for i in range (0,len(eBGP),2):
                    ecriture_fichier(file,"  neighbor " + eBGP[i] + " activate\n")
        if iBGP != [] :
            for i in iBGP:
                ecriture_fichier(file,"  neighbor " + i + " activate\n")
                if ip_version == 4 :
                    ecriture_fichier(file, "  neighbor " + i + " send-community extended\n")

        ecriture_fichier(file," exit-address-family\n"+"!\n")


def neighbors_iBGP(list_routers, AS_host, hostname, ip_version):
    '''
    retourne une listes qui contient toutes les adresses loopback des routeurs de l'AS de l'hôte dans la liste iBGP (sans l'adresse loopback de l'hôte). 
    retourne dans routes_AS les ad ip des routes de l'AS qui ne sont pas en Loopback
    '''
    iBGP = []
    routes_AS = []
    for router in list_routers:
        if (router.AS == AS_host and router.hostname != hostname):
            for interface in router.interfaces :
                if interface.name == "Loopback0" and "iBGP" in interface.protocols :
                    if ip_version == 6 :
                        ip = enleve_masque_6(interface.ip_address)
                    elif ip_version == 4:
                        ip = enleve_masque_4(interface.ip_address)
                    iBGP.append(ip)
                elif interface.name != "Loopback0" and "iBGP" in interface.protocols :
                    routes_AS.append(interface.ip_address)
    return iBGP, routes_AS

def neighbors_eBGP(list_routers, hostname):
    '''
    retourne une listes qui contient toutes les adresses des routeurs voisins en eBGP de l'AS de l'hôte et le numéro d'AS du voisin
    par exemple : eBGP = ["2001:111:112:34::1/64","112"]
    '''
    eBGP = []
    for router in list_routers:
        if (router.hostname != hostname and hostname in router.neighbors) :
            for interface in router.interfaces:
                if "eBGP" in interface.protocols :
                    ip = enleve_masque_4(interface.ip_address)
                    eBGP.append(ip)
                    eBGP.append(router.AS)
    return eBGP

def ecriture_fichier(file,text):
    file.write(text)

def enleve_masque_6(ip_masque):
    '''
    prend en paramètre une chaîne de caractère qui correspond à une adresse IP avec un masque 
    retourne l'adresse ip sans le masque
    '''
    indice = ip_masque.find("/")
    ip_sans_masque = ip_masque[:indice]
    return (ip_sans_masque)

def enleve_masque_4(ip_masque):
    '''
    prend en paramètre une chaîne de caractère qui correspond à une adresse IP avec un masque 
    retourne l'adresse ip sans le masque
    '''
    indice = ip_masque.find(" ")
    ip_sans_masque = ip_masque[:indice]
    #masque = ip_masque[indice+1:]
    return ip_sans_masque

def prefixe_ip_6(ip_masque):
    '''
    prend une adresse ip avec son masque
    retourne seulement le préfixe avec /masque
    '''
    liste_ip = decompose_ip_6(ip_masque)
    masque = liste_ip[8]
    prefixe = ""
    if masque == "/64" :
        for i in range(0,4,1):
            prefixe += liste_ip[i] + ":"
        prefixe += ":" + masque
    if masque == "/128" :
        prefixe = ip_masque
    return prefixe

def decompose_ip_6(ip):
    '''
    retourne une liste dont les éléments sont les partis séparées de l'adresse ip avec masque en argument
    '''
    ip_decomposee = []
    indice_precedent = -1
    # récupère les 8 nombres hexadécimaux de l'adresse dans une liste
    for i in range (len(ip)):
        if ip[i] == ":" or ip[i] == "/":
            groupe = ip[indice_precedent+1:i]
            ip_decomposee.append(groupe)
            indice_precedent = i
    # récupère le masque et le met en position 8 dans la liste ip_decomposee
    indice = ip.find("/")
    masque = ip[indice:]
    ip_decomposee.append(masque)
    return ip_decomposee

def networks (routes_AS):
    """
    récupère les adresses ip (pas loopback) de l'AS
    retourne une liste des préfixes de ces adresses sans doublons
    """
    prefixes = []
    for k in routes_AS : 
        prefixe = prefixe_ip_6(k)
        new = True
        for i in prefixes :
            if i == prefixe : 
                new = False
        if new == True :
            prefixes.append(prefixe)
    return prefixes
