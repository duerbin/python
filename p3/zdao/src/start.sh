#!/bin/bash

#########################################################################################
################                 service info ###########################################
#########################################################################################
ALIAS[0]="gls";
ALIAS[1]="license";
ALIAS[2]="dds";
ALIAS[3]="cms";
ALIAS[4]="ucx";
ALIAS[5]="datakeeper";
ALIAS[6]="rm";
ALIAS[7]="ucds";
ALIAS[8]="dcs";
ALIAS[9]="ss";
ALIAS[10]="eas";
ALIAS[11]="dae";
ALIAS[12]="psr";
ALIAS[13]="fps";
ALIAS[14]="dcproxy";
ALIAS[15]="daengine";
ALIAS[16]="tsr";
ALIAS[17]="tsrl";
ALIAS[18]="agentproxy";

PROC[0]="Glsserver";
PROC[1]="LicenseServer";
PROC[2]="DDSServer";
PROC[3]="cmsserver";
PROC[4]="ucxserver";
PROC[5]="DataKeeper";
PROC[6]="RMServer";
PROC[7]="UCDServer";
PROC[8]="dcs";
PROC[9]="StatSchedule";
PROC[10]="EAService";
PROC[11]="dae";
PROC[12]="psr";
PROC[13]="fpsvr";
PROC[14]="dcproxy";
PROC[15]="daengine";
PROC[16]="tsrecadsrv";
PROC[17]="tsr_longlink";
PROC[18]="AgentProxy";

DIR[0]="./bin";
DIR[1]="./bin/license";
DIR[2]="./bin";
DIR[3]="./bin";
DIR[4]="./bin";
DIR[5]="./bin";
DIR[6]="./bin";
DIR[7]="./bin";
DIR[8]="./bin";
DIR[9]="./bin";
DIR[10]="./bin";
DIR[11]="./bin";
DIR[12]="./bin";
DIR[13]="./bin";
DIR[14]="./bin";
DIR[15]="./bin";
DIR[16]="./qnrecsrv/tsr_normal";
DIR[17]="./qnrecsrv/tsr_longlink";
DIR[18]="./bin";

ARGV[0]="";
ARGV[1]="";
ARGV[2]="--config.main=../cfg/dds_config.cfg";
ARGV[3]="--config.main=../etc/config.cms2";
ARGV[4]="--config.main=../etc/config.ucx";
ARGV[5]="";
ARGV[6]="";
ARGV[7]="";
ARGV[8]="";
ARGV[9]="../cfg/ss_config.cfg";
ARGV[10]="../cfg/eas_config.cfg";
ARGV[11]="";
ARGV[12]="";
ARGV[13]="--config ../cfg/fps.cfg";
ARGV[14]="";
ARGV[15]="";
ARGV[16]="";
ARGV[17]="";
ARGV[18]="";

PROC_COUNT=19
CHECK_TIME=10

#CHECK_LOGFILE="check.log"
CHECK_LOGFILE="/dev/null"

#########################################################################################

################################################################################33

usage()
{
	echo  "Usage: start.sh [options] service1 [,service2..]";
	echo  "Start/stop services or show files version" 
	echo  "  -c    Get coredump, used with -k."
	echo  "  -d    Run a daemon script for service"
	echo  "  -f    Force kill service, used with -k" 
	echo  "  -h    Print help infomation"
	echo  "  -k    Kill service"
	echo  "  -o    Get owner authority [ -o user ]"                       
	echo  "  -r    Restart service "
	echo  "  -s    Show service status"
	echo  "  -v    Show file version"
	echo  "  list  Show all services status"
	echo  "  Note: If no option ,default to start a service. "
	echo  ""
	echo  "Valid shortcut for services:"
	echo  "  gls license dds cms ucx datakeeper ucds dcs ss eas daengine psr fps"
	echo  "  "
	echo  "Example: "
	echo  "  \"start.sh list\"    View status of all services."
	echo  "  \"start.sh gls\"     Start Glsserver."
	echo  "  \"start.sh -d gls\"  Start Glsserver with a daemon."
	echo  "  \"start.sh gls dds\" Start Glsserver and DDSServer."
	echo  "  \"start.sh -v gls\"  Show Glsserver version."
	echo  "  \"start.sh -s gls\"  Show Glsserver status."
	echo  "  \"start.sh -k gls\"  Stop Glsserver."
	echo  "  \"start.sh -r gls\"  Restart Glsserver."
	echo  "  \"start.sh -kd gls\" Stop Glsserver and its daemon."
	echo  "  \"start.sh -kf gls\" Force,kill Glsserver immediately."
	echo  "  \"start.sh all\"     Start all services at once."
	echo  "  \"start.sh -k all\"  Stop all services at once."
}

