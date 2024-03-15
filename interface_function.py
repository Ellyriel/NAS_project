"""
Le code doit renvoyer le texte suivant

interface Loopback0
 no ip address
 ipv6 address 2001:100::1/128
 ipv6 enable
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
interface GigabitEthernet1/0
 no ip address
 negotiation auto
 ipv6 address 2001:100:4:1::1/64
 ipv6 enable
 ipv6 rip ripng enable
!
interface GigabitEthernet2/0
 no ip address
 shutdown
 negotiation auto
!
"""

def ecriture_fichier(file,text):
    file.write(text)

def configureinterface(router, file):
    for interface in router.interfaces:
        ecriture_fichier(file, "interface " + interface.name + "\n")
        ip_ad = interface.ip_address
        if interface.name == "Looback0" and ip_ad != None :
            ecriture_fichier(file, "ip address" + ip_ad)
        else : 
            if interface.name == "FastEthernet0/0":
                    ecriture_fichier(file, "no ip address\nshutdown\nduplex full\n")
            elif interface.ip_address != None :
                ecriture_fichier(file, " ip address " + ip_ad + "\n")
                process_id = router.hostname[1:]
                area = interface.area
                if area != None : 
                    ecriture_fichier(file," ip ospf " + process_id + " area " + area + "\n")
            ecriture_fichier(file, " negociation auto\n")
        ecriture_fichier(file,"!\n")
