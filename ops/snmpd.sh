SYS_NAME="ftp01"
SYS_LOCATION="ZBC-DC"
sudo apt update
sudo apt upgrade -y
sudo apt install ufw snmp snmpd
sudo truncate -s 0 /etc/snmp/snmpd.conf


sudo tee /etc/snmp/snmpd.conf >/dev/null <<EOF
agentAddress udp:161
sysServices 72
rocommunity RITtest 127.0.0.1/32
rocommunity RITadmin 172.16.20.7/32
sysLocation ${SYS_LOCATION}
sysContact patr121@zbc.dk,tobi801j@zbc.dk
sysName ${SYS_NAME}-agritech
# Specify proper OIDs...
view altingv2c included .1
view altingv3 included .1
access notConfigGroup "" v2c noauth exact altingv2c none none
access notConfigGroup "" usm authPriv exact altingv3 none none
EOF

if ! sudo grep -q 'snmpacc' /var/lib/snmp/snmpd.conf; then
  sudo net-snmp-create-v3-user -ro \
    -a SHA -A 'KOde12345!!?' \
    -x AES -X 'KOde12345!!?' \
    snmpacc
fi
#snmpwalk -v3 -l authPriv -u snmpacc -a SHA -A 'KOde12345!!?' -x AES -X 'KOde12345!!?' '127.0.0.1' system

sudo ufw allow 22
sudo ufw allow from 172.16.20.0/24 to any port 161 proto udp

sudo systemctl enable snmpd
sudo systemctl restart snmpd

sudo ufw --force enable
sudo ufw reload