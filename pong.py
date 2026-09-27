import turtle

wind = turtle.Screen()
wind.title("Ping Pong ")
wind.bgcolor("black")
wind.setup(width = 800, height= 600)
wind.tracer(0)
##

#Racket1
Racket1 = turtle.Turtle()
Racket1.speed(0)
Racket1.shape("square")
Racket1.color("Green")
Racket1.shapesize(stretch_wid=5, stretch_len=1)
Racket1.penup()
Racket1.goto(-340,0)

#Racket2
Racket2 = turtle.Turtle()
Racket2.speed(0)
Racket2.shape("square")
Racket2.color("red")
Racket2.shapesize(stretch_wid=5, stretch_len=1)
Racket2.penup()
Racket2.goto(340,0)

#ball 
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0,0)
ball.dx = 2.5
ball.dy = 2.5

# Score
score1 = 0
score2 = 0

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player1: 0   Player2: 0", align="center", font=("Courier", 24, "normal"))


def Racket1_up():
    y = Racket1.ycor()
    y += 20
    if y < 250:  
        Racket1.sety(y)

def Racket1_down():
    y = Racket1.ycor()
    y -= 20
    if y > -250:
        Racket1.sety(y)

def Racket2_up():
    y = Racket2.ycor()
    y += 20
    if y < 250:
        Racket2.sety(y)

def Racket2_down():
    y = Racket2.ycor()
    y -= 20
    if y > -250:
        Racket2.sety(y)


# keyboard
wind.listen() #expext keyboard input

wind.onkeypress(Racket1_up, "w")
wind.onkeypress(Racket1_down, "s")
wind.onkeypress(Racket2_up, "Up")
wind.onkeypress(Racket2_down, "Down")


def update_score():
    pen.clear()
    pen.write("Player1: {}   Player2: {}".format(score1, score2),
               align="center", font=("Courier", 24, "normal"))


def game_loop():
    global score1, score2

    wind.update()

    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # top and bottom
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score1 += 1
        update_score()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score2 += 1
        update_score()

    if (ball.xcor() < -320 and ball.xcor() > -340) and \
       (ball.ycor() < Racket1.ycor() + 50 and ball.ycor() > Racket1.ycor() - 50):
        ball.setx(-320)
        ball.dx *= -1

    if (ball.xcor() > 320 and ball.xcor() < 340) and \
       (ball.ycor() < Racket2.ycor() + 50 and ball.ycor() > Racket2.ycor() - 50):
        ball.setx(320)
        ball.dx *= -1

    wind.ontimer(game_loop, 10)


game_loop()
wind.mainloop()
