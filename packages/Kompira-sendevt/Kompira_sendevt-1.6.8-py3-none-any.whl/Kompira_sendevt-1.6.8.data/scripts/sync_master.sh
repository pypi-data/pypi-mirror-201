#!/bin/bash
#
# Copyright (c) 2012-2014 Fixpoint Inc. All rights reserved.
# ---
# マスターDBからスナップショットを取得し、同期処理を行う
#
shopt -s extglob
THIS_DIR=$(dirname $(readlink -f $0))
SETUP_TYPE="Sync with the Master"

. $THIS_DIR/setup_utils.sh

sync_pgsql=false

usage_exit()
{
    cat <<EOF
Usage: `basename $0` [<master-name>]

  --help                Show this message.

EOF
    exit 1
}

parse_options()
{
    OPTIONS=`getopt -q -o '' -l help -- "$@"`
    [ $? != 0 ] && usage_exit

    local slave_mode
    eval set -- "$OPTIONS"
    while true
    do
        arg="$1"
        case "$arg" in
            --) shift; break ;; # 引数は無視
            *) usage_exit ;;
        esac
        shift
    done

    if [ -n "$1" ]; then
        HA_OTHERHOST="$1"
    fi
}

check_standby()
{
    #
    # スタンバイモードの確認
    #
    if [ "$(crm_standby -qG)" == "on" ]; then
        abort_setup "This node is currently in standby mode. Please execute 'pcs cluster unstandby' and try again."
    fi
}

check_nodename()
{
    #
    # ノード名の確認
    #
    check_localname
    check_othername
    echo_info "HA_LOCALNAME=$HA_LOCALNAME"
    echo_info "HA_OTHERNAME=$HA_OTHERNAME"
}

check_pacemaker()
{
    check_standby
    check_nodename
}

start_pacemaker()
{
    echo_title "Start pacemaker service."
    #
    # pacemaker 制御下でなく起動している pgsql/rabbitmq は停止させておく
    #
    if is_active_service $POSTGRES; then
        echo_warn "Stop $POSTGRES not under pacemaker control."
        service_stop $POSTGRES
    fi
    if is_active_service rabbitmq-server; then
        echo_warn "Stop rabbitmq-server not under pacemaker control."
        killall -q beam beam.smp
        service_stop rabbitmq-server
    fi
    #
    # pacemaker を起動する
    #
    service_start pacemaker
    exit_if_failed "$?" "Failed to start pacemaker."
    cluster_wait_current_dc
    exit_if_failed "$?" "The state of pacemaker did not stabilize."
    echo_info "Pacemaker has stablized."
    check_pacemaker
    sync_corosync $HA_OTHERNAME
    #
    # リソースの状態が安定するのを待つ
    #
    wait_resources_stabilize
}

check_cluster()
{
    echo_title "Check cluster status."
    get_cluster_status
    if ! $CLUSTER_CONFIGURED; then
        abort_setup "Cluster configuration is not setup."
    fi
    if ! $CLUSTER_RUNNING; then
        # pacemaker が起動していないときは起動させる
        start_pacemaker
    else
        check_pacemaker
    fi
}

check_pgsql()
{
    #
    # マスターノードでは sync_master しない
    #
    if pgsql_is_primary; then
        echo_warn "PostgreSQL on this node is running as a Master."
        return
    fi
    #
    # pacemaker が管理している postgres の状態をチェックする
    # pgsql_score が 1000 のときは
    # 同期状態でレプリケーション中とみなす（sync_master 不要）
    #
    local pgsql_score=$(get_pgsql_score)
    if [[ $pgsql_score == $PGSQL_SLAVE_SCORE ]]; then
        # TODO: --force オプションで強制的に sync_master させる
        echo_info "PostgreSQL on this node is running as a Slave."
        return
    fi
    echo_info "PostgreSQL on this node needs to be synchronized with the Master."
    sync_pgsql=true
}

sync_pgsql()
{
    #
    # pgsql の復旧
    #
    if $sync_pgsql; then
        #
        # postgres を停止させる
        #
        verbose_run pcs resource debug-stop res_pgsql
        #
        # データベースのバックアップを実行する
        #
        if ! pgsql_replica $HA_OTHERHOST; then
            echo_error "Failed to backup the database."
            return 1
        fi
        #
        # postgre を再開
        #
        verbose_run pcs resource debug-start res_pgsql
    fi
    return 0
}

sync_master()
{
    local rc_pgsql
    local rc=0
    check_cluster
    check_pgsql
    #
    # メンテナンスモードに移行する
    #
    pcs_enter_maintenance_mode
    exit_if_failed "$?" "Failed to enter maintenance mode."
    #
    # pgsql を同期させる
    #
    if $sync_pgsql; then
        sync_pgsql
        rc_pgsql=$?
        if [ $rc_pgsql == 0 ]; then
            echo_info "Reset the failcount of PostgreSQL"
            pcs_failcount_reset res_pgsql
        else
            rc=1
        fi
    fi
    if [ $rc == 0 ]; then
        pcs_failcount_reset res_vip res_httpd res_kompirad res_kompira_jobmngrd res_memcached res_rabbitmq
    fi
    #
    # メンテナンスモードを解除する
    #
    pcs_leave_maintenance_mode
    #
    # 同期の成否をチェックする
    #
    exit_if_failed "$rc" "Failed to sync with $HA_OTHERHOST."
}

remove_startup()
{
    #
    # sync_master 完了後の kompirad 起動時は DB マイグレーション不要
    # になるため、$KOMPIRA_VAR_DIR/startup/do* ファイルを削除しておく
    # パッケージ情報はノードごとに収集するので do_update_packages_info は消さない
    #
    rm -f $KOMPIRA_VAR_DIR/startup/{do_migrate,do_import_data}
}

################################################################

if ! is_yum_installed "pacemaker"; then
    echo_error "Cluster configuration is not setup."
    exit 1
fi
parse_options "$@"
start_setup
sync_master
wait_resources_stabilize
exit_if_failed $? "Resources did not stabilize."
sync_secret_keyfile
remove_startup
pcs_show_status
exit_setup 0
