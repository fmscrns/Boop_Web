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

                return redirect(url_for("home"))

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
    current_user = User.get_current_user()

    return render_template("home.html", title="Home", current_user=current_user)

@boop.route("/<username>/pets", methods=["GET", "POST"])
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

    return render_template("user_profile.html", title="Account", current_user_page=current_user_page, current_user=current_user, user=user_json, user_pets=userPets, addPetForm=addPetForm, petsNavActivate="3px #00002A solid")

@boop.route("/<username>/posts", methods=["GET", "POST"])
@login_required
def user_profile_posts(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    userPosts = []

    shareContentForm = ShareContentForm()

    if username == current_user["username"]:
        current_user_page = True

        userPets_json = Pet.get_user_pets(username)

        shareContentForm.taggedPet_input.choices = [(data["public_id"], data["pet_name"]) for data in userPets_json["data"]]

        if request.method == "POST":
            if shareContentForm.validate_on_submit():
                shareContent_json = Content.share_a_content(request)

                if shareContent_json["status"] == "success":
                    flash(shareContent_json["payload"], "success")

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

                else:
                    flash(shareContent_json["payload"], "danger")

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
            
            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_posts", username=current_user["username"]))

    return render_template("user_profile.html", title="Account", current_user_page=current_user_page, current_user=current_user, user=user_json, user_posts=userPosts, shareContentForm=shareContentForm, postsNavActivate="3px #00002A solid")

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

    return render_template("pet_profile.html", title="Account", current_user_page=current_user_page, current_user=current_user, user=user_json, pet=pet_json, owner_list=owner_list, postsNavActivate="3px #00002A solid")

@boop.route("/<username>/pets/<public_id>/media", methods=["GET", "POST"])
@login_required
def pet_profile_media(username, public_id):
    return redirect(url_for("pet_profile_wall", username=username, public_id=public_id))

@boop.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.pop("booped_in")

    return redirect(url_for("welcome"))