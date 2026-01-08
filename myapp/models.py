from django.db import models

# Create your models here.


class Department(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField()
    dob = models.DateField()
    roll_number = models.CharField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    password = models.CharField()
    semester = models.IntegerField(default=1)


    def __str__(self):
        return self.name

class Result(models.Model):
    semester = models.IntegerField()
    marks = models.IntegerField()
    total_marks = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # usage
    def percentage(self):
        return (self.marks / self.total_marks) * 100

    def grade(self):
        p = self.percentage()
        if p >= 90: return "A+"
        if p >= 80: return "A"
        if p >= 70: return "B"
        if p >= 60: return "C"
        return "D"
    
class Lectures(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"Lecture {self.number}"


class Attendances(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lectures, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.lecture.number} - {'Present' if self.present else 'Absent'}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Faculty(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    phone=models.CharField(max_length=20,blank=True)

class ContactMessage(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
