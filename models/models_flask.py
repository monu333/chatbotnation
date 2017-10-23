from flask_sqlalchemy import SQLAlchemy
from  models.database import db



class User(db.Model):
    __tablename__ = 'user'

    usr_id = db.Column(db.db.Integer, primary_key=True)
    usr_name = db.Column(db.db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email_id = db.Column(db.String(320))
    phone_num = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, server_default=db.db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)
    conference_num = db.Column(db.Integer)
    skype = db.Column(db.String(255))
    google_hangout = db.Column(db.String(255))
    go_to_meeting = db.Column(db.String(255))
    join_me = db.Column(db.String(255))
    web_ex = db.Column(db.String(255))
    video_conf = db.Column(db.String(255))



class UserChatRsp(db.Model):
    __tablename__ = 'user_chat_rsp'

    usr_chat_rsp_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.db.ForeignKey('user.usr_id'), index=True)
    usr_input = db.Column(db.String(255), nullable=False)
    usr_output = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    usr = db.db.relationship('User')


class UserClnMap(db.Model):
    __tablename__ = 'user_cln_map'

    usr_cln_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    client_name = db.Column(db.String(255))
    cln_Email_ID = db.Column(db.String(320))
    cln_str = db.Column(db.Integer)
    active_flag = db.Column(db.String(1))
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)

    usr = db.relationship('User')


class UserFrndList(db.Model):
    __tablename__ = 'user_frnd_list'

    usr_frnd_list_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    frnd_usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)
    active_flag = db.Column(db.Integer)

    frnd_usr = db.relationship('User', primaryjoin='UserFrndList.frnd_usr_id == User.usr_id')
    usr = db.relationship('User', primaryjoin='UserFrndList.usr_id == User.usr_id')


class UserGst(db.Model):
    __tablename__ = 'user_gst'

    usr_gst_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    email_id = db.Column(db.String(255))
    active_flag = db.Column(db.Integer)
    usr_sync = db.Column(db.Integer)
    email_sync = db.Column(db.Integer)

    usr = db.relationship('User')


class UserPref(db.Model):
    __tablename__ = 'user_pref'

    usr_pref_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    pref_day = db.Column(db.Integer)
    pref_start_time = db.Column(Time)
    pref_end_time = db.Column(Time)
    max_time = db.Column(db.Integer)
    time_zone = db.Column(db.String(255))
    active_flag = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)
    pref_usr_cln_id = db.Column(db.Integer)

    usr = db.relationship('User')


class UserSch(db.Model):
    __tablename__ = 'user_sch'

    usr_sch_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    sch_date = db.Column(db.Date)
    sch_start_time = db.Column(db.Time)
    sch_duration = db.Column(db.Integer)
    application = db.Column(db.String(255))
    location = db.Column(db.String(255))
    active_flag = db.Column(db.Integer)
    usr_cln_id = db.Column(db.ForeignKey('user_cln_map.usr_cln_id'), index=True)
    usr_prin_part_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)
    usr_sync = db.Column(db.Integer)
    prim_part_sync = db.Column(db.Integer)

    usr_cln = db.relationship('UserClnMap')
    usr = db.relationship('User')


class UserTeam(db.Model):
    __tablename__ = 'user_team'

    team_id = db.Column(db.Integer, primary_key=True)
    leader_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    team_name = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)
    active_flag = db.Column(db.Integer)

    leader = db.relationship('User')


class UserTeamMap(db.Model):
    __tablename__ = 'user_team_map'

    team_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    usr_email_id = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)
    active_flag = db.Column(db.Integer)

    usr = db.relationship('User')


class UserVipList(db.Model):
    __tablename__ = 'user_vip_list'

    usr_vip_list_id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    vip_id = db.Column(db.ForeignKey('user.usr_id'), index=True)
    active_flag = db.Column(db.String(1))
    created_date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_date = db.Column(db.DateTime)

    usr = db.relationship('User', primaryjoin='UserVipList.usr_id == User.usr_id')
    vip = db.relationship('User', primaryjoin='UserVipList.vip_id == User.usr_id')