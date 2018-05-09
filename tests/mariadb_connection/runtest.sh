#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of mariadb_connection
#   Description: Tries to connect to MariaDB via unixODBC package
#   Author: Michal Schorm <mschorm@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2018 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/bin/rhts-environment.sh || exit 1
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="mariadb-connector-odbc"

rlJournalStart
    rlPhaseStartSetup
        # Check if all needed packages are installed
        rlAssertRpm $PACKAGE
        rlAssertRpm unixODBC
        rlAssertRpm mariadb
        rlAssertRpm mariadb-server
        # check unix ODBC configuration
        rlAssertExists "/etc/odbcinst.ini"
        rlAssertGrep "MariaDB" "/etc/odbcinst.ini"

        rlRun "cp -f odbc.ini /etc/"
        rlAssertExists "/etc/odbc.ini"
        rlAssertGrep "MariaDB" "/etc/odbc.ini"

        # Start MariaDB
        rlRun "systemctl start mariadb" 0
    rlPhaseEnd

    rlPhaseStartTest
        rlRun " echo 'show databases' | isql -v mariadb-connector-odbc -b > /tmp/test_query_output" 0
        rlAssertGrep "Database" "/tmp/test_query_output"
        rlAssertGrep "information_schema" "/tmp/test_query_output"
        rlAssertGrep "mysql" "/tmp/test_query_output"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun " echo 'create database ci_test_database' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'show databases' | isql -v mariadb-connector-odbc -b > /tmp/test_query_output" 0
        rlAssertGrep "ci_test_database" "/tmp/test_query_output"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun " echo 'create table ci_test_database.ci_test_table (root int, pow int)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'insert into ci_test_database.ci_test_table values (0, 1)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'insert into ci_test_database.ci_test_table values (1, 1)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'insert into ci_test_database.ci_test_table values (2, 4)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'insert into ci_test_database.ci_test_table values (3, 9)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'insert into ci_test_database.ci_test_table values (4, 16)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'insert into ci_test_database.ci_test_table values (5, 25)' | isql -v mariadb-connector-odbc -b " 0
        rlRun " echo 'select * from ci_test_database.ci_test_table where root>2' | isql -v mariadb-connector-odbc -b > /tmp/test_query_output" 0
        rlAssertNotGrep "0" "/tmp/test_query_output"
        rlAssertGrep "9" "/tmp/test_query_output"
        rlAssertGrep "16" "/tmp/test_query_output"
        rlAssertGrep "25" "/tmp/test_query_output"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun " echo 'drop database ci_test_database' | isql -v mariadb-connector-odbc -b " 0
        rlRun " rm -f /tmp/test_query_output" 0
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
