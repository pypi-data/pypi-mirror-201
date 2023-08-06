#
# Copyright (c) 2012-2014 Fixpoint Inc. All rights reserved.
# ---
#
#   セットアッププログラム用共通関数定義
#
#
shopt -s extglob
#
# バージョン情報はパッケージングの際に置換される(Makefile参照)
#
BRANCH=$(python -c 'exec("try: import kompira_common.version; print(kompira_common.version.BRANCH)\nexcept Exception: pass")')
VERSION=$(python -c 'exec("try: import kompira_common.version; print(kompira_common.version.VERSION)\nexcept Exception: pass")')
SHORT_VERSION=$(python -c 'exec("try: import kompira_common.version; print(kompira_common.version.SHORT_VERSION)\nexcept Exception: pass")')


trap "interrupt" SIGHUP SIGINT SIGQUIT SIGABRT SIGTERM

REQUIRES_ARCH="x86_64"
REQUIRES_PYTHON3="Python 3.[6].*"
REQUIRES_POSTGRES="12"
REQUIRES_SYSTEM_CENT="CentOS*release [78]*"
REQUIRES_SYSTEM_AMZN="Amazon Linux release 2 *"
REQUIRES_SYSTEM_RHEL="Red Hat Enterprise Linux* release [78].*"

#
# システム種別チェック
#
: ${SYSTEM_RELEASE:=}
: ${RHEL_VERSION:=$(rpm -E '%{rhel}' 2>/dev/null)}
if [ -z "$SYSTEM_RELEASE" ]; then
    for file in /etc/system-release /etc/redhat-release; do
        if [ -f $file ]; then SYSTEM_RELEASE=$(< $file); break; fi
    done
fi
case $SYSTEM_RELEASE in
    $REQUIRES_SYSTEM_CENT) SYSTEM="CENT"; SYSTEM_NAME="cent$RHEL_VERSION" ;;
    $REQUIRES_SYSTEM_RHEL) SYSTEM="RHEL"; SYSTEM_NAME="rhel$RHEL_VERSION" ;;
    $REQUIRES_SYSTEM_AMZN) SYSTEM="AMZN"; SYSTEM_NAME="amzn" ;;
    *)                     SYSTEM="unknown" ;;
esac
if [ -z "$SYSTEM_RELEASEVER" ]; then
    SYSTEM_RELEASEVER=$(echo "$SYSTEM_RELEASE" | sed -r -e "s/.*release ([0-9.]+).*/\1/")
fi

#
# CentOS 8.3以降は HighAvailability -> ha に名称変更
#
case $SYSTEM_RELEASEVER in
    8.[0-2].*) CENT8_HA_REPONAME="HighAvailability" ;;
    *) CENT8_HA_REPONAME="ha" ;;
esac

