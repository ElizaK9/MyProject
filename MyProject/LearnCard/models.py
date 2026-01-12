from django.db import models

class Words(models.Model):
    word_foreign = models.CharField(max_length=50)
    word_rus = models.CharField(max_length=50)
    word_topic = models.CharField(max_length=50)
    word_image = models.ImageField("Изображение", upload_to='words_images/', blank=True, null=True)

    def __str__(self):
        return self.word_foreign

class Symbol_alphabet(models.Model):
    letter = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    pronunciation = models.CharField(max_length=250)

    def __str__(self):
        return self.letter