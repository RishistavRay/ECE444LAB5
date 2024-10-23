import pytest
import requests

class TestFlaskApp:
    BASE_URL = 'http://servesentiment-env.eba-wzth6yic.us-east-1.elasticbeanstalk.com/'

    @pytest.mark.parametrize("text, expected", [
        ("real news", 'real'),
        ("honesty is the best policy", 'real'),
        ("The moon is made of cheese.", 'fake'),
        ("Aliens have invaded Earth!", 'fake'),
    ])
    def test_prediction(self, text, expected):
        response = requests.post(self.BASE_URL, data={'text': text})
        assert response.status_code == 200

      
        response_text = response.text.lower()
      
        start_index = response_text.find('prediction: ') + len('prediction: ')
        end_index = response_text.find('</div>', start_index)

   
        prediction_text = response_text[start_index:end_index].strip()

        assert expected in prediction_text

if __name__ == "__main__":
    pytest.main()
