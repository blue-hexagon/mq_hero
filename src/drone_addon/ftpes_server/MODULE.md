# Guide
To setup the FTPES server:

Modify config-variables in ´ftpes_installer.sh`
```json
DEPARTMENTS_STR="image,video"
HOST_IP="172.16.20.192"
COMPANY_NAME="agritech"
COMPANY_DOMAIN="agitech.rit.local"
```
Then execute:
```
chmod a+x ftpes_installer.sh
sudo ./ftpes_installer.sh
```