#
# [RHEL] RHUI チェック
#
if [ -z "$RHUI_MODE" ]; then
    if [ $SYSTEM == "RHEL" ] && grep -qiE "^\[rhui\b.*\]" /etc/yum.repos.d/*.repo; then
        RHUI_MODE=true
    else
        RHUI_MODE=false
    fi
fi

#
# systemd 判別チェック
#
if [ "$(cat /proc/1/comm 2>/dev/null)" = "systemd" ]; then
    SYSTEMD=true
else
    SYSTEMD=false
fi
SHOW_OPTIONS="SYSTEM SYSTEM_NAME SYSTEM_RELEASE SYSTEM_RELEASEVER PLATFORM_PYTHON PYTHON SYSTEMD TMPDIR"
: ${PLATFORM_PYTHON:=$((which /usr/libexec/platform-python || which python) 2>/dev/null)}
: ${PYTHON:=$((which python38 || which python3.8 || which python37 || which python3.7 || which python36 || which python3.6 || which python3 || which python) 2>/dev/null)}
: ${PIP:=$(which pip 2>/dev/null)}
: ${SERVICE:=service}
: ${SYSTEMCTL:=systemctl}
: ${INSTALL:=install}
: ${SUBSCRIPTION_MANAGER:=$(which subscription-manager 2>/dev/null)}
: ${NETWORK_SCRIPTS_DIR:=/etc/sysconfig/network-scripts}
: ${TMPDIR_TEMPLATE:=".tmp.install-$(date +%Y%m%d-%H%M).XXXX"}
: ${TMPDIR:="/tmp"}
: ${TMPFILES_CONF_DIR:="/usr/lib/tmpfiles.d"}
: ${SETUP_TYPE:="Setup"}
: ${SKIP_CLEAN_YUM_CACHE:=true}
: ${OFFLINE_MODE:=false}

#
# runuser/su チェック
#
if [ -z "$SU" ]; then
    if [ -x /sbin/runuser ]; then
        SU=/sbin/runuser
    else
        SU=su
    fi
fi

#
# variables for Kompira
#
: ${KOMPIRA_USER:=kompira}
: ${KOMPIRA_GROUP:=kompira}
: ${KOMPIRA_HOME:=/opt/kompira}
: ${KOMPIRA_VAR_DIR:=/var/opt/kompira}
: ${KOMPIRA_LOG_DIR:=/var/log/kompira}
: ${KOMPIRA_BACKUP:="$KOMPIRA_VAR_DIR/kompira_backup.json.gz"}
: ${KOMPIRA_ENV:="$KOMPIRA_HOME"}
: ${KOMPIRA_BIN:="$KOMPIRA_HOME/bin"}
: ${KOMPIRA_SSL_DIR:="$KOMPIRA_HOME/ssl"}
: ${KOMPIRA_PG_USER:=kompira}
: ${KOMPIRA_PG_DATABASE:=kompira}
: ${KOMPIRA_AMQP_USER:=kompira}
: ${KOMPIRA_AMQP_PASSWORD:=}
: ${KOMPIRA_REALM_NAME:=default}
: ${KOMPIRA_HA_CLIENT:=haclient}

#
# variables for extra package
#
: ${KOMPIRA_EXTRA_NAME:="kompira-extra-$SHORT_VERSION.$SYSTEM_NAME"}
: ${KOMPIRA_EXTRA_DIR:="$KOMPIRA_EXTRA_NAME"}
: ${KOMPIRA_EXTRA_REPO:="/etc/yum.repos.d/$KOMPIRA_EXTRA_NAME.repo"}
: ${KOMPIRA_EXTRA_BASE:="/opt/kompira/extra/$SHORT_VERSION/$SYSTEM_NAME"}
: ${KOMPIRA_EXTRA_PIP:="$KOMPIRA_EXTRA_BASE/pip"}
: ${KOMPIRA_EXTRA_RPM:="$KOMPIRA_EXTRA_BASE/packages"}
: ${KOMPIRA_EXTRA_WHL:="$KOMPIRA_EXTRA_BASE/wheelhouse"}

#
# variables for proxy settings
#
: ${PROXY_URL:="$http_proxy"}
: ${NO_PROXY:="${no_proxy:-localhost,127.0.0.1}"}
if id $KOMPIRA_USER > /dev/null 2>&1; then
    if [ "OK" == "$($SU - $KOMPIRA_USER -c "echo OK" 2>/dev/null)" ]; then
        PROXY_URL=$($SU - $KOMPIRA_USER -c "echo \$http_proxy")
        NO_PROXY=$($SU - $KOMPIRA_USER -c "echo \$no_proxy")
    fi
fi

#
# variables for postgres
#
PG_VERSION="$REQUIRES_POSTGRES"
if [ "$SYSTEM" == "AMZN" ]; then
    PG_PREFIX="postgresql"
    PG_SERVICE="postgresql"
    PG_DATADIR="/var/lib/pgsql/data"
    PG_SETUP="postgresql-setup"
else
    PG_PREFIX="postgresql${PG_VERSION/./}"
    PG_SERVICE="postgresql-${PG_VERSION}"
    PG_REPONAME="pgdg${PG_VERSION/./}"
    PG_REPOPKG0="pgdg-redhat"
    PG_REPOPKG="${PG_REPOPKG0}${PG_VERSION/./}"
    PG_DATADIR="/var/lib/pgsql/${PG_VERSION}/data"
    PG_SETUP="postgresql-${PG_VERSION/./}-setup"
fi
PG_BASEDIR=$(dirname $PG_DATADIR)
PG_LOG_DIR="/var/log/postgresql"
PG_REPL_USER="repl"
PG_REPL_PASS=$PG_REPL_USER
PGSQL_USER="postgres"
PGSQL_DB="postgres"
PGSQL_OPTIONS=""
DB_SECRET_KEYFILE="$KOMPIRA_VAR_DIR/.secret_key"

#
# variables for rabbitmq-server
#
RABBITMQ_CONFD_DIR="/etc/rabbitmq/conf.d"
RABBITMQ_USER="rabbitmq"
RABBITMQ_GROUP="rabbitmq"
RABBITMQ_LISTENER_TCP="127.0.0.1:5672"
RABBITMQ_LISTENER_SSL="0.0.0.0:5671"
RABBITMQ_SSL_VERIFY="verify_peer"
RABBITMQ_SSL_FAIL_IF_NO_PEER_CERT="false"
ERLANG_COOKIE="/var/lib/rabbitmq/.erlang.cookie"


#
# variables for memcached
#
MEMCACHED_USER="memcached"
MEMCACHED_GROUP="memcached"
MEMCACHED_SOCK_DIR="/var/run/memcached"

#
# variables for cluster
#
CLUSTER_CIB_FILE="/var/lib/pacemaker/cib/cib.xml"
CLUSTER_CONFIGURED=false
CLUSTER_RUNNING=false
CLUSTER_MASTER=false

#
# 冗長構成の対向ホスト名
#
HA_LOCALHOST=ha-kompira-local
HA_OTHERHOST=ha-kompira-other
: ${HA_LOCALNAME:=}
: ${HA_OTHERNAME:=}

#
# 冗長構成のリソース属性値
#
PGSQL_MASTER_SCORE=1001
PGSQL_SLAVE_SCORE=1000

: ${ECHO_LEVEL:=3}
ECHO_OPTIONS=
ECHO_PREFIX=
ECHO_POSTFIX=

# cp/install コマンドでのデフォルトバックアップ接尾辞
export SIMPLE_BACKUP_SUFFIX=.old

_now()
{
    date "+%F %T"
}

_echo()
{
    local msg
    for msg in "$@"; do
        echo $ECHO_OPTIONS "[$(_now)] ${ECHO_PREFIX}${msg}${ECHO_POSTFIX}"
    done
}

echo_debug()
{
    ECHO_PREFIX="DEBUG: " _echo "$@"
}
echo_verbose()
{
    ECHO_PREFIX="VERBOSE: " _echo "$@"
}
echo_info()
{
    ECHO_PREFIX="INFO: " _echo "$@"
}
echo_warn()
{
    ECHO_PREFIX="WARN: " _echo "$@"
}
echo_error()
{
    ECHO_PREFIX="ERROR: " _echo "$@"
}
echo_always()
{
    ECHO_PREFIX="****: " _echo "$@"
}
echo_param()
{
    echo_info "$(printf "    %-24s = %s" "$1" "$2")"
}
echo_title()
{
    echo_always "----------------------------------------------------------------" "$@" ""
}

verbose_run()
{
    echo_verbose "run: $*" >&2
    "$@"
    local rc=$?
    if [ "$rc" -ne 0 ]; then
        echo_verbose "status=$rc" >&2
    fi
    return $rc
}

#
# [BUG] templateの末尾に改行コードが無いと展開したファイルに__EOF__が付加されてしまう
#
expand_template()
{
    eval "$(echo "cat <<__EOF__"; cat $1; echo "__EOF__")"
}

diff_install()
{
    diff_and_cmd $INSTALL "$@"
}

diff_cp()
{
    diff_and_cmd cp -b "$@"
}

diff_and_cmd()
{
    local old=${!#}
    set ${@:1:$#-1}
    local new=${!#}
    set ${@:1:$#-1}
    if ! diff -N -u "$old" "$new"; then
        verbose_run "$@" "$new" "$old"
    fi
}

copy_new_conf_file()
{
    local temp_file=$1
    local conf_file=$2
    shift 2
    local install_opts=$@
    if [ -z "$install_opts" ]; then
        install_opts="-m 0664"
    fi
    if [ ! -f $conf_file ]; then
        # 設定ファイルが存在しない場合はそのままコピーする
        verbose_run $INSTALL $install_opts $temp_file $conf_file
    elif ! diff -q $conf_file $temp_file; then
        # 設定ファイルがカスタマイズされている場合は上書きせず .new ファイルとしてコピーする
        verbose_run $INSTALL $install_opts $temp_file $conf_file.new
        echo_info "Copied $conf_file.new (check the difference)"
        verbose_run diff -u $conf_file $conf_file.new
    fi
}

interrupt()
{
    echo_title "Abort ${SETUP_TYPE}."
    exit 1
}

inquire()
{
    echo -n "$1 "
    if [ -t 0 ]; then
        read answer
        case $answer in
            [yY]* ) answer="y";;
            [nN]* ) answer="n";;
            *) answer="$2" ;;
        esac
    else
        answer="$2"
        abort_setup "stdin is not the terminal!"
    fi
}

install_repo_direct()
{
    local repo_name=$1
    local repo_file=$2
    local repo_url=$3

    if [ ! -f /etc/yum.repos.d/$repo_file ]
    then
        echo_info "Install repository (direct): $repo_name"
        verbose_run yum-config-manager --add-repo=$repo_url
        exit_if_failed "$?" "Failed to install $repo_name"
    fi
}

install_repo_from_rpm()
{
    local repo_name=$1
    local repo_remove=$2
    local repo_url=$3

    if ! is_yum_installed $repo_name
    then
        if [ -n "$repo_remove" ]; then
            remove_if_installed $repo_remove
        fi
        echo_info "Install repository (rpm): $repo_name"
        local dir=$(dirname $repo_url)
        local pattern=$(basename $repo_url)
        echo_verbose "search $pattern in $dir"
        local url=$(find_link $dir $pattern | tail -1)
        if [ -z "$url" ]; then
            exit_if_failed 1 "$repo_name is not found"
        fi
        echo_info "install $url"
        verbose_run yum $YUM_OPTION -y install $url
        exit_if_failed "$?" "Failed to install $repo_name"
        return 0
    fi
    return 1
}

find_link()
{
    #
    # url で指定した HTML ページから pattern にマッチするリンク(href)を抽出する
    #
    local url=$1
    local pattern=$2
    curl -L -s "$url/" | sed -nre "s|.*href=\"($pattern)\".*|$url/\1|p"
}

is_runnable()
{
    test -x "$(which $1 2>/dev/null)"
}

is_yum_installed()
{
    local pkg
    local yum_option=$YUM_OPTION
    if $OFFLINE_MODE; then
        yum_option="$yum_option --noplugins --disablerepo=* --enablerepo=$KOMPIRA_EXTRA_NAME"
    fi
    for pkg; do
        if ! yum $yum_option list installed $pkg > /dev/null 2>&1
        then
            return 1
        fi
    done
}

exit_if_failed()
{
    local rc=$1
    shift
    if [ $rc -ne 0 ]; then
        abort_setup "$@"
    fi
}

yum_install()
{
    if [ -n "$*" ]; then
        local DESCRIPTION="${DESCRIPTION:-$@}"
        local yum_option=$YUM_OPTION
        echo_info "Install $DESCRIPTION"
        if $OFFLINE_MODE; then
            yum_option="$yum_option --noplugins --disablerepo=* --enablerepo=$KOMPIRA_EXTRA_NAME"
        fi
        verbose_run yum $yum_option -y install "$@"
        exit_if_failed "$?" "Failed to install $DESCRIPTION"
    fi
}

yum_install_if_not_installed()
{
    local DESCRIPTION="${DESCRIPTION:-$@}"
    if ! is_yum_installed $@; then
        yum_install $@
    fi
}

debuginfo_install()
{
    if [ -n "$*" ]; then
        local DESCRIPTION="${DESCRIPTION:-$@}"
        local yum_option=$YUM_OPTION
        echo_info "Debuginfo-install $DESCRIPTION"
        if $OFFLINE_MODE; then
            yum_option="$yum_option --noplugins --disablerepo=* --enablerepo=$KOMPIRA_EXTRA_NAME"
        fi
        #
        # 前の yum がロックを掴んでいるケースがあるため待機する
        #
        sleep 1  # 直後は yum.pid が生成されないため最初に少し待機する
        for i in $(seq 10); do
            if [ ! -f /var/run/yum.pid ]; then
                break
            fi
            echo_info "Waiting yum lock released ..."
            sleep 5
        done
        verbose_run debuginfo-install $yum_option -y "$@"
        exit_if_failed "$?" "Failed to debuginfo-install $DESCRIPTION"
    fi
}

remove_if_installed()
{
    local pkg
    for pkg; do
        if is_yum_installed $pkg; then
            echo_info "Remove ${pkg}"
            verbose_run yum $YUM_OPTION -y remove $pkg
        fi
    done
}

ver2num()
{
    echo $1 | awk -F. '{printf "%03d%03d%03d%03d\n",$1,$2,$3,$4}'
}

get_rpm_version()
{
    local name=$1
    rpm -q "$name" --info | sed -rne 's/^Version\s*:\s*(\S+).*/\1/p'
}

