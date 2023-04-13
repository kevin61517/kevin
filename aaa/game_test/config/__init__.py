"""
遊戲配置
"""

from .A import *
from .B import *



@signals.user_phone_confirmed.connect
def on_user_phone_confirmed(sender, user, first=False, delay_time=0, **kwargs):
    from spinach.workers import user_event
    from spinach.workers.job import activity_user_info_confirmed
    event = 'user_phone_confirmed'
    if delay_time:
        user_event.apply_async((user.id, event), first=first, countdown=delay_time, **kwargs)
    else:
        user_event.delay(user_id=user.id, event=event, first=first, **kwargs)
    if TENANT_ID == 'wcg' and first and user.ident_confirmed:
        activity_user_info_confirmed.delay(user_id=user.id, title='会员完善信息活动')
    if UNIVERSAL_AGENT_ON and first and user.u_plat == 15 and not user.is_universal_agent and user.referrer_name \
            and user.card_confirmed and get_deposit_paid_count(user) > 0:
        activity_user_info_confirmed.delay(user_id=user.id, title='交个朋友官方让利活动-被邀請人')
    if TELEMARKETING_WORKER_ENABLE and user.phone and len(user.phone) > 0:
        from spinach.workers.user import on_telemarketing_invited_to_be_platform_member
        on_telemarketing_invited_to_be_platform_member.delay(
            phone_number=user.phone,
            register_at=user.register_at,
            platform_username=user.username,
        )
    if TENANT_ID == 'test' and first:
        activity_user_info_confirmed.delay(user_id=user.id, title='完善信息-绑定手机号')


@signals.user_card_confirmed.connect
def on_user_card_confirmed(sender, user, first=False, card=None, **kwargs):
    from spinach.workers import user_event
    from spinach.workers.job import activity_user_info_confirmed
    event = 'user_card_confirmed'
    card_id = None
    if card:
        card_id = card.id
    user_event.delay(user_id=user.id, event=event, first=first, card_id=card_id, **kwargs)
    if UNIVERSAL_AGENT_ON and first and user.u_plat == 15 and not user.is_universal_agent and user.referrer_name \
            and user.phone_confirmed and get_deposit_paid_count(user) > 0:
        activity_user_info_confirmed.delay(user_id=user.id, title='交个朋友官方让利活动-被邀請人')
    if TENANT_ID == 'test' and card:
        if card.open_bank == 'USDTCARD':
            activity_user_info_confirmed.delay(user_id=user.id, title='绑定虚拟币地址')
        else:
            activity_user_info_confirmed.delay(user_id=user.id, title='完善信息-绑定银行卡')


@signals.withdrawal_succeeded.connect
def on_withdrawal_settled(sender, withdrawal, **kws):
    from spinach.workers.job import activity_user_info_confirmed
    from spinach.services import withdrawals
    user = withdrawal.user
    start = user.register_at
    end = datetime.utcnow()
    check_withdrawal = withdrawals.search({'created_ge': start, 'created_lt': end, 'user': withdrawal.user,
                                           'succeeded': True}).count()
    if TENANT_ID == 'test' and check_withdrawal == 1:
        activity_user_info_confirmed.delay(user_id=withdrawal.user_id, title='完善信息-首次提现')


def on_recharge_settled(recharge, **kwargs):
    """
    充值成功到账后的活动任务处理
    1.充值是否附帶活動
     - 有活動、狀態不是完成、金額大於100的：
     - 有活動、狀態不是完成、標題為首充、金額大於50
    """
    user = recharge.user

    # 存款创建首冲活动关联
    if recharge.has_job:  # 关联了充值活动，如果充值成功， 活动标志位成功，计算需要发放的流水
        user_job = recharge.user_job
        if user_job and user_job.status != 'finished' and recharge.amount_paid >= 100:
            user_jobs.on_done(user_job=user_job, obj=recharge)
        elif user_job and user_job.status != 'finished' and user_job.title == '首次充值赠送本金的50%' \
                and recharge.amount_paid >= 50:
            user_jobs.on_done(user_job=user_job, obj=recharge)

    # 存款活动
    for user_job in user_jobs.my_jobs(user=user, type='recharge'):
        user_jobs.update_recharge(user_job=user_job, recharge=recharge)

    # 首次充值成功，自动发放的活动
    if recharge.first:
        from spinach.workers.job import activity_user_info_confirmed
        if user.u_plat == 15 and not user.is_universal_agent and user.referrer_name \
                and user.card_confirmed and user.phone_confirmed:
            activity_user_info_confirmed.delay(user_id=user.id, title='交个朋友官方让利活动-被邀請人')
        if TENANT_ID == 'test':
            activity_user_info_confirmed.delay(user_id=user.id, title='首次充值')

    # 交个朋友-存款大福利
    if user.u_plat == 15 and user.referrer and not user.extra.get('invitee_deposit_job_ts') and get_total_deposit(
            user) >= 500:
        user.extra = dict(user.extra,
                          invitee_deposit_job_ts=int(recharge.time_paid.replace(tzinfo=pytz.UTC).timestamp()))
        users.update(user)