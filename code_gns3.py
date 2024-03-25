import json
import bgp
import interface_function
import debut_cfg
import fin_cfg
import automatic_ip
import os
import sys

with open("data_extent.json") as file:
    data = json.load(file)
    
ip_version = int(data["ip_version"])

if ip_version != 4 and ip_version != 6 :
    print("ERROR : improper IP version")
    sys.exit()

# classe définissant un routeur
class Router :

    def __init__ (self, hostname, id, AS, area, neighbors, interfaces) :
        self.hostname = hostname
        self.id = id
        self.AS = AS
        self.area = area
        self.neighbors = neighbors
        self.interfaces = interfaces
        
    def __str__(self):
        return f'[{self.hostname} : AS n°{self.AS} and area n°{self.area}, Router ID {self.id}, {len(self.neighbors)} neighbor(s), {len(self.interfaces)} interface(s)]'
    
    def __repr__(self):
        return f'Router {self.hostname}'


# classe définissant une interface d'un routeur
class Interface :

    def __init__ (self, name, ip_address, protocols, connected_to, client) :
        self.name = name
        self.ip_address = ip_address
        self.protocols = protocols
        self.connected_to = connected_to
        self.client = client

    def __str__(self):
        return f'[Interface {self.name} : IP Address {self.ip_address}, Routing Protocols {self.protocols}, Connected to {(self.connected_to)}]'
    
    def __repr__(self):
        return f'Interface {self.name}'


# mise en forme des données de chacun des routeurs
list_routers = []
for router in data["router"]:
    hostname = router["hostname"]
    id = router["id"]
    AS = router["AS"]
    area = router["area"]
    neighbors = router["neighbors"]

    list_interfaces = []
    for interface in router["interfaces"]:
        name = interface["name"]
        ip_address = None
        protocols = interface["protocols"]
        connected_to = interface["connected_to"]
        client = interface["client"]
        list_interfaces.append(Interface(name, ip_address, protocols, connected_to, client))

    list_routers.append(Router(hostname, id, AS, area, neighbors, list_interfaces))


# création des adresses ipv4 ou ipv6 pour chaque interface des routeurs
for router in list_routers:
    for interface in router.interfaces:
        if interface.name == "Loopback0":
            if ip_version == 4 :
                interface.ip_address = automatic_ip.generer_ip_loopback_4(router)
            elif ip_version == 6 :
                interface.ip_address = automatic_ip.generer_ip_loopback_6(router)
        if interface.connected_to != None and interface.name != "Loopback0":
            a = 0
            router2 = list_routers[a]
            while router2.hostname != interface.connected_to and a < len(list_routers):
                a += 1
                router2 = list_routers[a]
            if ip_version == 4 :
                interface.ip_address = automatic_ip.generer_ip_4(router,router2)
            elif ip_version == 6 :
                interface.ip_address = automatic_ip.generer_ip_6(router,router2)


# affiche la liste des routeurs, leurs interfaces et leurs voisins
def affichage(list_routers):
    for router in list_routers:
        print(router)
        print("List of neighbor(s) :")
        print(f'    {router.neighbors}')
        print("List of interface(s) :")
        for interface in router.interfaces:
            print(f'    {interface}')
        print("------------")
    print(list_routers)

# génération des fichiers de configuration

def creation_fichier(router):
    name = "i"+ router.hostname[1:] + "_startup-config.cfg"
    #f = open(name,"w")
    #return f
    road = os.path.join('./NAS_GNS3/project-files/dynamips')
    dossiers = [f for f in os.listdir(road)]
    i = 0
    while i < len(dossiers) :
        road_dossier = os.path.join(road + '/' + dossiers[i] +'/configs')
        fichier = os.listdir(road_dossier)
        if name in fichier:
            f = open(road_dossier + '/' + name,"w")
            return f
        i += 1 

for i in range (len(list_routers)):
    router = list_routers[i]
    fichier_config = creation_fichier(router)
    debut_cfg.creation_texte_debut(list_routers, router, ip_version, fichier_config)
    interface_function.configureinterface(router, ip_version, fichier_config)
    bgp.configureBGP(list_routers, router, ip_version, fichier_config)
    fin_cfg.creation_texte_fin(router, ip_version, fichier_config)
    print(f"Config routeur {i+1} complète")

