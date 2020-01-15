import requests, json
from app import boop
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from app.forms import *
from app.decorators import *
from app.services import *

@boop.route("/", methods=["GET", "POST"])
@boop.route("/welcome", methods=["GET", "POST"])
@not_authenticated
def welcome():
    loginForm = LoginForm()

    if request.method == "POST":
        if loginForm.validate_on_submit():
            form = request.form

            loginUser_json = Auth.login_user(form)
            
            if loginUser_json["status"] == "success":
                Variable.store_session(loginUser_json["authorization"])

                flash(loginUser_json["payload"], "success")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))

            else:
                flash(loginUser_json["payload"], "danger")

                return redirect(url_for("login"))

    return render_template("welcome.html", title="Welcome", loginForm=loginForm)

@boop.route("/about", methods=["GET", "POST"])
@not_authenticated
def about():
    return render_template("about.html", title="Welcome")

@boop.route("/signup", methods=["GET", "POST"])
@not_authenticated
def signup():
    signupForm = SignupForm()

    if request.method == "POST":
        if signupForm.validate_on_submit():
            form = request.form

            signupUser_json = Auth.signup_user(form)

            if signupUser_json["status"] == "success":
                Variable.store_session(signupUser_json["authorization"])

                flash(signupUser_json["payload"], "success")

                return redirect(url_for("home"))

            else:
                flash(signupUser_json["payload"], "danger")

                return redirect(url_for("login"))

    return render_template("signup.html", title="Welcome", signupForm=signupForm)
    
@boop.route("/login", methods=["GET", "POST"])
@not_authenticated
def login():
    loginForm = LoginForm()

    if request.method == "POST":
        if loginForm.validate_on_submit():
            form = request.form

            loginUser_json = Auth.login_user(form)
            
            if loginUser_json["status"] == "success":
                Variable.store_session(loginUser_json["authorization"])

                flash(loginUser_json["payload"], "success")

                return redirect(url_for("home"))

            else:
                flash(loginUser_json["payload"], "danger")

                return redirect(url_for("login"))
            
    return render_template("login.html", title="Welcome", loginForm=loginForm)

@boop.route("/home", methods=["GET", "POST"])
@login_required
def home():
    form = ShareContentForm()
    
    current_user = User.get_current_user()

    posts = Post.get_all_posts()["data"]
    # post_json = Post.get_user_posts(username)
    print(posts)

    i=0

    while i < len(posts):
        posts[i]["posted_on"] = Helper.datetime_str_to_datetime_obj(posts[i]["posted_on"])  
        i += 1

    return render_template("home.html", title="Home", current_user=current_user, all_posts=posts, shareContentForm=form)

@boop.route("/admin/users/all", methods=["GET"])
@login_required
def all_users():
    current_user = User.get_current_user()

    users = User.get_all_users()["data"]

    return render_template("manage_user.html", title="All Users", current_user=current_user, users=users)