echo_w()
{
	width=`expr 60 - $1`
	f=`printf "%ds" $width`
	printf  "%$f\n"  "$2"
}
set_ulimit() 
{
    core_limit=`ulimit -c`
    [ $core_limit="0" ]
    if [ $? -eq "0" ]; then
        ulimit -c unlimited
        #echo "ulimit set"
    fi;
}

checkDaemonRunning()
{
	ret=`ps -u $WHO -o pid -o comm -o cmd|grep "$SCRIPT_NAME -a -d $1"|grep -v grep|awk '{print $1}'`;
	echo $ret
	if [ "$ret" = "" ]; then
		return 0;
	else
		return 1;
	fi
}

checkRunning()
{
	ret=`ps -u $WHO -o pid -o comm|grep $1|awk '{print $1}'`;
	echo $ret

	if [ -z "$ret" ]; then
		return 0;
	else
		return 1;
	fi
}


show_status()
{
	proc=${PROC[$1]}
	ret=`checkRunning $proc`;
	if [ $? -ne 0 ];then
		str="$proc (pid $ret)";
		len=`expr length "$str"`;
		echo -n $str
		ret=`checkDaemonRunning ${ALIAS[$1]}`;
		if [ $? -ne 0 ];then
			echo_w `expr $len - 10` "[daemon][[32mrunning[0m]";
		else
			echo_w `expr $len - 10` "[[32mrunning[0m]";
		fi
	else
		echo -n $proc
		len=`expr length "$proc"`;
		echo_w `expr $len - 10` "[[31mstopped[0m]";
	fi
}

restart_proc()
{
	kill_proc $1;
#	[ $? -ne 0 ]&& return; 		
	start_proc $1;
}

kill_daemon()
{
	len=`expr length "${PROC[$1]} daemon"`
	ret=`checkDaemonRunning ${ALIAS[$1]}`;	
	if [ $? -ne 0 ];then
		echo -n "stoping ${PROC[$1]} daemon .";	
		for pid in "$ret"
		do
			kill -9 $pid;
		done
		echo_w $len "[[31mstopped[0m]";
	fi	
}
kill_proc()
{
	result=1;
	[ "$DAEMON" = "true" ] && kill_daemon $1;
	proc=${PROC[$1]}
	echo -n "stoping $proc .";	
	len=`expr length "$proc"`
	ret=`checkRunning $proc`;	
	if [ $? -ne 0 ];then
		for pid in "$ret"		
		do
			if [ "$FORCE" = "true" ];then
				kill -9 $pid;
			elif [ "$CORE" = "true" ];then
				kill -6 $pid;
			else
				kill -9 $pid;
			fi
			for((t=0; t<10; t++))
			do
				echo -n "."
				len=`expr $len + 1`
				ret=`checkRunning $proc`;	
				if [ $? -ne 0 ];then
					sleep 1;
				else
					echo_w $len "[[31mstopped[0m]";
					result=0;
					break;
				fi
				if [ $t -eq 8 ];then
					echo_w $len "[[32mrunning[0m]";
					KILLFAILED=true;
				fi
					
			done
		done
	else
		echo -n ".."
		echo_w `expr $len + 2` "[[31mstopped[0m]";
	fi
	return $result;
}

start_daemon()
{
	$SCRIPT_NAME -a -d ${ALIAS[$1]} >/dev/null 2>&1 &
	echo  "starting daemon for ${PROC[$1]}... OK";				
#	ret=`checkDaemonRunning ${ALIAS[$1]}`;
#	if [ $? -ne 0 ];then
#		echo  "already a instance running ...";
#	else	
#		$SCRIPT_NAME -a -d ${ALIAS[$1]} >/dev/null 2>&1 &
#		echo  "starting daemon for ${PROC[$1]}... OK";				
#	fi
}

start_real_daemon()
{
	while true
	do
		start_proc $1
		if [ $? = 2 ];then
			echo "`date`: start daemon ${PROC[$1]} ok" >> daemon.log
		elif [ $? = 3 ];then
			echo "`date`: start daemon ${PROC[$1]} failed" >> daemon.log
		fi
		sleep $CHECK_TIME
	done		
}