get_pip_info()
{
    local name=$1
    local field=$2
    $PIP show "$name" 2> /dev/null | sed -rne "s/^$field:\s*(.*)/\1/p"
}

get_kompira_version()
{
    get_pip_info "Kompira" "Version"
}

get_kompira_location()
{
    get_pip_info "Kompira" "Location"
}

get_object_version() {
    $KOMPIRA_BIN/manage.py shell <<EOF
from kompira.models.version import get_object_version
print("{0:04}".format(get_object_version() or 0))
EOF
}

set_object_version() {
    local current=$1
    $KOMPIRA_BIN/manage.py shell <<EOF
from kompira.models.version import set_object_version
set_object_version('$current')
EOF
}

pip_uninstall_if_installed()
{
    local pkg
    for pkg; do
        if $PIP show $pkg > /dev/null; then
            echo_info "Uninstall ${pkg} [$PIP]"
            verbose_run $PIP uninstall -y $pkg
        fi
    done
}

is_active_service()
{
    local svc=$1
    $SYSTEMCTL is-active $svc > /dev/null 2>&1
}

is_enabled_service()
{
    local svc=$1
    $SYSTEMCTL is-enabled $svc > /dev/null 2>&1
}

_service_status()
{
    local svc=$1
    verbose_run $SYSTEMCTL status $svc
}