@boop.route("/<username>/pets", methods=["GET", "POST", "PUT"])
@login_required
def user_profile_pets(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    userPets = Pet.get_user_pets(username)["data"]
    for pet in userPets:
        print(pet["profPic_filename"])

    addPetForm = AddPetForm()
    updateUserForm = SignupForm()

    if username == current_user["username"]:
        current_user_page = True

        Helper.modify_addPetForm(addPetForm)

        if request.method == "POST":
            addPetForm.breed_input.choices = [(request.form.get("breed_input"), "")]
            if addPetForm.validate_on_submit():
                addPet_json = Pet.add_a_pet(request)

                if addPet_json["status"] == "success":
                    flash(addPet_json["payload"], "success")

                    return redirect(url_for("user_profile_pets", username=current_user["username"]))

                else:
                    flash(addPet_json["payload"], "danger")

                    return redirect(url_for("user_profile_pets", username=current_user["username"]))
            
            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_pets", username=current_user["username"]))


    return render_template("user_profile.html", title="Account", current_user_page=current_user_page, current_user=current_user, user=user_json, user_pets=userPets, addPetForm=addPetForm, updateUserForm=updateUserForm, petsNavActivate="3px #00002A solid")

'''
@boop.route("/<username>/update", methods=["GET", "POST"])
@login_required
def update_user(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    updateUserForm = SignupForm()

    if username == current_user["username"]:
        current_user_page = True

        if request.method == "POST":
            
            if updateUserForm.validate_on_submit():
                userUpdate_json = User.update_user(request)
                print('ipa graduate nako pls!')    
                if userUpdate["status"] == "success":
                    flash(userUpdate_json["payload"], "success")

                    return redirect(url_for("user_profile_pets", username=current_user["username"]))

                else:
                    flash(userUpdate_json["payload"], "danger")

                    return redirect(url_for("user_profile_pets", username=current_user["username"]))
            
            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_pets", username=current_user["username"]))



@boop.route("/<username>/update", methods=["GET", "POST"])
@login_required
def update_user(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    updateUserForm = SignupForm()

    if username == current_user["username"]:
        current_user_page = True

        if request.method == "POST":
            
            if updateUserForm.validate_on_submit():
                print('bitchhh')
                updateUser_json = User.update_user(request)

                updateUserForm.firstName_input = request.form['firstName_input']
                updateUserForm.last_name = request.form['last_name']
                updateUserForm.contactNo_input = request.form['contactNo_input']
                updateUserForm.username_input = request.form['username_input']
                updateUserForm.email_input = request.form['email_input']

                User.update_user(username)
                flash('Your info has been updated!', 'success')
            return redirect(url_for("user_profile_pets", username=current_user["username"]))
        return redirect(url_for("user_profile_pets", username=current_user["username"]))
	
    return redirect(url_for("user_profile_pets", username=current_user["username"]))
'''

@boop.route("/<username>/edit", methods=["GET", "PUT"])
@login_required
def update_user(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)
    

    if user_existence is False:
        abort(404)

    User.update_user(username)['data']

    updateUserForm = SignupForm()

    if request.method == "POST":
        if updateForm.validate_on_submit():
            form = request.form

            updatepUser_json = User.update_user(form,username)

            if updatepUser_json["status"] == "success":
                Variable.store_session(updatepUser_json["authorization"])

                flash(updatepUser_json["payload"], "success")

                return redirect(url_for("user_profile_pets", username=current_user["username"]))

            else:
                flash(updatepUser_json["payload"], "danger")

                return redirect(url_for("user_profile_pets", username=current_user["username"]))
        
        return redirect(url_for("user_profile_pets", username=current_user["username"]))

    elif request.method == "GET":
        updateForm.firstName_input.data = current_user["firstName"]
        updateForm.lastName_input.data = current_user["lastName"]
        updateForm.email_input.data = current_user["email"]
        updateForm.username_input.data = current_user["username"]
        updateForm.contactNo_input.data = current_user["contactNo"]            

    
    return redirect(url_for("user_profile_pets", username=current_user["username"]))



@boop.route("/<username>/posts", methods=["GET", "POST"])
@login_required
def user_profile_posts(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)
    post_json = Post.get_user_posts(username)
    posts = Post.get_all_posts()["data"]
    comments = Comment.get_all_comments()["data"]
    print("aw: ",comments)

    if user_existence is False:
        abort(404)

    for p in posts:
        for c in comments:
                print(p["content"])
                if p["post_id"] == c["post_id"]:
                    print(c["comment"]) 

    userPosts = Post.get_user_posts(username)["data"]
    
    updateUserForm = SignupForm()
    commentPostForm = CommentPostForm()
    # post_json = Post.get_user_posts(username)
    print(userPosts)

    i=0

    while i < len(userPosts):
        userPosts[i]["posted_on"] = Helper.datetime_str_to_datetime_obj(userPosts[i]["posted_on"])  
        i += 1

    
    updateUserForm = SignupForm()
    commentPostForm = CommentPostForm()
    shareContentForm = ShareContentForm()

    if username == current_user["username"]:
        current_user_page = True

        userPets_json = Pet.get_user_pets(username)

        if request.method == "POST":
            
            if shareContentForm.validate_on_submit():
                shareContent_json = Post.new_post(request)
                
                if shareContent_json["status"] == "success":
                    
                    flash(shareContent_json["payload"], "success")
                    
                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

                else:
                    flash(shareContent_json["payload"], "danger")
                    
                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
            
            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_posts", username=current_user["username"]))

    return render_template("aw.html", title="Account", commentPostForm = commentPostForm, updateUserForm=updateUserForm, post_json=post_json, current_user_page=current_user_page, current_user=current_user, user=user_json, user_posts=userPosts, shareContentForm=shareContentForm, comments=comments, postsNavActivate="3px #00002A solid")

@boop.route("/<username>/posts/<post_id>/comment", methods=["GET", "POST"])
@login_required
def comment(username, post_id):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)
    post_json = Post.get_user_posts(username)

    if user_existence is False:
        abort(404)

    userPosts = Post.get_user_posts(username)["data"]
    commentPostForm = CommentPostForm()

    if username == current_user["username"]:
        current_user_page = True

    if request.method == "POST":
            print('comment bitchhh')
            if commentPostForm.validate_on_submit():
                commentPost_json = Comment.new_comment(request,post_id)
                

                if commentPost_json["status"] == "success":
                    
                    flash(commentPost_json["payload"], "success")
                    
                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

                else:
                    flash(commentPost_json["payload"], "danger")
                    
                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
            
            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_posts", username=current_user["username"]))

    return redirect(url_for("user_profile_posts", username=current_user["username"]))
   

