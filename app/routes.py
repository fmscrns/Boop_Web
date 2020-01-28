import requests, json
from app import boop
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from app.forms import *
from app.decorators import *
from app.services import *
from datetime import datetime

@boop.route("/", methods=["GET", "POST"])
@boop.route("/welcome", methods=["GET", "POST"])
@inaccesible_if_authenticated
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
@inaccesible_if_authenticated
def about():
    return render_template("about.html", title="Welcome")

@boop.route("/signup", methods=["GET", "POST"])
@inaccesible_if_authenticated
def signup_part_one():
    signupPartOneForm = SignupPartOneForm()
    
    if request.method == "POST":
        if signupPartOneForm.validate_on_submit():
            data = request.form

            return redirect(url_for("signup_part_two", firstName=data.get("firstName_input"), lastName=data.get("lastName_input"), email=data.get("email_input"), username=data.get("username_input")))

    return render_template("signup_part_one.html", title="Sign up", signupPartOneForm=signupPartOneForm)

@boop.route("/signup/p2/fname=<firstName>&lname=<lastName>&email=<email>&username=<username>", methods=["GET", "POST"])
@inaccesible_if_authenticated
def signup_part_two(firstName, lastName, email, username):
    signupPartTwoForm = SignupPartTwoForm()

    if request.method == "POST":
        if signupPartTwoForm.validate_on_submit():
            data = {"first_name" : firstName, "last_name" : lastName, "email" : email, "username" : username, "contact_no" : request.form.get("contactNo_input"), "password" : request.form.get("password_input")}
            
            signupUser_json = Auth.signup_user_part_two(data)

            if signupUser_json["status"] == "success":
                Variable.store_session(signupUser_json["authorization"])

                flash(signupUser_json["payload"], "success")

                return redirect(url_for("home"))

            else:
                flash(signupUser_json["payload"], "danger")

                return redirect(url_for("login"))

    return render_template("signup_part_two.html", title="Sign up", signupPartTwoForm=signupPartTwoForm)
    
@boop.route("/login", methods=["GET", "POST"])
@inaccesible_if_authenticated
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
    current_user_page = False
    current_user = User.get_current_user()
    
    shareContentForm = ShareContentForm()

    postList_req = Post.get_all_posts()["data"]
    
    allPosts = []
    for x, post in enumerate(postList_req):
        author = User.get_a_user(post["post_author"])

        dict = {}

        dict["public_id"] = post["public_id"]
        dict["content"] = post["content"]
        dict["posted_on"] = post["posted_on"]
        dict["author_firstName"] =  author["first_name"]
        dict["author_lastName"] = author["last_name"]
        dict["author_username"] = author["username"]
        dict["author_profPhoto_filename"] = author["profPhoto_filename"]
        dict["photo"] = post["photo"]

        allPosts.append(dict)

    return render_template("home.html", title="Home", current_user=current_user, all_posts=allPosts, shareContentForm=shareContentForm, username=current_user["username"] )

@boop.route("/admin/users/all", methods=["GET","POST"])
@login_required
def all_users():
    current_user = User.get_current_user()
    print(current_user)

    users = User.get_all_users()["data"]

    get_specie = Specie.get_all_specie()["data"]
    print(get_specie)
    get_breeds = Breed.get_all_breeds()["data"]



    addSpeciesForm = AddSpeciesForm()
    
    addBreedForm = AddBreedForm()

    if request.method == "POST":
        print('add species!')
        if addSpeciesForm.is_submitted():
                
            addSpecies_json = Specie.new_specie(request)
                
            print('deal routes')
            if addSpecies_json["status"] == "success":
                    
                flash(addSpecies_json["payload"], "success")
                    
                return redirect(url_for("all_users"))
            else:
                flash(addSpecies_json["payload"], "danger")
                    
                return redirect(url_for("all_users"))
        else:
            flash("Try again.", "danger")
                
            return redirect(url_for("all_users"))

    return render_template("admin.html", title="All Users", get_breeds=get_breeds, addBreedForm=addBreedForm, get_specie=get_specie, addSpeciesForm=addSpeciesForm, current_user=current_user, users=users)

