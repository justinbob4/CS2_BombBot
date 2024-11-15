import pymem, pymem.process, os, time, datetime, requests

offsets = requests.get('https://raw.githubusercontent.com/sezzyaep/CS2-OFFSETS/refs/heads/main/offsets.json').json()
client_dll = requests.get('https://raw.githubusercontent.com/sezzyaep/CS2-OFFSETS/refs/heads/main/client_dll.json').json()

dwPlantedC4 = offsets['client.dll']['dwPlantedC4']
m_nBombSite = client_dll['client.dll']['classes']['C_PlantedC4']['fields']['m_nBombSite']
m_bBeingDefused = client_dll['client.dll']['classes']['C_PlantedC4']['fields']['m_bBeingDefused']
m_bBombDefused = client_dll['client.dll']['classes']['C_PlantedC4']['fields']['m_bBombDefused']


def main():
    print("BombBot started.")
    time.sleep(3)
    os.system('cls')
    game_handle = pymem.Pymem("cs2.exe")
    client_dll = pymem.process.module_from_name(game_handle.process_handle, "client.dll").lpBaseOfDll
    then = None
    bomb_exploded = False
    while True:
        try:
            cplantedc4 = game_handle.read_ulonglong(client_dll + dwPlantedC4)
            cplantedc4 = game_handle.read_ulonglong(cplantedc4)
            planted = game_handle.read_bool(client_dll + dwPlantedC4 - 0x8)
            if planted:
                if then == None:
                    then = datetime.datetime.now()
                if int(40 - (datetime.datetime.now() - then).total_seconds()) < 0:
                    bomb_exploded = True
                site = game_handle.read_int(cplantedc4 + m_nBombSite)
                beingdefused = game_handle.read_bool(cplantedc4 + m_bBeingDefused)
                defused = game_handle.read_bool(cplantedc4 + m_bBombDefused)
                if site > 0:
                    site = "B"
                else:
                    site = "A"
                if not bomb_exploded:
                    if int(40 - (datetime.datetime.now() - then).total_seconds()) < 5:
                        print(f"Bomb cannot be defused!\nTime Left: {int(40 - (datetime.datetime.now() - then).total_seconds())}s")
                    elif int(40 - (datetime.datetime.now() - then).total_seconds()) < 10:
                        print(f"Bomb can be defused with kit!\nTime Left: {int(40 - (datetime.datetime.now() - then).total_seconds())}s")
                    elif not defused:
                        print(f"Bomb planted on: {site}\nDefusing: {beingdefused}\nTime Left: {int(40 - (datetime.datetime.now() - then).total_seconds())}s")
                    else:
                        then = None
                        print("Bomb Defused!")
                else:
                    print("Bomb Exploded!")
            else:
                then = None
                bomb_exploded = False
                print("Bomb not planted!")

            time.sleep(1)

            os.system('cls')

        except KeyboardInterrupt:
            break
        except:
            pass


if __name__ == "__main__":
    main()
