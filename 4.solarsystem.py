##A solar system with the sun, venus, earth, moon, and a rocket wondering around.
import cv2
import numpy as np

def deg2rad(degree):
    rad = degree * np.pi / 180.0
    return rad

def getRegularNgon(ngon):
        vertices = []
        delta = 360.0/ngon
        for i in range(ngon):
            degree = delta * i
            radian = deg2rad(degree)
            x = np.cos(radian)
            y = np.sin(radian)
            vertices.append((x,y))
            
        vertices = np.array(vertices)
        return vertices
    
def getline(canvas,x0,y0,x1,y1,color):
    # |기울기|<1 --> y =  (x-x0) * (y1-y0) / (x1-x0) +y0
    # |기울기|>1 --> x = (y-y0) * (x1-x0)/(y1-y0) +x0
    if(abs(x1-x0)<abs(y1-y0)): #|기울기|>1인 경우
        if(y1==y0):
            y = y0
            if(x0<x1):
                for x in range(x0,x1+1):
                    canvas[int(y),int(x)] = color
            else:
                for x in range(x0,x1-1,-1):
                    canvas[int(y),int(x)] = color
        else:
            if(y0<y1):
                for y in range(y0,y1+1):
                    x = (y-y0) * (x1-x0)/(y1-y0) +x0
                    canvas[int(y),int(x)] = color
            else:
                for y in range(y0,y1-1,-1):
                    x = (y-y0) * (x1-x0)/(y1-y0) +x0
                    canvas[int(y),int(x)] = color
   
    else:#|기울기|<=1인 경우
        if(x1==x0):
            x = x0
            if(y0<y1):
                for y in range(y0,y1+1):
                    canvas[int(y),int(x)] = color
            else:
                for y in range(y0,y1-1,-1):
                    canvas[int(y),int(x)] = color
        
        else:
            if(x0<x1):
                for x in range(x0,x1+1):
                    y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                    canvas[int(y),int(x)] = color
                    
            else:
                for x in range(x0,x1-1,-1):
                    y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                    canvas[int(y),int(x)] = color
    
def getCenter(pts):
    center = np.array([[0.0,0.0]])
    for p in pts:
        center+=p
        
    center = center / pts.shape[0]
    center = center.astype('int')
    
    return center
    
        
def drawPolygon(canvas,pts,color):
    num = pts.shape[0]
    for i in range(num-1):
        getline(canvas,pts[i,0],pts[i,1],pts[i+1,0],pts[i+1,1],color)   
    getline(canvas,pts[0,0],pts[0,1],pts[-1,0],pts[-1,1],color)  
          
def makeTmat(a,b,ellipse=None):
    if ellipse is None:
        T = np.eye(3,3)
        T[0,2] = a
        T[1,2] = b
        return T
    else:
        T = np.eye(3,3)
        r = (0.25*np.cos(2*deg2rad(ellipse)))+0.75
        if ellipse%90==0:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(1-r)
            print(ellipse)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        T[0,2] = a-a*(1-r)
        T[1,2] = b
        return T


    
def makeRmat(deg,ellipse=False):
    if ellipse==False:
        R = np.eye(3,3)
        radian = deg2rad(deg)
        c = np.cos(radian)
        s = np.sin(radian)
        R[0,0] = c
        R[0,1] = -s
        R[1,0] = s
        R[1,1] = c
        return R
    else:
        R = np.eye(3,3)
        radian = deg2rad(deg)
        c = np.cos(radian)
        s = np.sin(radian)
        R[0,0] = c
        R[0,1] = -s/2
        R[1,0] = s
        R[1,1] = c/2
        return R


def ctoc(canvas,SUN,p2):
    c1 = getCenter(SUN)
    c2 = getCenter(p2) 
    
    getline(canvas, c1[0,0],c1[0,1], c2[0,0],c2[0,1], color=(255, 128, 128))
    
def draw_diag(canvas,polygon,axis=False):
    num = polygon.shape[0] #몇각형인지 //5각형이면 5
    for i in range(num): #0-4
        for count in range(num):
            if(2<=abs(i-count)<num-1):
                getline(canvas,polygon[count,0],polygon[count,1],polygon[i,0],polygon[i,1],color=(50,50,200))
    if axis==True:
        Center = getCenter(polygon)
        getline(canvas, Center[0,0],Center[0,1], polygon[0,0],polygon[0,1], color=(255, 128, 128))             
                   
