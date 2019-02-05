from flask import Flask, request
from flask_cors import CORS
from models import db, Contact
from config import SQLALCHEMY_DATABASE_URI
from flask.views import MethodView
import logging
from sqlalchemy import or_
from utils import resp_fail, resp_success
from sqlalchemy.exc import IntegrityError
import sys
from helpers import get_paginated_list
from auth import authorize

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USERNAME'] = 'tester'
app.config['PASSWORD'] = 'tester@123'
db.init_app(app)



class ContactAPI(MethodView):
    # TODO: Add caching wherever required
    def get(self, cid=None):
        search_term = request.args.get("q")
        # pagination params
        start = request.args.get('start') or 1
        limit = request.args.get('limit') or 10
        # fetching a particular contact
        if cid:
            contacts = Contact.query.filter_by(id=cid).all()
        # fetching contacts based on the search term in name or email
        elif search_term:
            contacts = Contact.query.filter(
                or_(Contact.name.contains(search_term),Contact.email_id.contains(search_term))
            ).order_by(Contact.name).all()
        # fetching all contacts if search term is not passed
        else:
            contacts = Contact.query.all()
        data = []
        for contact in contacts:
            c_obj = {}

            c_obj["id"] = contact.id
            c_obj["name"] = contact.name
            c_obj["email"] = contact.email_id
            c_obj["phone"] = contact.phone
            data.append(c_obj)
        return resp_success("Successfully retrieved contacts.", data=get_paginated_list(data, start=int(start), limit=int(limit)))
    
    def post(self, cid=None):
        try:
            data = request.get_json() or {}
            name = data["name"]
            phone_number = data["phone"]
            email = data["email"]
            # check for duplicate email id.
            contact = Contact.query.filter_by(email_id=email).first()
            if contact:
                return resp_fail(f"Contact with same email-id already exists.", status_code=203)            
            contact = Contact(name=name, phone=phone_number, email=email)
            db.session.add(contact)
            db.session.commit()
            return resp_success(f"Contact {name}:{phone_number} was created successfully.", status_code=201)
        except KeyError as e:
            return resp_fail(f"Missing parameter : {e.args[0]}")
        except IntegrityError as e:
            db.session.rollback()
            logger.info(f"Duplicate contact {name}:{email}")
            return resp_fail(f"Contact with same email-id already exists.", status_code=203)
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return resp_fail("Something went wrong.", status_code=500)
    
    def put(self, cid):
        try:
            data = request.get_json() or {}    
            contact = Contact.query.filter_by(id=cid).first()
            contact.name = data["name"]
            contact.phone = data["phone"]
            contact.email_id = data["email"]
            db.session.commit()
            return resp_success("Contact was updated successfully", data = data, status_code=201)
        except AttributeError as e:
            return resp_fail(f"Couldn't find contact with id:{cid}.", status_code=203)
        except KeyError as e:
            return resp_fail(f"Missing parameter : {e.args[0]}")
        except IntegrityError as e:
            db.session.rollback()
            logger.info(f"Duplicate contact {data['name']}:{data['email']}")
            return resp_fail(f"Contact with same email-id already exists.", status_code=203)
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return resp_fail("Something went wrong.", status_code=500)




app.add_url_rule('/contact', view_func=authorize(ContactAPI.as_view('contacts')))
app.add_url_rule('/contact/<cid>', view_func=authorize(ContactAPI.as_view('contacts-detail')))