_service_start()
{
    local svc=$1
    verbose_run $SYSTEMCTL start $svc
}

_service_stop()
{
    local svc=$1
    verbose_run $SYSTEMCTL stop $svc
}

_service_restart()
{
    local svc=$1
    verbose_run $SYSTEMCTL restart $svc
}

service_start()
{
    local svc=$1
    echo_info "Start service: ${svc}"
    _service_start $svc
    exit_if_failed "$?" "Failed to start ${svc}"
}

service_stop()
{
    local svc=$1
    if is_active_service $svc; then
        echo_info "Stop service: ${svc}"
        _service_stop $svc
        exit_if_failed "$?" "Failed to stop ${svc}"
    fi
}

service_restart()
{
    local svc=$1
    if is_active_service $svc; then
        echo_info "Restart service: ${svc}"
        _service_restart $svc
        exit_if_failed "$?" "Failed to restart ${svc}"
    else
        service_start $svc
    fi
}

service_register()
{
    local svc=$1
    verbose_run $SYSTEMCTL daemon-reload
}

service_enable()
{
    local svc=$1
    verbose_run $SYSTEMCTL enable $svc.service
}

service_disable()
{
    local svc=$1
    verbose_run $SYSTEMCTL disable $svc.service
}

check_root()
{
    if [ $(whoami) != root ]; then
        abort_setup "Please execute as root user."
    fi
}

