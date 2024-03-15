# ipv6
def num_ip_6(router1, router2):
    num_router1 = int(router1.hostname[1:])
    num_router2 = int(router2.hostname[1:])
    if num_router1 < num_router2:
        numero = num_router1*100 + num_router2
    else :
        numero = num_router2*100 + num_router1
    return str(numero)
    
def generer_ip_6(router1,router2):
    num_router1 = int(router1.hostname[1:])
    num_router2 = int(router2.hostname[1:])
    numero = num_ip_6(router1, router2)
    if num_router1 < num_router2:
        combinaison_AS = router1.AS + ":"+ router2.AS
    else :
        combinaison_AS = router2.AS + ":" + router1.AS
    address_ip = "2001:" + combinaison_AS +":" + numero + ":0:0:0:" + router1.hostname[1:] + "/64"
    return address_ip

def generer_ip_loopback_6(router):
    address_ip = "2001:0:0:0:0:0:0:"+ router.hostname[1:] + "/128"
    return address_ip

#ipv4
def num_ip_4(router1, router2):
    num_router1 = int(router1.hostname[1:])
    num_router2 = int(router2.hostname[1:])
    if num_router1 < num_router2:
        numero = num_router1*10 + num_router2
    else :
        numero = num_router2*10 + num_router1
    return str(numero)
    
def generer_ip_4(router1,router2):

    numero = num_ip_4(router1, router2)
    address_ip = "192.168." + numero +"." + router1.hostname[1:] + " 255.255.255.0"
    return address_ip

def generer_ip_loopback_4(router):
    address_ip = "192.168.0."+ router.hostname[1:] + " 255.255.255.255"
    return address_ip
