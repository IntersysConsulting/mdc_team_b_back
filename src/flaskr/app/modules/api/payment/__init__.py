from flask_restplus import Resource, Namespace
#from ..resources.cart import UserCart # Not yet implemented
# from werkzeug.datastructures import FileStorage  # Only import if needs files

from .get import Get, Parser as get_cards_parser
from .put import Put, Parser as put_cards_parser
from .delete import Delete, Parser as delete_cards_parser

from flask_jwt_extended import (get_jwt_identity, jwt_required)
any_ns = Namespace(
    "payment",
    description=
    "Endpoints that allow users to interact with their credit cards"
)

###################################
# Payment Section
###################################

@any_ns.route("/")
@any_ns.response(401, "Invalid or missing credentials")
class Pay(Resource):
    #############
    # GET
    #############
    @any_ns.response(200, "Payment info was found")
    @any_ns.response(400, "No payment registered")
    @any_ns.expect(get_cards_parser)
    @jwt_required
    def get(self):
        '''
        √ Returns the user's payment cards (last 4 digits) based on their JWT token.
        '''
        identify = get_jwt_identity()
        args = get_cards_parser.parse_args()
        return Get(args, identify)

    #############
    # PUT
    #############
    @any_ns.response(200, "Card info successfully updated")
    @any_ns.response(400, "Card info could not be added")
    @any_ns.expect(put_cards_parser)
    @jwt_required
    def put(self):
        '''
        √  Add a user's payment card to the list. Create a list and added a card if the list does not exists.
        '''
        identify = get_jwt_identity()
        args = put_cards_parser.parse_args()
        return Put(args, identify)


###################################
# Card Section
###################################

@any_ns.route("/cards")
@any_ns.response(401, "Invalid or missing credentials")
class Card(Resource):
    #############
    # GET
    #############
    @any_ns.response(200, "Card info was found")
    @any_ns.response(400, "No cards registered")
    @any_ns.expect(get_cards_parser)
    @jwt_required
    def get(self):
        '''
        √ Returns all the stripe's customer object
        '''
        identify = get_jwt_identity()
        args = get_cards_parser.parse_args()
        return Get(args, identify)

    #############
    # PUT
    #############
    @any_ns.response(200, "Card info successfully updated")
    @any_ns.response(400, "Card info could not be added")
    @any_ns.expect(put_cards_parser)
    @jwt_required
    def put(self):
        '''
        √  Add a user's payment card. It will create a Stripe Account the first. Set the added card as default.
        '''
        identify = get_jwt_identity()
        args = put_cards_parser.parse_args()
        return Put(args, identify)

    #############
    # DELETE
    #############
    @any_ns.response(200, "Card information was deleted succesfully")
    @any_ns.response(400, "Card ID does not exist")
    @any_ns.expect(delete_cards_parser)
    @jwt_required
    def delete(self):
        '''
        √ Removes a card from the user's list
        '''
        identify = get_jwt_identity()
        args = delete_cards_parser.parse_args()
        return Delete(args, identify)


################################### End Route
