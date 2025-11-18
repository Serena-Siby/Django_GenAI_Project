import json
import logging
import os
from logging.handlers import RotatingFileHandler

import openai
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hangman
from .serializers import HangSerializer

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(handlers=[RotatingFileHandler("hangman.log", maxBytes=20000000, backupCount=10)],
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    force=True)


class HangmanView(APIView):

    def hangman_function(self):

        user_content = """Prepare a word for the Hangman game and specify the category it belongs to. Additionally, 
        create three clues to assist the user in guessing the word. the clues should be ordered from difficulty to 
        easy, avoiding any scientific terms, and should maintain a jolly tone. Ensure that the clues are short 
        sentences with catchy phrases. 
        
        Response format:
        {
        "word": "word to be guessed", 
        "category": "category the word belongs to", 
        "clue1": "first clue which is a difficult one", 
        "clue2": "second clue with a lower difficulty level compared to clue1", 
        "clue3": "third clue with a lower difficulty level compared to clue2", 
        }
        """

        system_content = """You are a game expert specializing in Hangman, designed for entertainment and stress relief. 
        Be creative, witty, and respond in a relatable manner.
        """

        try:
            response = openai.chat.completions.create(model="gpt-4o", messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ])
            data = response.choices[0].message.content
            logging.info("====================================================")
            logging.info(data)
            logging.info("====================================================")
            return json.loads(data)
        except Exception as e:
            logging.error(e)
            return {"Status": "Failure"}

    def get(self, request):
        game_content = self.hangman_function()
        hang_data  = Hangman(words=game_content["word"], category=game_content["category"], clue_1=game_content["clue1"],
                            clue_2=game_content["clue2"], clue_3=game_content["clue3"])
        hang_data.save()
        word_id = hang_data.id
        response_content = {"word_length": len(game_content["word"]), "word_id": word_id,
                            "category": game_content["category"]}
        return Response(response_content)

    def post(selfSelf, request):
        data = request.data
        word_id = data.get("word_id")
        guessed_letter = data.get("guessed_letter")
        attempts_left = data.get("attempts_left")
        word = Hangman.objects.filter(id=word_id)
        serializer_w = HangSerializer(word, many=True)
        word = serializer_w.data[0]['words'].upper()
        if guessed_letter in word:
            guess = True
            positions = [i for i, char in enumerate(word) if char==guessed_letter]
        else:
            guess = False
            positions = []
            attempts_left -= 1
        return Response({"guess": guess, "position": positions, "attempts_left": attempts_left})


@api_view(["POST"])
def clue_generation(request):
    if request.method == "POST":
        word_id = request.data["word_id"]
        clue_count = request.data["clue_count"]
        clues = Hangman.objects.filter(id=word_id)
        serializer_c = HangSerializer(clues, many=True)
        clues = [v for k, v in serializer_c.data[0].items if k!='words'][:clue_count]
        return Response({"clue": clues})
