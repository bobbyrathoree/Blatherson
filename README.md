# Blatherson
Blatherson is a chatbot developed using Seq2Seq NMT model by Tensorflow. It uses reddit comments/replies dump since last year (around 900 GB), and is continuously learning.

## Download reddit comments data
http://files.pushshift.io/reddit/comments/

Download however many months of data you want, just keep in mind, takes more time to clean your data and even more to train your bot.

If you wish to use the original model provided by Daniel Kukiela, clone this: https://github.com/daniel-kukiela/nmt-chatbot

Best to use Colab provided by Google to train your model. Make sure to install Tensorflow-GPU. This requires some serious horsepower. If possible, run using Nvidia Tesla P100 or V100 on GCP.

## Sample responses

ME: Where did you come from?
BLATHERSON: The internet

ME: What is the color of the sky?
BLATHERSON: The color of the blue .

ME: What is the best song ever?
BLATHERSON: Darude - Sandstorm

ME: What is the Universe?
BLATHERSON: The Universe is a lie .
