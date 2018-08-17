from django.db import models
from states.models import State


def upload_image_path_questions(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "questions/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class Question(models.Model):
	state          =   models.ForeignKey(State, on_delete=models.CASCADE)
	text  =   models.CharField(max_length=6600)
	question_image =   models.FileField(upload_to = upload_image_path_questions, null = True, blank = True)

	option1        =   models.CharField(blank=True, max_length=2200)
	option2        =   models.CharField(blank=True, max_length=2200)
	option3        =   models.CharField(blank=True, max_length=2200)
	option4        =   models.CharField(blank=True, max_length=2200)

	op1            =   models.BooleanField(default=False)
	op2            =   models.BooleanField(default=False)
	op3            =   models.BooleanField(default=False)
	op4            =   models.BooleanField(default=False)

	time           =   models.IntegerField(default=0)
	score          =   models.IntegerField(default=0)
	integer_type   =   models.BooleanField(default=False)
	single_option  =   models.BooleanField(default=False)
	integeral_answer = models.CharField(blank=True, max_length=100)
	answer_image   =   models.FileField(upload_to = upload_image_path_questions, null = True, blank = True)
	answer_text    =   models.TextField()


	def __str__(self):
		return self.text
