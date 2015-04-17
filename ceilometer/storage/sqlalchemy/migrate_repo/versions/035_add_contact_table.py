# -*- encoding: utf-8 -*-
#
# Copyright © 2013 eNovance <licensing@enovance.com>
# Copyright © 2013 Red Hat, Inc.
#
# Author: Mehdi Abaakouk <mehdi.abaakouk@enovance.com>
#         Angus Salkeld <asalkeld@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from sqlalchemy import MetaData, Table, Column, Text
from sqlalchemy import Boolean, Integer, String, DateTime


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    contact = Table(
        'contact', meta,
        Column('contact_id', String(255), primary_key=True, index=True),
        Column('contact_name', String(64)),
        Column('contact_email', String(64), index=True),
        Column('contact_phone', String(64)),
        Column('timestamp', DateTime(timezone=False)),
        Column('user_id', String(255), index=True),
        Column('project_id', String(255), index=True),
        Column('state', String(32)),
        Column('state_timestamp', DateTime(timezone=False)),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    contact.create()


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    contact = Table('contact', meta, autoload=True)
    contact.drop()