def main():
    width,height = 1280,720
    color = (255,255,255)
    theta=1
    theta_earth = 0
    theta_venus = 0
    theta_moon = 0
    theta_rocket = 0
    while True:
        canvas = np.zeros((height,width,3),dtype='uint8')
        ngon=10
        points = getRegularNgon(ngon)
        SUN = points.copy()
        SUN*=50
        SUN = SUN.T
        VENUS = SUN.copy()
        EARTH = SUN.copy()
        MOON = SUN.copy()
        ROCKET = SUN.copy()
        VENUS /=4
        EARTH /=2
        MOON/=4
        ROCKET/=4
     
        l = np.ones(ngon) #1로만 이루어진 행렬 만들기
        SUN = np.append(SUN,[l],axis=0) #axis=0 --> 행 추가 // if axis=1 -->열 추가
        VENUS = np.append(VENUS,[l],axis=0)
        EARTH = np.append(EARTH,[l],axis=0)#3 by 3 행렬로 만들기
        MOON = np.append(MOON,[l],axis=0)
        ROCKET = np.append(ROCKET,[l],axis=0)
        
        points = makeTmat(width//2,height//2) @ makeRmat(theta) @ SUN
        # points = makeTmat(600,400) @ makeRmat(theta) @ P1
        points = np.delete(points,2,axis=0)
        points = points.T
        points = points.astype('int')
        drawPolygon(canvas,points,(50,50,200))
        ###########################################################태양
        venus = makeTmat(width//2,height//2)@ makeRmat(theta_venus) @makeTmat(100,0) @ makeRmat(theta_venus) @VENUS
        cv2.circle(canvas,(width//2,height//2),100,(0,127,255),3)
        venus = np.delete(venus,2,axis=0)
        venus = venus.T
        venus =venus.astype('int')
        ctoc(canvas,points,venus)
        draw_diag(canvas,venus,(150,233,233))
        ###########################################################금성
        earth = makeTmat(width//2,height//2)@ makeRmat(theta_earth) @makeTmat(175,0) @ makeRmat(theta_earth) @EARTH
        cv2.circle(canvas,(width//2,height//2),175,(200,50,50),3)
        earth = np.delete(earth,2,axis=0)
        earth = earth.T
        earth =earth.astype('int')
        ctoc(canvas,points,earth)
        draw_diag(canvas,earth,(200,50,50))
        ############################################################지구
        earth_x,earth_y = getCenter(earth)[0,:]
        moon = makeTmat(earth_x,earth_y)@ makeRmat(theta_moon) @makeTmat(50,0) @ makeRmat(theta_moon) @MOON
        cv2.circle(canvas,(earth_x,earth_y),50,(200,200,200),3)
        moon = moon.T
        moon =moon.astype('int')
        drawPolygon(canvas,moon,color)
        ############################################################# 달
        # rocket = makeTmat(500,0,ellipse=theta_rocket) @ROCKET
        rocket = makeTmat(width//2,height//2)@ makeRmat(theta_rocket) @makeTmat(500,0) @ makeRmat(theta_rocket) @ROCKET
        ys = rocket[1,:]
        y_dif = ys-(height//2)
        rocket[1,:] = rocket[1,:]-y_dif//2
        rocket = np.delete(rocket,2,axis=0)
        cv2.ellipse(canvas,(width//2,height//2),(500,250),0,0,360,(50,200,50))
        rocket = rocket.T
        rocket =rocket.astype('int')
        ctoc(canvas,points,rocket)
        draw_diag(canvas,rocket)
        ############################################################# 로켓
        cv2.imshow("myWindow",canvas)
        if cv2.waitKey(20) == 27:
            break
        
        theta +=1
        theta_earth+=2
        theta_venus+=3
        theta_moon+=4
        theta_rocket+=1
        theta%=360
        theta_earth%=360
        theta_venus%=360
        theta_moon%=360
        theta_rocket%=360
        
    
if __name__ =="__main__":
    main()