@boop.route("/admin/add/<public_id>/breed", methods=["GET","POST"])
@login_required
def add_breed(public_id):
    current_user = User.get_current_user()
    print(current_user)

    users = User.get_all_users()["data"]

    get_specie = Specie.get_all_specie()["data"]
    get_breeds = Breed.get_all_breeds()["data"]


    addBreedForm = AddBreedForm()

    if request.method == "POST":
        
        if addBreedForm.validate_on_submit():
            print('validate breed')
                
            addBreed_json = Breed.new_breed(request, public_id)
                
            print('deal routes')
            if addBreed_json["status"] == "success":
                    
                flash(addBreed_json["payload"], "success")
                    
                return redirect(url_for("all_users"))
            else:
                flash(addBreed_json["payload"], "danger")
                    
                return redirect(url_for("all_users"))
        else:
            flash("Try again.", "danger")
                
            return redirect(url_for("all_users"))

    return redirect(url_for("all_users"))


@boop.route("/admin/specie/<public_id>/delete", methods=["GET","POST","DELETE"])
@login_required
def delete_species(public_id):
    current_user = User.get_current_user()
    get_specie = Specie.get_all_specie()["data"]
    get_breeds = Breed.get_all_breeds()["data"]
     
    Specie.delete_species(public_id)

    return redirect(url_for('all_users'))

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

    addPetForm = AddPetForm()
    updateUserForm = UpdateUserForm()

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
            
            if updateUserForm.validate_on_submit():
                updateUser_json = User.update_user(request)
                
                if updateUser_json["status"]  == "success":
                    flash(updateUser_json["payload"], "success")

                    current_user = User.get_current_user()

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
                
                else:
                    flash(updateUser_json["payload"], "danger")

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

            else:
                flash("Try again.", "danger")
                

                return redirect(url_for("user_profile_posts", username=current_user["username"]))

        elif request.method == "GET":
            updateUserForm.firstName_input.default = current_user["firstName"]
            updateUserForm.lastName_input.default = current_user["lastName"]
            updateUserForm.email_input.default = current_user["email"]
            updateUserForm.username_input.default = current_user["username"]
            updateUserForm.contactNo_input.default = current_user["contactNo"]

            updateUserForm.process()

    return render_template("user_profile.html", title="Account", current_user_page=current_user_page, current_user=current_user, user=user_json, user_pets=userPets, addPetForm=addPetForm, updateUserForm=updateUserForm, petsNavActivate="3px #00002A solid")


@boop.route("/<username>/posts", methods=["GET", "POST"])
@login_required
def user_profile_posts(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    
    user_existence = Helper.user_existence_check(user_json)
    if user_existence is False:
        abort(404)

    postList_req = Post.get_user_posts(username)["data"]

    userPosts = []
    for x, post in enumerate(postList_req):
        author = User.get_a_user(post["post_author"])

        dict = {}

        dict["public_id"] = post["public_id"]
        dict["content"] = post["content"]
        dict["posted_on"] = post["posted_on"]
        dict["author_firstName"] =  author["first_name"]
        dict["author_lastName"] = author["last_name"]
        dict["author_username"] = author["username"]
        dict["author_profPhoto_filename"] = author["profPhoto_filename"]
        dict["photo"] = post["photo"]
        
        userPosts.append(dict)

    shareContentForm = ShareContentForm()
    updateUserForm = UpdateUserForm()

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

            
            if updateUserForm.validate_on_submit():
                updateUser_json = User.update_user(request)
                
                if updateUser_json["status"]  == "success":
                    flash(updateUser_json["payload"], "success")

                    current_user = User.get_current_user()

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
                
                else:
                    flash(updateUser_json["payload"], "danger")

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

            else:
                flash("Try again.", "danger")
                

                return redirect(url_for("user_profile_posts", username=current_user["username"]))

        elif request.method == "GET":
            updateUserForm.firstName_input.default = current_user["firstName"]
            updateUserForm.lastName_input.default = current_user["lastName"]
            updateUserForm.email_input.default = current_user["email"]
            updateUserForm.username_input.default = current_user["username"]
            updateUserForm.contactNo_input.default = current_user["contactNo"]

            updateUserForm.process()

    return render_template("user_profile.html", title="Account", current_user_page=current_user_page, current_user=current_user, user=user_json, user_posts=userPosts, shareContentForm=shareContentForm, updateUserForm=updateUserForm, postsNavActivate="3px #00002A solid")

@boop.route("/<username>/gallery", methods=["GET", "POST"])
@login_required
def user_profile_gallery(username):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)

    user_existence = Helper.user_existence_check(user_json)
    if user_existence is False:
        abort(404)

    userPosts_req =  Post.get_user_posts(username)["data"]
    userGallery = []
    
    for post in userPosts_req:
        if post["photo"] != None:
            userGallery.append(post["photo"])
    
    shareContentForm = ShareContentForm()
    updateUserForm = UpdateUserForm()

    if username == current_user["username"]:
        current_user_page = True

        if request.method == "POST":
            if shareContentForm.validate_on_submit():
                shareContent_json = Post.new_post(request)
                
                if updateUser_json["status"] == "success":
                    
                    flash(updateUser_json["payload"], "success")
                    
                    return redirect(url_for("update_uuser_profile_postsser_posts", username=current_user["username"]))

                else:
                    flash(updateUser_json["payload"], "danger")

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
            
            if updateUserForm.validate_on_submit():
                updateUser_json = User.update_user(request)
                
                if updateUser_json["status"]  == "success":
                    flash(updateUser_json["payload"], "success")

                    current_user = User.get_current_user()

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))
                
                else:
                    flash(updateUser_json["payload"], "danger")

                    return redirect(url_for("user_profile_posts", username=current_user["username"]))

            else:
                flash("Try again.", "danger")
                
                return redirect(url_for("user_profile_posts", username=current_user["username"]))

        elif request.method == "GET":
            updateUserForm.firstName_input.default = current_user["firstName"]
            updateUserForm.lastName_input.default = current_user["lastName"]
            updateUserForm.email_input.default = current_user["email"]
            updateUserForm.username_input.default = current_user["username"]
            updateUserForm.contactNo_input.default = current_user["contactNo"]

            updateUserForm.process()

    return render_template("user_profile.html", title="Account", updateUserForm=updateUserForm, current_user_page=current_user_page, current_user=current_user, user=user_json, user_gallery=userGallery, shareContentForm=shareContentForm, galleryNavActivate="3px #00002A solid")

