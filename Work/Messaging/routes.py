from flask import Blueprint,render_template, redirect, url_for, request, abort, flash
from flask_login import current_user, login_required
from Work.models import Farmer, Message, Restuarant
from Work.Messaging.forms import MessageForm
from Work import db
from datetime import datetime
from sqlalchemy import and_ 

chat = Blueprint('Chat', __name__)


@chat.route('/farmer/chat/<string:recipient_username>/<int:recipient_type>', methods=['POST', 'GET'])
@login_required
def send_message(recipient_username, recipient_type):
    if recipient_type == 0:
        recipient = Farmer.query.filter_by(username=recipient_username).first_or_404()
        
        messages = Message.query.filter( and_(Message.recipient_id == recipient.id, Message.sender_id == current_user.id)).union(
            Message.query.filter( and_(Message.sender_id == recipient.id, Message.recipient_id == current_user.id))
        ).order_by(Message.timestamp.asc() )    


    elif recipient_type == 1:
        recipient = Restuarant.query.filter_by(username=recipient_username).first_or_404()

        messages = Message.query.filter( and_(Message.comp_recipient_id == recipient.id, Message.sender_id == current_user.id)).union(
            Message.query.filter( and_(Message.comp_sender_id == recipient.id, Message.recipient_id == current_user.id))
        ).order_by(Message.timestamp.asc() )   

    else:
        # Bad request
        abort(400)

    title = "Chat"
    form = MessageForm()
    
    # Updating the latest time the current_user read thier message 
    current_user.last_read_time = datetime.utcnow()
    db.session.commit()

    if form.validate_on_submit():
        if recipient_type == 0 and current_user.user_type == 0:
            message = Message(
                author = current_user,
                recipient = recipient,
                body = form.message.data
            )

        elif recipient_type == 1 and current_user.user_type == 0:
            message = Message(
                author = current_user,
                company_recipient = recipient,
                body = form.message.data
            )
        
        elif recipient_type == 0 and current_user.user_type == 1:
            message = Message(
                author = recipient,
                company_sender = current_user,
                body = form.message.data
            )

        elif recipient_type == 1 and current_user.user_type == 1:
            message = Message(
                company_recipient = recipient,
                company_sender = current_user,
                body = form.message.data
            )

        db.session.add(message)
        db.session.commit()
    return render_template('Messaging/messages.html',form=form, title = title, recipient=recipient, messages=messages, recipient_type=recipient_type)


# @chat.route('/user/chat/messages/<string:recipient_username>', methods=['POST', 'GET'])
# @login_required
# def view_message(recipient_username):

#     recipient = User.query.filter_by(username=recipient_username).first_or_404()
#     title = "Messages"
#     current_user.last_read_time = datetime.utcnow()
#     db.session.commit()
#     messages = Message.query.filter( and_(Message.recipient_id == recipient.id, Message.sender_id == current_user.id)).union(
#         Message.query.filter( and_(Message.sender_id == recipient.id, Message.recipient_id == current_user.id))
#     ).order_by(Message.timestamp.asc() )    

#     return render_template("Messaging/messages.html", title=title, messages=messages )