start_proc()
{
	proc=${PROC[$1]}	
	echo -n "starting $proc ";
	len=`expr length "$proc"`
        ret=`checkRunning $proc`;
	cret=$?;
	if [ "$ISLIST" != "true" ]; then
		echo "`date` check $proc return=[$ret] [$cret]" >> $CHECK_LOGFILE
	fi
        if [ $cret -ne 0 ] || [ "$ret" != "" ]
	then
		echo -n ".."
		echo_w `expr $len + 2` "[[31mFAILED[0m]"
		echo "Error:$proc already have a instance (pid $ret)";
		return 1
        else
            cd ${DIR[$1]}
                nohup ./$proc ${ARGV[$1]}  >/dev/null 2>&1 &
            cd - >> /dev/null 2>&1
            for t in 1 2 3
            do 
            	echo -n "."	
            	len=`expr $len + 1`
            	sleep 1
            done
            echo -n "."
            ret=`checkRunning $proc`;
            if [ $? -ne 0 ];then
           	echo_w `expr $len + 1` "[[32m  OK  [0m]";
            	return 2
            else
           	echo_w `expr $len + 1` "[[31mFAILED[0m]";
            	return 3
            fi
        fi
}

show_version()
{
	echo "====================== ${PROC[$1]} Version Info ======================";	
	cd bin
	./${PROC[$1]} --version
	cd ..		
}



do_process()
{
	if [ "$KILL" = "true" ];then
		kill_proc $1;
		return;
	fi
	if [ "$RESTART" = "true" ];then
		restart_proc $1;	
		return;
	fi
		
	if [ "$VERSION" = "true" ];then
		show_version $1;
	fi
	
	if [ "$STATUS" = "true" ];then
		show_status $1;
	fi
	
	if [ "$START" = "true" ];then
		start_proc $1;
	fi

	if [ "$DAEMON" = "true" ] && [ "$EXPAND" != "true" ];then
		start_daemon $1
	fi

	if [ "$DAEMON" = "true" ] && [ "$EXPAND" == "true" ];then
		start_real_daemon $1;
	fi
}

##=========================================================================================================
##=========================================================================================================
##=
##=========================================================================================================
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/lib:`pwd`/oracle
export TNS_ADMIN=`pwd`/oracle

KILL=false;
VERSION=false;
STATUS=false;
START=true;
FORCE=false;
CORE=false;
DAEMON=false;
RESTART=false;
EXPAND=false;
WHO=`whoami`;
OWN=`stat -c %U $0`
KILLFAILED=false;
SCRIPT_NAME=$0
ISLIST=false;


while getopts :krvsahfcdo: OPTION
do
	case $OPTION in
	a)
		EXPAND=true;
		START=false;;
	k)
		KILL=true;
		START=false;;
	v)
		START=false;
		VERSION=true;;
	s)
		START=false;
		STATUS=true;;
	f)
		FORCE=true;;
	r)
		START=false;
		RESTART=true;;
	c)
		START=false;
		CORE=true;;
	o)
		WHO=$OPTARG;;
	d)
		START=false;
		DAEMON=true;;
	h)
		usage;
		exit 0;;
	\?)
		echo "start.sh: invalid option"
		echo "Tyr \"start.sh -h\" for more infomation."
		exit;;
	esac
done
	

shift `expr $OPTIND - 1`;

if [ "$#" = "0" ];then
	echo "start.sh: missing operand." 
	echo "Try \"start.sh -h\" for more infomation."
	exit 1;
fi

if [ $OWN != $WHO ];then
	echo "start.sh:sorry [$WHO], the owner is [$OWN]."
	echo "Add option \"-o $OWN\" to ignore this."
	echo "Try \"start.sh -h\" for more infomation."
	exit 1;
fi

set_ulimit;

for proc in "$@"
do
	num=-1
	proc=`tr A-Z a-z <<< $proc`;
	if [ "$proc" = "list" ];then
		ISLIST=true;
		for((i=0; i<PROC_COUNT; i++))
		do
			show_status $i;
		done	
		exit 0;
		
	fi	
	if [ "$proc" = "all" ];then
		for((i=0; i<PROC_COUNT; i++))
		do
			do_process $i;	
		done	
		exit 0;
	fi
	for((i=0; i<PROC_COUNT; i++))
	do
		if [ "$proc" = "${ALIAS[$i]}" ]; then
			num=$i;	
			break;
		fi
	done
	if [ $num -ne -1 ];then 
		do_process $num;
	else
		echo "start.sh: wrong service name [$proc]. "
		echo "Try \"start.sh -h\" for more infomation."
		exit 1;
	fi
done

if [ "$KILLFAILED" = "true" ];then
	echo "  ----"
	echo "If they are still running , check it later use command \"start.sh list\"";
	echo "Also can use \"start.sh -kf SERVICES\" to kill them immediately"
fi

exit 0;
	