@boop.route("/<username>/pets/<public_id>", methods=["GET", "POST"])
@boop.route("/<username>/pets/<public_id>/wall", methods=["GET", "POST"])
@login_required
def pet_profile_wall(username, public_id):
    current_user_page = False
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)
    pet_json = Pet.get_a_pet(public_id)
    pet_existence = Helper.pet_existence_check(pet_json)

    if user_existence is False:
        abort(404)

    if pet_existence is False:
        abort(404)

    updatePetForm = UpdatePetForm()

    owner_list = User.get_pet_owners(pet_json["public_id"])["data"]

    for user in owner_list:
        if current_user["username"] == user["username"]:
            current_user_page = True

        pet_json["birthday"] = Helper.datetime_str_to_datetime_obj(pet_json["birthday"])  

    if username == current_user["username"]:
        current_user_page = True

        if request.method == "POST":
            if updatePetForm.validate_on_submit():
                flash("ok", "success")

                return redirect(url_for("pet_profile_wall", username=username, public_id=public_id))

        elif request.method == "GET":
            updatePetForm.petName_input.default = pet_json["pet_name"]
            updatePetForm.bio_input.default = pet_json["bio"]
            updatePetForm.birthday_input.default = pet_json["birthday"]
            updatePetForm.sex_input.default = pet_json["sex"]

            updatePetForm.process()

    return render_template("pet_profile.html", title="Account", updatePetForm=updatePetForm, public_id=public_id, current_user_page=current_user_page, current_user=current_user, user=user_json, pet=pet_json, owner_list=owner_list, postsNavActivate="3px #00002A solid")

@boop.route("/post/<public_id>", methods=["GET", "POST"])
@login_required
def display_post(public_id):
    current_user_page = False
    current_user = User.get_current_user()
    post = Post.get_a_post(public_id)
    post_owner = User.get_a_user(post["post_author"])

    comments = Comment.get_rel_comment(public_id)
    display_comments = []

    if comments:
        for x, comment in enumerate(comments):
            author = User.get_a_user(comment["posted_by"])

            dict = {}

            dict["content"] = comment["comment"]
            dict["author_username"] = comment["posted_by"]
            dict["author_firstName"] = author["first_name"]
            dict["author_lastName"] = author["last_name"]
            dict["posted_on"] = comment["posted_on"]
            dict["profPhoto_filename"] = author["profPhoto_filename"]

            display_comments.append(dict)

    commentPostForm = CommentPostForm()

    if request.method == "POST":
        if commentPostForm.validate_on_submit():
            commentPost_json = Comment.new_comment(request, public_id)
            
            if commentPost_json["status"] == "success":
                
                flash(commentPost_json["payload"], "success")
                
                return redirect(url_for("display_post", public_id=public_id))

            else:
                flash(commentPost_json["payload"], "danger")
                
                return redirect(url_for("display_post", public_id=public_id))
        
        else:
            flash("Try again.", "danger")
            
            return redirect(url_for("user_profile_posts", username=current_user["username"]))

    return render_template("post.html", title="Post", commentPostForm=commentPostForm, post=post, display_comms=display_comments, post_owner=post_owner, current_user=current_user)