check_arch()
{
    local arch=$(uname -i)
    case $arch in
        $REQUIRES_ARCH)
            echo_info "Confirmed architecture: $arch" ;;
        *)
            abort_setup "Please execute on the x86_64 Linux." ;;
    esac
}

check_system()
{
    if [ -z "$SYSTEM" ]; then
        abort_setup "CentOS/Red Hat 7.X or 8.X is required!"
    fi
    if [ ! "SYSTEMD" ]; then
        abort_setup "Systemd is not found!"
    fi
    echo_info "Confirmed system: $SYSTEM_RELEASE"
}

get_cluster_status()
{
    if [ ! -e $CLUSTER_CIB_FILE ]; then
        echo_info "Pacemaker is not configured."
        return 0
    fi
    CLUSTER_CONFIGURED=true
    PCS_VERSION=$(get_rpm_version pcs)
    if ! is_active_service "pacemaker"; then
        echo_info "Pacemaker is stop."
        return 0
    fi
    CLUSTER_RUNNING=true
    if pgsql_is_primary; then
        echo_info "Pacemaker is running (MASTER)"
        CLUSTER_MASTER=true
    else
        echo_info "Pacemaker is running (SLAVE)"
        CLUSTER_MASTER=false
    fi
}

check_subscription()
{
    local offline_mode=${1:-false}
    if $offline_mode || $RHUI_MODE; then
        return 0
    fi
    if [[ $SYSTEM == "RHEL" && -n "$SUBSCRIPTION_MANAGER" ]]; then
        echo_info "[RHEL] Check subscription status"
        if ! $SUBSCRIPTION_MANAGER status; then
            abort_setup "Please attach a valid subscription." \
                        "" \
                        "ex) subscription-manager register --auto-attach"
        fi
    fi
}

pgsql_cmddir()
{
    dirname $(readlink -f $(which psql))
}

pgsql_replica()
{
    local master_host="$1"

    verbose_run rm -f $PG_BASEDIR/tmp/PGSQL.lock
    verbose_run rm -rf $PG_DATADIR.old
    verbose_run mv -f $PG_DATADIR $PG_DATADIR.old

    # pg_baseback コマンドでデータベースをバックアップする
    # postgres ユーザで実行するため、ルートディレクトリに移動してから起動する
    (cd / && verbose_run sudo -u postgres pg_basebackup -h $master_host -U $PG_REPL_USER -D $PG_DATADIR -X stream --checkpoint=fast -P)
    local rc=$?
    if [ $rc -eq 0 ]; then
        # 成功した場合は $PG_DATADIR.old を削除する
        echo_info "Backup succeed: cleanup $PG_DATADIR.old"
        rm -rf $PG_DATADIR.old
    else
        # 失敗した場合は $PG_DATADIR.old を元に戻す
        echo_error "Backup FAILED!: restore $PG_DATADIR"
        rm -rf $PG_DATADIR
        mv -f $PG_DATADIR.old $PG_DATADIR
    fi
    return $rc
}

pgsql_has_kompira_table()
{
    # postgres が初期化されているか（kompira データベースにテーブルが存在するか）確認する
    LANG= psql -U kompira -Atc '\dt' kompira | grep -q "table"
}

pgsql_is_in_recovery()
{
    # postgres がリカバリモードか確認する
    psql -U $PGSQL_USER -Atc "select pg_is_in_recovery()" 2>/dev/null
}

pgsql_is_primary()
{
    local pg_is_in_recovery rc
    pg_is_in_recovery=$(pgsql_is_in_recovery)
    rc=$?
    if [ $rc -ne 0 ]; then
        echo_warn "PostgreSQL is stop (rc=$rc)"
        return 2
    fi
    case $pg_is_in_recovery in
        f)
            echo_info "PostgreSQL is running as a primary."
            return 0
            ;;
        t)
            echo_info "PostgreSQL is running as a hot standby."
            return 1
            ;;
        *)
            abort_setup "Invalid result: pg_is_in_recovery=$pg_is_in_recovery"
            ;;
    esac
}

