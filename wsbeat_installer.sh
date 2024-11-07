#! /bin/bash

clear

WSBEAT_CONFIGURATION_FOLDER=/etc/WSBeat-Suite/WSBeat/configuration
WSBEAT_AGENT_CONFIGURATION_FOLDER=/etc/WSBeat-Suite/WSBeat-Agent/configuration
WSBEAT_LOGS_FOLDER=/var/log/WSBeat
WSBEAT_KEY=/etc/WSBeat-Suite/WSBeat/configuration/key

echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m"
echo -e "\e[96mAuthor: Erick Roberto Rodríguez Rodríguez\e[0m"
echo -e "\e[96mEmail: erodriguez@tekium.mx, erickrr.tbd93@gmail.com\e[0m"
echo -e "\e[96mGitHub: https://github.com/erickrr-bd/Telk-Alert"
echo -e "\e[96mInstaller for WSBeat v1.0 - October 2024\e[0m"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "Do you want to install or update WSBeat? (I/U)"
read opc
if [ $opc = "I" ] || [ $opc = "i" ]; then
	#echo -e "\e[96mStarting the Telk-Alert installation process\e[0m\n"
	echo -e "\e[96mCreating user and group \"wsbeat_user\" and \"wsbeat_group\"\e[0m\n"
	if grep -w ^wsbeat_group /etc/group > /dev/null; then
		echo -e "\e[0;31m\"wsbeat_group\" already exists\e[0m\n"
	else
		groupadd wsbeat_group
		echo -e "\e[0;32m\"wsbeat_group\" group created\e[0m\n"
	fi
	if id wsbeat_user &> /dev/null; then
		echo -e "\e[0;31m\"wsbeat_user\" already exists\e[0m"
	else
		useradd -M -s /bin/nologin -g wsbeat_group -d /home/wsbeat_user wsbeat_user
		echo -e "\e[0;32m\"wsbeat_user\" user created\e[0m\n"
	fi
	sleep 3
	#echo -e "\e[96mCreating the service for Telk-Alert and Telk-Alert-Agent\e[0m\n"
	#cd $dir
	#cp wsbeat.service /etc/systemd/system/
	#cp telk-alert-agent.service /etc/systemd/system
	#systemctl daemon-reload
	#systemctl enable wsbeat.service
	#systemctl enable telk-alert-agent.service
	#echo -e "\e[96mServices created\e[0m\n"
	sleep 3
	#echo -e "\e[96mInstalling Telk-Alert\e[0m\n"
	#cp -r WSBeat-Suite /opt
	if [ ! -d "$WSBEAT_CONFIGURATION_FOLDER" ]; 
	then
		mkdir -p $WSBEAT_CONFIGURATION_FOLDER
	fi
	if [ ! -d "$WSBEAT_AGENT_CONFIGURATION_FOLDER" ]; 
	then
		mkdir -p $WSBEAT_AGENT_CONFIGURATION_FOLDER
	fi
	if [ ! -d "$WSBEAT_LOGS_FOLDER" ]; 
	then
		mkdir -p $WSBEAT_LOGS_FOLDER
	fi
	#echo -e "\e[96mTelk-Alert installed\e[0m\n"
	sleep 3
	echo -e "\e[96mCreating encryption key\e[0m\n"
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $WSBEAT_KEY
$encryption_key
EOF
	echo -e "\e[96mEncryption key created\e[0m\n"
	sleep 3
	echo -e "\e[96mMaking changes to Telk-Alert\e[0m\n"
	#chown telk_alert:telk_alert -R /opt/Telk-Alert-Suite
	chown wsbeat_user:wsbeat_group -R /etc/WSBeat-Suite
	chown wsbeat_user:wsbeat_group -R /var/log/WSBeat
	echo -e "\e[96mChanges made\e[0m\n"
	sleep 3
	#echo -e "\e[96mCreating aliases for Telk-Alert-Tool\e[0m\n"
	#echo "alias Telk-Alert-Tool='/opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py'" >> ~/.bashrc
	#echo -e "\e[96mAlias created\e[0m\n"
	#sleep 3
	#echo -e "\e[96mRunning Telk-Alert-Tool\e[0m\n"
	#sleep 3
	#cd /opt/Telk-Alert-Suite/Telk-Alert-Tool
	#python3 Telk_Alert_Tool.py
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	echo -e "\e[96mStarting the Telk-Alert update\e[0m\n"
	sleep 3
	echo -e "\e[96mStopping and updating the Telk-Alert and Telk-Alert-Agent service\e[0m\n"
	systemctl stop telk-alert.service
	systemctl stop telk-alert-agent.service
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	echo -e "\e[96mUpdated services\e[0m\n"
	sleep 3
	echo -e "\e[96mUpdating Telk-Alert\e[0m\n"
	cp -r Telk-Alert-Suite /opt
	chown telk_alert:telk_alert -R /opt/Telk-Alert-Suite
	echo -e "\e[96mTelk-Alert updated\e[0m\n"
	sleep 3
	echo -e "\e[96mRunning Telk-Alert-Tool\e[0m\n"
	sleep 3
	cd /opt/Telk-Alert-Suite/Telk-Alert-Tool
	python3.9 Telk_Alert_Tool.py
fi