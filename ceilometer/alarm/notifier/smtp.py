# -*- encoding: utf-8 -*-

import smtplib
import eventlet
from oslo.config import cfg
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ceilometer.alarm import notifier
from ceilometer.openstack.common import log

LOG = log.getLogger(__name__)

EMAIL_NOTIFIER_OPTS = [
    cfg.StrOpt('email_notifier_host',
               default='smtp.qq.com',
               help='email_notifier_host'
               ),
    cfg.StrOpt('email_notifier_host_user',
               default='179312371@qq.com',
               help='email_notifier_host_user'
               ),
    cfg.StrOpt('email_notifier_host_password',
               default='wxwl1986',
               help='email_notifier_host_password'
               ),
    cfg.IntOpt('email_notifier_port',
               default=25,
               help='email_notifier_port'
               ),
    cfg.BoolOpt('email_notifier_use_tls',
                default=False,
                help='email_notifier_use_tls'
                ),
    cfg.StrOpt('email_notifier_server_email',
               default='',
               help='email_notifier_server_email'
               ),
    cfg.StrOpt('email_notifier_subject',
               default=u'网宿云告警服务',
               help='email_notifier_subject'
               ),
]
cfg.CONF.register_opts(EMAIL_NOTIFIER_OPTS, group="alarm")


class SMTPAlarmNotifier(notifier.AlarmNotifier):
    """mail alarm notifier."""

    @staticmethod
    def notify(action, alarm_id, previous, current, reason, reason_data):
        LOG.info("Notifying alarm %s from %s to %s with action %s because %s",
                 alarm_id, previous, current, action, reason)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '%s %s' % (reason, date)          
        LOG.debug("mail_message:%s" % message)
        subject = '%s' % cfg.CONF.alarm.email_notifier_subject
        send_mail(subject, message, action.netloc)


def send_mail(subject, message, recipient_list):
    '''发送邮件
    param subject: 邮件标题
    param message: 邮件正文
    param recipient_list: 邮件收件人列表
    ''' 
    try:     
        if cfg.CONF.alarm.email_notifier_use_tls:
            smtp = smtplib.SMTP_SSL()
        else:
            smtp = smtplib.SMTP()
        from_user = cfg.CONF.alarm.email_notifier_host_user
        smtp.connect(cfg.CONF.alarm.email_notifier_host,
                     cfg.CONF.alarm.email_notifier_port)
        smtp.ehlo()
        smtp.login(from_user,
                   cfg.CONF.alarm.email_notifier_host_password)
        msg = MIMEMultipart()
        msg.attach(MIMEText(message, _subtype="html", _charset="utf-8"))
        msg['Subject'] = subject
        msg['From'] = from_user
        msg['To'] = recipient_list
        smtp.sendmail(from_user,
                      [recipient_list],
                      msg.as_string())
    except Exception, e:
        LOG.error(e)
        raise e
    finally:
        smtp.close()
