from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from forms import PositionAnalysis, VelAccAnalysis
from math import cos, sin, pi, atan, sqrt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PositionAnalysis()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        c = form.c.data
        d = form.d.data
        theta2 = form.theta2.data
        pa = positionAnalysis(a,b,c,d, theta2)
        return render_template('position_results.html',a = a, b = b, c = c, d = d, theta2 = theta2,  k1 = pa['k1'], k2 = pa['k2'], k3 = pa['k3'], k4 = pa['k4'], k5 = pa['k5'],\
            A = pa['A'], B = pa['B'], C = pa['C'], D = pa['D'], E = pa['E'], F = pa['F'],\
            theta4_p = pa['theta4_p'], theta4_m = pa['theta4_m'], theta3_p = pa['theta3_p'], theta3_m = pa['theta3_m'])

    return render_template('pos_in.html', form = form)

@app.route('/vel_acc', methods = ['GET','POST'])
def vel_acc():
    form = VelAccAnalysis()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        c = form.c.data
        d = form.d.data
        theta2 = form.theta2.data
        theta3 = form.theta3.data
        theta4 = form.theta4.data
        omega2 = form.omega2.data
        alpha2 = form.alpha2.data
    
        va = velaccAnalysis(a,b,c,d, theta2, theta3, theta4, omega2, alpha2)
        return render_template('vel_acc_results.html', a = a, b = b, c = c, d = d, \
            theta2 = theta2, theta3 = theta3,  theta4 = theta4, \
            omega2 = omega2, omega3 = va['omega3'], omega4 = va['omega4'], \
            alpha2 = alpha2, alpha3 = va['alpha3'], alpha4 = va['alpha4'],\
            A = va['A'], B = va['B'], C = va['C'], D = va['D'], E = va['E'], F = va['F'])

    return render_template('vel_acc_in.html', form = form)



def positionAnalysis(a,b,c,d,theta2):
    theta2 = theta2*pi/180 #theta2 is now in radians

    # POSITION ANALYSIS
    k1 = d/a
    k2 = d/c
    k3 = (a**2 - b**2 + c**2 + d**2)/(2*a*c)

    A = cos(theta2) - k1 - k2*cos(theta2) + k3
    B = -2*sin(theta2)
    C = k1 - (k2+1)*cos(theta2) + k3

    theta4_p = 2*atan(\
        (-B + sqrt(B**2 - 4*A*C))/(2*A)\
            )

    theta4_m = 2*atan(\
        (-B - sqrt(B**2 - 4*A*C))/(2*A)\
            )
    
    k4 = d/b
    k5 = (c**2 - d**2 - a**2 - b**2)/(2*a*b)

    D = cos(theta2) - k1 + k4*cos(theta2) + k5
    E = -2*sin(theta2)
    F = k1 + (k4-1)*cos(theta2) + k5

    theta3_p = 2*atan(\
        (-E + sqrt(E**2 - 4*D*F))/(2*D)\
            )

    theta3_m = 2*atan(\
        (-E - sqrt(E**2 - 4*D*F))/(2*D)\
            )

    #convert to degrees:
    theta4_p = theta4_p*(180/pi)
    theta4_m = theta4_m*(180/pi)
    theta3_p = theta3_p*(180/pi)
    theta3_m = theta3_m*(180/pi)
    
    result = {'k1':k1, 'k2':k2, 'k3':k3, 'k4':k4, 'k5':k5, 'A':A,'B':B,'C':C,'D':D,'E':E,'F':F,\
         'theta4_p':theta4_p, 'theta4_m':theta4_m, 'theta3_p':theta3_p, 'theta3_m':theta3_m }

    return result

def velaccAnalysis(a,b,c,d, theta2, theta3, theta4, omega2, alpha2):

    #convert angles to radians
    theta2 = theta2*pi/180 
    theta3 = theta3*pi/180 
    theta4 = theta4*pi/180 

    #VELOCITY ANALYSIS
    omega3 = (a*omega2*sin(theta4-theta2))/(b*sin(theta3 - theta4))
    omega4 = (a*omega2*sin(theta2-theta3))/(c*sin(theta4-theta3))

    #ACCELERATION ANALYIS
    A = c*sin(theta4)
    B = b*sin(theta3)
    C = a*alpha2*sin(theta2) + a*(omega2**2)*cos(theta2) + b*(omega3**2)*cos(theta3) - c*(omega4**2)*cos(theta4)
    D = c*cos(theta4)
    E = b*cos(theta3)
    F = a*alpha2*cos(theta2) - a*(omega2**2)*sin(theta2) - b*(omega3**2)*sin(theta3) + c*(omega4**2)*sin(theta4)

    alpha3 = ( ((C*D)-(A*F)) / ((A*E) - (B*D)) )
    alpha4 = ( ((C*E)-(B*F)) / ((A*E) - (B*D)) )

    result = {'omega3':omega3, 'omega4':omega4, 'A':A,'B':B,'C':C,'D':D,'E':E,'F':F,\
         'alpha3':alpha3, 'alpha4':alpha4 }
    
    return result

if __name__ == "__main__":
    app.run()
    


