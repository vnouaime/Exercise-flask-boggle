from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    
    def setUp(self): 
        
        app.config['TESTING'] = True

    def test_home_page(self):
        """ tests home page of application by making sure that session is initialized to zero for both high score and number of plays. makes sure that an html response is being generated """
        with app.test_client() as client: 
            response = client.get("/")
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<div>High Score: <b>0</b></div>", html)
            self.assertIn("<div>Number of Plays: 0</div>", html)

            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
        
    
    def test_session_home_page(self):
        """ tests to make sure that session is updated as browser updates highscore and number of plays """
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highscore'] = 12
                change_session['nplays'] = 10

            response = client.get("/")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(session['highscore'], 12)
            self.assertEqual(session['nplays'], 10)  

    def test_valid_word(self):
        """ creates a demo board first in the session and then checks to see if some words are valid. if they are, server should receive an ok response """
        with app.test_client() as client: 
            with client.session_transaction() as session: 
                session['board'] = [["A", "H", "A", "T", "R"], 
                                    ["A", "H", "A", "T", "R"], 
                                    ["A", "H", "A", "T", "R"], 
                                    ["A", "H", "A", "T", "R"], 
                                    ["A", "H", "A", "T", "R"]]

            response = client.get('/check-word?word=hat')
            response = client.get('/check-word?word=at')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')
           
    def test_not_on_board(self):
        """ tests to see that any word that is not on a board is returning a value from the server indication that it is not on the board """ 
        with app.test_client() as client: 
            response = client.get('/')
            response = client.get('/check-word?word=bat')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_invalid_word(self): 
        """ tests to see if a word sent to the post request is a valid word. server will respond if word is not a real word. """
        with app.test_client() as client: 
            response = client.get('/')
            response = client.get('/check-word?word=fhfhfhfhfjs')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')
                   
    def test_post_score(self): 
        """ tests to see if the post request is encountering any errors while sending """ 
        with app.test_client() as client: 
            response = client.post('/post-score', json={'score': 42})
            response_data = response.get_json()

            self.assertEqual(response.status_code, 200)
