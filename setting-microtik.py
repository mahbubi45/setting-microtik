#!/usr/bin/python

import paramiko

#input dari pengguna
host = input('Masukan IP Router: ')
usern = input('Masukan Username: ')
passwd = input('Masukan Password: ')
port = 22

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#connect ke mikrotik
ssh_client.connect(host, port=port, username=usern, password=passwd)

def add_ip_address():
    try:
        ip = input('Masukan IP Address: ')
        interface = input('Masukan nomor interface (1/2/3): ')
        # Menjalankan perintah untuk menambahkan IP Address
        command = f'/ip/address/add address={ip} interface=ether{interface}'
        ssh_client.exec_command(command)

        # Menampilkan daftar IP Address
        output = ssh_client.exec_command('/ip/address/print')[1].read().decode()
        print("Daftar IP Address:")
        print(output)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Menutup koneksi
        print('done')

def dhcpClient():
    try:
        # ask interface yang akan digunakan
        eth = input('Mau ether berapa? (1/2/3): ')

        # add DHCP Client
        command = f'/ip/dhcp-client/add interface=ether{eth}'
        ssh_client.exec_command(command)

        # show daftar DHCP Client
        output = ssh_client.exec_command('/ip/dhcp-client/print')[1].read().decode()
        print(output)

    except Exception as e:
        print(f"Error: {e}")
    
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna.")

    finally:
        ssh_client.close()

def natMasquerade():
    try:
        oInter = input('out interface (1/2/3)?: ')
        command = f'/ip/firewall/nat/ add chain=srcnat out-interface={oInter} action=masquerade'
        ssh_client.exec_command(command)

        output = ssh_client.exec_command('ip/firewall/nat/pr')[1].read().decode()
        print(output)
    
    except Exception as e:
        print(f"error: {e}")
    
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna.")

    finally:
        ssh_client.close()

def IpInfo():
    print("menampilkan tabel ip address")
    try:
        command = ssh_client.exec_command(f'/ip/address/print')[1].read().decode()
        print(command)
        
    except Exception as e:
        print(f"error:{e}")
    
    finally:
        ssh_client.close

def main():
    while True:
        choose = int(input("1. Menambahkan IP Address \n2. Menambahkan DHCP Client\n3. Nat-masquerade firewall\n4 menampilkan ip address router \npilih salah satu atau ketik 0 untuk mengakhiri: "))
        if choose == 1:
            add_ip_address()
        elif choose == 2:
            dhcpClient()
        elif choose == 3:
            natMasquerade()
        elif choose == 4:
            IpInfo()
        elif choose == 0:
            exit()
        else:
            print('error')
            exit()
        
if __name__ == "__main__":
    main()