from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from back_end.mongointerface import MongoInterface
from back_end.recommender import Recommender 
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from back_end.filtersort import BusinessFilter
import graphlab as gl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I love to code YOLO'
#called mango on purpose (too many mongo's)
mango = MongoInterface()
model = gl.load_model("model")
recommender = Recommender(model=model)

@app.route('/', methods=['GET','POST'])
def index():
    '''
    Landing and Login Page
    '''
    return render_template('index.html')

@app.route('/submit_confirmation', methods=['GET','POST'])
def submit_confirmation():
    '''
    Login Checker
    '''
    user_id = request.form['user']
    if mango.login(user_id):
        session['user_id'] = user_id
        return redirect('dashboard')
    else:
        return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    '''
    Homepage, Root Node
    '''
    category= 'Restaurants'
    user_id = session['user_id']
    sf = model.recommend(users=[user_id], k=500)
    bus_filter = BusinessFilter(sf['business_id'], mango)
    business_list = bus_filter.get_filtered_list()
    return render_template('dashboard.html', recommendations=sf, businesses=business_list)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    '''
    Page for Friends
    '''
    user_id = session['user_id']
    friends = mango.get_all_friends(user_id)
    friends = [ mango.get_user(friend) for friend in friends ]
    incoming_invites = [ mango.get_user(inv.inviter_id) for inv in mango.get_all_in_invitations(user_id) ]
    outgoing_invites = [ mango.get_user(inv.invited_id) for inv in mango.get_all_out_invitations(user_id) ]
    return render_template('friends.html', friends=friends, incoming_invites=incoming_invites, outgoing_invites=outgoing_invites)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    '''
    Page for Groups
    '''
    user_id = session['user_id']
    my_groups = mango.get_all_lead_groups(user_id)
    others_groups = mango.get_all_member_groups(user_id)
    incoming_invites = mango.get_all_user_group_invitations(user_id)
    inviting_groups = [ mango.get_group(inv['group_id']) for inv in incoming_invites ]
    return render_template('groups.html', my_groups=my_groups, others_groups=others_groups, inviting_groups=inviting_groups)

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    '''
    Page for Creating Groups
    '''
    group_name = request.args.get('group_name', '', type=str)
    user_id = session['user_id']
    if group_name == '':
        ### blank
        return jsonify(result=0)
    boolean = mango.create_group(user_id, group_name)
    if boolean:
        ### make group with js if db worked
        return jsonify(result=1, group_name=group_name, group_id=group_name+user_id)

    ### duplicate found
    return jsonify(result=-1)

@app.route('/group_up', methods=['GET', 'POST'])
def group_up():
    '''
    Page to Meet up and get recommendations and modify groups
    '''
    user_id = session['user_id']

    group_id = request.form.get('group_up')
    group = mango.get_group(group_id)

    invites = mango.get_all_group_invitations(group_id)
    invited_id = [ invited['invited_id'] for invited in invites ]
    invited = [ mango.get_user(invited_person['invited_id']) for invited_person in invites ]

    members = [mango.get_user(member) for member in group.members]

    rest_of_friends = [ mango.get_user(friend) for friend in 
        mango.get_all_friends(user_id) if (not(friend in group.members))
         and (not(friend in invited_id)) ]

    all_members = group.members
    all_members.append(user_id)
    assert len(all_members)
    recommendation = recommender.make_prediction(all_members)
    groupmodel = recommendation.group_predictions()
    least_misery = groupmodel.average_score()
    bus_filter = BusinessFilter(least_misery['business_id'], mango)

    return render_template('group_up.html', group = group, 
        members = members, rest_of_friends = rest_of_friends, 
        group_businesses = bus_filter.get_filtered_list(),
        invited = invited
        )

@app.route('/disband', methods=['GET', 'POST'])
def disband():
    '''
    Removes a group from db and redirects back to group Page
    '''
    group_id = request.form.get('disband')
    mango.remove('groups', 'group_id', group_id)
    for inv in mango.get_all_group_invitations(group_id):
        mango.remove('group_invitations', 'group_invitation_id', inv['group_invitation_id'])
    return redirect('/groups')

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    '''
    Page Looking at Reviews
    '''
    user_id = session['user_id']
    reviews = mango.get_all_reviews(user_id)
    for review in reviews:
        review['group'] = mango.get_business(review['business_id'])
    return render_template('reviews.html', businesses=reviews)

@app.route('/invite_group', methods=['GET', 'POST'])
def invite_group():
    '''
    Inviting a friend
    '''
    inviter_id = session['user_id']
    invited_id = request.args.get('invited','',type=str)
    group_id = request.args.get('group_id', '', type=str)
    mango.create_group_invitation(inviter_id, invited_id, group_id)
    User = mango.get_user(invited_id)
    return jsonify(invited_id=invited_id, name=User.name)