setup_firewalld()
{
    echo_title "Configure firewalld settings."
    local rule rule_elem rule_spec prot port
    for rule; do
        case $rule in
            +([0-9])/@(tcp|udp))
                verbose_run firewall-cmd --add-port=$rule --permanent
                ;;
            +([0-9]|\.)?(/+([0-9])))
                verbose_run firewall-cmd --zone=trusted --add-source=$rule --permanent
                ;;
            *)
                verbose_run firewall-cmd --add-service=$rule --permanent
                ;;
        esac
    done
    verbose_run firewall-cmd --reload
}

setup_iptables()
{
    echo_title "Configure iptables settings."
    local rule rule_elem rule_spec prot port
    iptables-save > $TMPDIR/iptables_cur
    for rule; do
        rule_spec=""
        for rule_elem in ${rule/,/ }; do
            case $rule_elem in
                +([0-9])/@(tcp|udp))
                    prot=${rule_elem#*/}
                    port=${rule_elem%/*}
                    rule_spec="$rule_spec -p $prot -m $prot --dport $port"
                    ;;
                +([0-9]|\.)?(/+([0-9])))
                    rule_spec="$rule_spec -s $rule_elem"
                    ;;
                *)
                    echo_warn "invalid rule: $rule_elem"
                    ;;
             esac
        done
        rule_spec=${rule_spec# }
        if [ -z "$rule_spec" ]; then
            continue
        fi
        rule_spec="INPUT $rule_spec -j ACCEPT"
        if grep -q -e "^-A $rule_spec" $TMPDIR/iptables_cur; then
            echo_info "A rule '$rule_spec' is already set."
        else
            echo_info "Append a rule '$rule_spec' to iptables."
            verbose_run iptables -I $rule_spec
        fi
    done
    iptables-save > $TMPDIR/iptables_new
    diff_cp $TMPDIR/iptables_new /etc/sysconfig/iptables
}

patch_resource_agents()
{
    local ra_ver=$(get_rpm_version resource-agents)
    if [ -z "$ra_ver" ]; then return 0; fi
    echo_info "Patch resource-agents $ra_ver"
    #
    # apache-conf.sh の source_envfiles で読み取った変数を
    # httpd に環境変数として渡すために export するようにパッチをあてる
    #
    if patch --dry-run -f -s -d/ -p1 -i $THIS_DIR/patches/apache-conf.sh.patch > /dev/null; then
        verbose_run patch -b -f -d/ -p1 -i $THIS_DIR/patches/apache-conf.sh.patch
    fi
    #
    # monitorの性能改善のためのパッチ(余分なrabbitmqctl呼び出しを削除)
    # users, permissions 情報のバックアップ・リストア処理改善のためのパッチ
    #
    for patch in $THIS_DIR/patches/rabbitmq-cluster*.patch; do
        if patch --dry-run -f -s -d/ -p1 -i $patch > /dev/null; then
            verbose_run patch -b -f -d/ -p1 -i $patch
        fi
    done
}

setup_ha_user()
{
    #
    # kompirad から pcs コマンドを操作できるように haclient グループに追加する
    #
    verbose_run usermod -a -G $KOMPIRA_HA_CLIENT $KOMPIRA_USER
}

cluster_wait_current_dc()
{
    local timeout=60
    ECHO_OPTIONS="-n" echo_info "Waiting Current DC"
    sleep 3
    while [ $timeout -gt 0 ]; do
        let timeout=$timeout-1
        if crm_mon -1 | grep "Current DC: NONE" > /dev/null; then
            echo -n "."
            sleep 1
            continue
        fi
        echo
        return 0
    done
    echo
    return 1
}

pcs_enter_maintenance_mode()
{
    echo_info "Enter the pacemaker in maintenance mode."
    verbose_run pcs property set maintenance-mode=true
}

pcs_leave_maintenance_mode()
{
    echo_info "Exit the pacemaker from maintenance mode."
    verbose_run pcs property set maintenance-mode=false
}

pcs_remove_resources()
{
    local pcs_opt=$@
    #
    # 既存のリソースを削除する
    #
    local resource_list
    local res
    pcs_remove_constraints $pcs_opt
    for group in $(pcs $pcs_opt resource show --full | grep 'Group:' | sed -re 's/.*: (\w+)/\1/'); do
        verbose_run pcs $pcs_opt resource delete $group
    done
    for res in $(pcs $pcs_opt resource show --full | grep 'Resource:' | sed -re 's/.*: (\w+).*/\1/'); do
        verbose_run pcs $pcs_opt resource delete $res
    done
}

pcs_remove_constraints()
{
    local pcs_opt=$@
    #
    # 既存の制約条件を削除する
    #
    local constraint
    for constraint in $(pcs $pcs_opt constraint show --full | grep 'id:' | sed -re 's/.*id:(.*)\)\s*$/\1/'); do
        verbose_run pcs $pcs_opt constraint remove $constraint
    done
}

pcs_setup_constraints()
{
    local pcs_opt=$@
    local res_name_pgsql
    if [ $(ver2num $PCS_VERSION) -lt $(ver2num "0.10.0") ]; then
        res_name_pgsql=ms_pgsql
    else
        res_name_pgsql=res_pgsql-clone
    fi
    #
    # *** 順序制約 ***
    # - pgsql が promote してから webserver を起動する
    #   (kompirad が早く起動して master になっていない pgsql に接続しようとするのを防ぐ)
    # - rabbitmqがstarted状態になってから webserverを起動する
    #
    verbose_run pcs $pcs_opt constraint order promote $res_name_pgsql then start webserver
    verbose_run pcs $pcs_opt constraint order set res_rabbitmq-clone role=Started set webserver
    #
    # *** 場所制約 ***
    # - webserver は pgsqlのマスタノードで実行可能
    # - pgsql マスタはrabbitmq が起動しているノードで実行可能
    #
    verbose_run pcs $pcs_opt constraint colocation add webserver with Master $res_name_pgsql
    verbose_run pcs $pcs_opt constraint colocation add Master $res_name_pgsql with res_rabbitmq-clone
}

pcs_set_property()
{
    # プロパティを16進ダンプした文字列で格納する（property の値には '=' を使用できないなど制約があるため）
    local key=$1
    local val=$(echo -n "$2" | $KOMPIRA_BIN/python -c "import sys;print(sys.stdin.buffer.read().hex())")
    shift 2
    local pcs_opt=$@
    verbose_run pcs property set $key=$val --force $pcs_opt
}

pcs_get_property()
{
    # プロパティ値を取得してデコードした結果を返す
    local key=$1
    local val=$(pcs property | grep $key:)
    echo -n ${val#*:} | $KOMPIRA_BIN/python -c "import sys;print(bytes.fromhex(sys.stdin.read()).decode())"
}

pcs_failcount_show()
{
    local res
    for res; do
        # [v1.5.0] pcs コマンドでは適切に failcount を扱えないので crm_failcount を利用する
        # pcs resource failcount show $res
        crm_failcount -r $res -G
    done
}

pcs_failcount_reset()
{
    local res
    for res; do
        # [v1.5.0] pcs コマンドでは適切に failcount を扱えないので crm_failcount を利用する
        # pcs resource failcount reset $res
        verbose_run crm_failcount -r $res -D
    done
}

pcs_show_status()
{
    echo_info "Display failcount for each resources."
    pcs_failcount_show res_vip res_httpd res_kompirad res_kompira_jobmngrd res_memcached res_pgsql res_rabbitmq
    echo_info "Display constraint setings of resources."
    pcs constraint show
    echo_info "Display state of resources."
    if [ $RHEL_VERSION == 8 ]; then
        pcs resource status
    else
        pcs resource show
    fi
}

check_localname()
{
    if [ -z $HA_LOCALNAME ]; then
        HA_LOCALNAME=$(crm_node -n)
        if [ -z $HA_LOCALNAME ]; then
            abort_setup "Name of local node could not be determined."
        fi
    fi
}

check_othername()
{
    if [ -z $HA_OTHERNAME ]; then
        HA_OTHERNAME=$(crm_node -l | cut -d' ' -f2 | grep -v -w $(crm_node -n) | head -n 1)
        if [ -z $HA_OTHERNAME ]; then
            abort_setup "Name of other node could not be determined."
        fi
    fi
}

get_rmq_node()
{
    local node_name=$1
    if [ -z $node_name ]; then
        check_localname
        node_name=$HA_LOCALNAME
    fi
    crm_attribute -l reboot -N "$node_name" -n rmq-node-attr-res_rabbitmq -G -q 2>/dev/null
}

get_pgsql_score()
{
    local node_name=$1
    if [ -z $node_name ]; then
        check_localname
        node_name=$HA_LOCALNAME
    fi
    crm_attribute -l forever -N "$node_name" -n master-res_pgsql -G -q 2>/dev/null
}

sync_secret_keyfile()
{
    #
    # pgsql の シークレットキーファイルを同期する
    #
    echo_info "Syncronize PostgreSQL secret key file."
    local secret_key=$(pcs_get_property pgsql-secret-key)
    if [ -z $secret_key ]; then
        # 1.6.5 以前のバージョンの場合はプロパティがセットされていないため、ここでセットする
        pcs_set_property pgsql-secret-key $(cat $DB_SECRET_KEYFILE)
    elif [ "$secret_key" != "$(cat $DB_SECRET_KEYFILE)" ]; then
        cp -f $DB_SECRET_KEYFILE ${DB_SECRET_KEYFILE}.bak
        echo -n $secret_key > $DB_SECRET_KEYFILE
    fi
}

#
# クラスタ構成が正常状態になるまで待つ
# ---
#   正常状態とは各ノードの属性値が以下の状態となることを指す
#   - スレーブノード:master-res_pgsql: 1000
#   - マスタノード:master-res_pgsql: 1001
#   - 各ノード: rmq-node-attr-res_rabbitmq: rabbit@<ノード名>
#
wait_resources_stabilize()
{
    check_localname
    check_othername
    get_cluster_status

    local timeout=60
    local pgsql_slave_score pgsql_master_score
    local pgsql_slave_node pgsql_master_node
    local rmq_local_node rmq_other_node
    local header="    PostgreSQL   | RabbitMQ"
    local format="    %5s, %5s | %20s, %20s"

    if $CLUSTER_MASTER; then
        pgsql_master_node=$HA_LOCALNAME
        pgsql_slave_node=$HA_OTHERNAME
    else
        pgsql_master_node=$HA_OTHERNAME
        pgsql_slave_node=$HA_LOCALNAME
    fi

    echo_info "Waiting for the resources to stabilize."
    echo "$header"
    while [ $timeout -gt 0 ]; do
        let timeout=$timeout-1
        #
        # リソースの状態を取得する
        #
        pgsql_slave_score=$(get_pgsql_score $pgsql_slave_node)
        if [ -z $pgsql_slave_score ]; then
            pgsql_slave_score="#NA"
        fi
        pgsql_master_score=$(get_pgsql_score $pgsql_master_node)
        if [ -z $pgsql_master_score ]; then
            pgsql_master_score="#NA"
        fi
        rmq_local_node=$(get_rmq_node $HA_LOCALNAME)
        if [ -z $rmq_local_node ]; then
            rmq_local_node="#NA"
        fi
        rmq_other_node=$(get_rmq_node $HA_OTHERNAME)
        if [ -z $rmq_other_node ]; then
            rmq_other_node="#NA"
        fi
        #
        # 状態を表示する
        #
        printf "$format\n" "$pgsql_slave_score" "$pgsql_master_score" "$rmq_local_node" "$rmq_other_node"
        #
        # 対象リソースが期待する状態に遷移した終了する
        #
        if [ "$pgsql_slave_score" == "$PGSQL_SLAVE_SCORE" -a \
             "$pgsql_master_score" == "$PGSQL_MASTER_SCORE" -a \
             "$rmq_local_node" == "rabbit@$HA_LOCALNAME" -a \
             "$rmq_other_node" == "rabbit@$HA_OTHERNAME" ]; then
            echo_info "Resources stabilized."
            return 0
        fi
        sleep 1
    done
    return 1
}

sync_corosync()
{
    # corosync の設定を対向ノードに同期する
    local othername="$1"
    local tmp_corosync="/tmp/corosync.conf.$$"
    verbose_run pcs cluster corosync $othername > $tmp_corosync
    exit_if_failed "$?" "Failed to sync corosync.conf"
    diff_cp $tmp_corosync /etc/corosync/corosync.conf
    verbose_run pcs cluster reload corosync
    rm -f $tmp_corosync
}

normalize_proxy_url()
{
    local url="$1"
    case "$url" in
        "" | http*://) url="";;
        http*://*) ;;
        *) url="http://$url" ;;
    esac
    echo $url
}

urlparse()
{
    local URL="$1"
    local URLPARSE_PREFIX="${URLPARSE_PREFIX:-URLPARSE_}"
    local URLPARSE_KEYS="${URLPARSE_KEYS:-scheme,hostname,port,username,password}"
    $PYTHON -c "from urlparse import urlparse; url=urlparse('$URL'); print('\n'.join(['${URLPARSE_PREFIX}%s=%s' % (k.upper(), getattr(url, k) or '') for k in '$URLPARSE_KEYS'.split(',')]))"
}

show_options()
{
    for opt in $@; do
        echo_param "$opt" "${!opt}"
    done
}

create_tmpdir()
{
    TMPDIR=$(mktemp -d --tmpdir=$(pwd) "$TMPDIR_TEMPLATE")
}

start_setup()
{
    echo_always \
        "****************************************************************" \
        "Kompira-$VERSION:" \
        "Start: ${SETUP_TYPE}" \
        ""
    show_options $SHOW_OPTIONS
}

exit_setup()
{
    local rc=${1:-0}
    echo_always \
        "" \
        "Finish: ${SETUP_TYPE} (status=$rc)" \
        "****************************************************************"
    sleep 1
    exit $rc
}

abort_setup()
{
    echo_error "" "$@" ""
    exit_setup 1
}