@boop.route("/<username>/pets/<public_id>/media", methods=["GET", "POST"])
@login_required
def pet_profile_media(username, public_id):
    return redirect(url_for("pet_profile_wall", username=username, public_id=public_id))

@boop.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.pop("booped_in")

    return redirect(url_for("welcome"))

@boop.route("/<username>/pets/<public_id>/settings", methods=["GET", "POST"])
@boop.route("/<username>/pets/<public_id>/settings/passport", methods=["GET", "POST"])
@login_required
def pet_settings_passport(username, public_id):
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    pet_json = Pet.get_a_pet(public_id)
    pet_existence = Helper.pet_existence_check(pet_json)

    if pet_existence is False:
        abort(404)
    
    return render_template("pet_settings.html", title="Account", current_user=current_user, user=user_json, pet=pet_json, passportActive="active")

@boop.route("/<username>/pets/<public_id>/settings/adoption", methods=["GET", "POST"])
@login_required
def pet_settings_adoption(username, public_id):
    current_user = User.get_current_user()
    user_json = User.get_a_user(username)
    user_existence = Helper.user_existence_check(user_json)

    if user_existence is False:
        abort(404)

    pet_json = Pet.get_a_pet(public_id)
    pet_existence = Helper.pet_existence_check(pet_json)

    if pet_existence is False:
        abort(404)

    if pet_json["status"] == 1:
        closeAdoptionForm = CloseAdoptionForm()

        if closeAdoptionForm.is_submitted():
            closeAdoption_resp = Pet.change_to_no_status(public_id)

            if closeAdoption_resp["status"] == "success":
                flash(closeAdoption_resp["payload"], "success")

                return redirect(url_for("pet_settings_adoption", username=username, public_id=public_id))

            else:
                flash(closeAdoption_resp["payload"], "danger")

                return redirect(url_for("pet_settings_adoption", username=username, public_id=public_id))
    
        return render_template("pet_settings.html", title="Account", current_user=current_user, user=user_json, pet=pet_json, closeAdoptionForm=closeAdoptionForm, adoptionActive="active")

    else:
        forAdoptionForm = ForAdoptionForm()

        if request.method == "POST":
            if forAdoptionForm.validate_on_submit():
                if forAdoptionForm.withoutPost_submit_input.data:
                    changeToAdoptionStatus_resp = Pet.change_to_adoption_status(public_id)

                    if changeToAdoptionStatus_resp["status"] == "success":
                        flash(changeToAdoptionStatus_resp["payload"], "success")
                        
                        return redirect(url_for("pet_settings_adoption", username=username, public_id=public_id))

                    else:
                        flash(changeToAdoptionStatus_resp["payload"], "danger")

                        return redirect(url_for("pet_settings_adoption", username=username, public_id=public_id))
                    
                elif forAdoptionForm.withPost_submit_input.data:
                    shareContent_json = Post.new_post(request)
                
                    if shareContent_json["status"] == "success":
                        changeToAdoptionStatus_resp = Pet.change_to_adoption_status(public_id)

                        if changeToAdoptionStatus_resp["status"] == "success":
                            flash(changeToAdoptionStatus_resp["payload"], "success")

                        else:
                            flash(changeToAdoptionStatus_resp["payload"], "danger")

                        flash(shareContent_json["payload"], "success")
                        
                        return redirect(url_for("user_profile_posts", username=current_user["username"]))

                    else:
                        changeToAdoptionStatus_resp = Pet.change_to_adoption_status(public_id)

                        if changeToAdoptionStatus_resp["status"] == "success":
                            flash(changeToAdoptionStatus_resp["payload"], "success")

                        else:
                            flash(changeToAdoptionStatus_resp["payload"], "danger")

                        flash(shareContent_json["payload"], "danger")
                        
                        return redirect(url_for("user_profile_posts", username=current_user["username"]))
        
        return render_template("pet_settings.html", title="Account", current_user=current_user, user=user_json, pet=pet_json, forAdoptionForm=forAdoptionForm, adoptionActive="active")

@boop.route("/<username>/pets/<public_id>/settings/delete", methods=["GET", "POST"])
@login_required
def pet_settings_delete(username, public_id):
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

    return render_template("pet_settings.html", title="Account", current_user=current_user, user=user_json, pet=pet_json, deleteActive="active")