@app.route('/remove_from_group', methods=['GET', "POST"])
def remove_from_group():
    '''
    Removing a member from group
    '''
    group_id = request.args.get('group_id', '', type=str)
    removing_member = request.args.get('removed','', type=str)
    mango.remove_friend_group(group_id, removing_member)
    return jsonify(group_id=group_id, removing_member=removing_member)

@app.route('/join_group', methods=['GET', "POST"])
def join_group():
    '''
    Joins a group
    '''
    user_id = session['user_id']
    group_id = request.form["join-group"]
    group = mango.get_group(group_id)
    mango.add_friend_group(group_id, user_id)
    invitation = group.leaders_id + user_id + group_id
    print "Inviting", invitation
    mango.remove("group_invitations", "group_invitation_id", invitation)
    return redirect('groups')

@app.route('/decline_group', methods=['GET', "POST"])
def decline_group():
    '''
    Decline a group invite
    '''
    user_id = session['user_id']
    group_id = request.form["decline-group"]
    
    group = mango.get_group(group_id)
    invitation = group.leaders_id + user_id + group_id
    mango.remove("group_invitations", "group_invitation_id", invitation)
    return redirect('groups')

@app.route('/member_leave_group', methods=['GET', "POST"])
def member_leave_group():
    '''
    Leave the group
    '''
    user_id = session['user_id']
    group_id = request.form["leave-group"]
    mango.remove_friend_group(group_id, user_id)
    return redirect('groups')

@app.route('/group_up_member', methods=['GET', "POST"])
def group_up_member():
    '''
    View of the group from member perspective
    '''
    group_id = request.form["grouping-up"]
    group = mango.get_group(group_id)
    user_id = session['user_id']

    invites = mango.get_all_group_invitations(group_id)
    invited_id = [ invited['invited_id'] for invited in invites ]
    invited = [ mango.get_user(invited_person['invited_id']) for invited_person in invites ]

    members = [mango.get_user(member) for member in group.members]

    all_members = group.members
    all_members.append(group.leaders_id)
    assert len(all_members)
    recommendation = recommender.make_prediction(all_members)
    groupmodel = recommendation.group_predictions()
    least_misery = groupmodel.average_score()
    bus_filter = BusinessFilter(least_misery['business_id'], mango)

    return render_template('member_group_up.html', group = group, 
        members = members,
        group_businesses = bus_filter.get_filtered_list(),
        invited = invited
        )

@app.route('/find_friends', methods=['POST'])
def find_friends():
    '''
    Finding friends
    '''
    user_id = session['user_id']
    friends = mango.get_all_friends(user_id)
    input_query = request.form["friend-query"]
    ### filter query with prior friends
    input_query = [ user for user in mango.get_all_users(input_query) if not((user['user_id'] in friends) or (user_id == user['user_id']))]
    return render_template("friends_result.html", results=input_query)

@app.route('/invite_friend', methods=['GET', 'POST'])
def invite_friend():
    '''
    Inviting a friend
    '''
    user_id = session['user_id']
    friend_id = request.args.get("friend_id")
    if mango.create_invitation(user_id, friend_id):
        return jsonify(worked=1)
    return jsonify(worked=-1)

@app.route('/accept_invitation', methods=['GET', 'POST'])
def accept_invitation():
    '''
    Accepting a friend invitation
    '''
    invitation_id = request.form['accept']
    invitation = mango.get_invitation(invitation_id)
    ##make friends
    mango.add_friend(invitation.invited_id, invitation.inviter_id)
    mango.add_friend(invitation.inviter_id, invitation.invited_id)
    ##remove invitation
    mango.remove("invitations", 'invitation_id', invitation_id)
    return redirect('friends')

@app.route('/decline_invitation', methods=['GET', 'POST'])
def decline_invitation():
    '''
    Decline a friend invitation
    '''
    invitation_id = request.form['decline']
    mango.remove("invitations", 'invitation_id', invitation_id)
    return redirect('friends')

@app.route('/find_businesses', methods=['GET', 'POST'])
def find_businesses():
    '''
    Find businesses
    '''
    query = request.form["business-query"]
    businesses = mango.query_businesses(query)
    return render_template("business_results.html", businesses=businesses)

@app.route('/give_rating', methods=['GET', 'POST'])
def give_rating():
    '''
    Rate a business
    '''
    user_id = session['user_id']
    business_id = request.form["business_id"]
    rating = int(request.form['rate'])
    if mango.create_review(user_id, business_id, rating):
        print 'duplicate'
    return redirect('dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)