@boop.route("/<username>/posts/<post_id>/delete", methods=["GET","POST","DELETE"])
@login_required
def delete_post(post_id, username):
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    post_json = Post.get_user_posts(username)

    if username == current_user["username"]:
        current_user_page = True
        
        Post.delete_post(post_id)
    
        print(post_id)


    return redirect(url_for('user_profile_posts',username=current_user["username"]))

@boop.route("/<username>/pets/<public_id>", methods=["GET", "POST"])
@boop.route("/<username>/pets/<public_id>/wall", methods=["GET", "POST"])
@login_required
def pet_profile_wall(username, public_id):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    pet_json = Pet.get_a_pet(public_id)
    pet_existence = Helper.pet_existence_check(pet_json)
    
    if pet_existence is False:
        abort(404)

    owner_list = User.get_pet_owners(pet_json["public_id"])["data"]

    for user in owner_list:
        if current_user["username"] == user["username"]:
            current_user_page = True

    pet_json["birthday"] = Helper.datetime_str_to_datetime_obj(pet_json["birthday"])  

    return render_template("pet_profile.html", title="Account", public_id=public_id, current_user_page=current_user_page, current_user=current_user, user=user_json, pet=pet_json, owner_list=owner_list, postsNavActivate="3px #00002A solid")


@boop.route("/<username>/pets/<public_id>/delete", methods=["GET","POST","DELETE"])
@login_required
def delete_pet(public_id, username):
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    pet_json = Pet.get_a_pet(public_id)
    pet_existence = Helper.pet_existence_check(pet_json)


    if pet_existence is False:
        abort(404)
    
    if username == current_user["username"]:
        current_user_page = True
        
        Pet.delete_pet(public_id)
     
    pet_json["birthday"] = Helper.datetime_str_to_datetime_obj(pet_json["birthday"])  

    return redirect(url_for('user_profile_pets',username=current_user["username"]))
'''
@boop.route("/<username>/pet/<pet_id>/deal", methods=["GET", "POST"])
@login_required
def deal_pet(username, pet_id):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    dealPetForm = DealPetForm()

    if username == current_user["username"]:
        current_user_page = True

    if request.method == "POST":
            print('comment bitchhh')
            if dealPetForm.validate_on_submit():
                dealPet_json = Deal.new_deal(request,pet_id)
                
                print('deal routes')
                if dealPet_json["status"] == "success":
                    
                    flash(dealPet_json["payload"], "success")
                    
                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

                else:
                    flash(dealPet_json["payload"], "danger")
                    
                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
            
            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_posts", username=current_user["username"]))

    return redirect(url_for("pet_profile_wall",username=current_user["username"]))
'''   

@boop.route("/<username>/pets/<public_id>/update", methods=["GET","PUT","DELETE"])
@login_required
def update_pet(public_id, username):
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    pet_json = Pet.get_a_pet(public_id)
    pet_existence = Helper.pet_existence_check(pet_json)


    if pet_existence is False:
        abort(404)
    
    if username == current_user["username"]:
        current_user_page = True
        
        Pet.update_pet(public_id)
     
    pet_json["birthday"] = Helper.datetime_str_to_datetime_obj(pet_json["birthday"])  

    return redirect(url_for('pet_profile_wall',username=username, public_id=public_id))


@boop.route("/<username>/pets/<public_id>/media", methods=["GET", "POST"])
@login_required
def pet_profile_media(username, public_id):
    return redirect(url_for("pet_profile_wall", username=username, public_id=public_id))

@boop.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.pop("booped_in")

    return redirect(url_for("welcome"))