# Jungwon20211030.github.io
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

          
def makeTmat(a,b):
    T = np.eye(3,3)
    T[0,2] = a
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
                getline(canvas,polygon[count,0],polygon[count,1],polygon[i,0],polygon[i,1],color=(255, 255, 255))
    if axis==True:
        Center = getCenter(polygon)
        getline(canvas, Center[0,0],Center[0,1], polygon[0,0],polygon[0,1], color=(255, 128, 128))

def draw_nums(canvas,): #300부터 1을 그린다
    h,w,_ = canvas.shape
    r = min(h//2,w//2)*2//3
    theta = 270
    for i in range(1,13):
        x,y = r*np.cos(deg2rad((theta+i*30)%360)),r*np.sin(deg2rad((theta+i*30)%360))
        x = x+(w//2)
        y = y+(h//2)
        canvas = cv2.putText(canvas,str(i),(int(x)-20,int(y)),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255))#-20좌표를 중간으로 옮기기 위해
    return canvas
               
def main():
    width,height = 400,400
    center_x = width//2
    center_y = height//2
    w,h = 6*10,2*10
    rectangle = np.array([[0,0],[w,0],[w,h],[0,h]])
    base_canvas = draw_nums(np.zeros((height,width,3),dtype=np.uint8)) #캔버스 만들고 drawnums때문에
    theta_hour = 90
    theta_minute = 270
    l = np.ones(4).reshape(4,1)
    while True:
        canvas = base_canvas.copy()
        rect_hour = rectangle.copy()
        rect_minute = rectangle.copy()
        rect_hour = np.concatenate([rect_hour,l],axis=1) #concatenate array2개를 엮는다
        rect_minute = np.concatenate([rect_minute,l],axis=1)
        rect_hour = makeTmat(center_x,center_y) @ makeRmat(theta_hour) @ makeTmat(0,-h//2) @ rect_hour.T
        rect_minute = makeTmat(center_x,center_y) @ makeRmat(theta_minute) @ makeTmat(0,-h//2) @ rect_minute.T
        rect_hour = rect_hour[:2,:].T
        rect_minute = rect_minute[:2,:].T #1을 빼는 것 
        drawPolygon(canvas,rect_hour.astype('int'),(50,200,50))
        drawPolygon(canvas,rect_minute.astype('int'),(50,50,200))
        cv2.imshow("canvas",canvas)
        if cv2.waitKey(20) == 27:
            break
        theta_hour+=3*(15/360)
        theta_minute+=3
    
if __name__ =="__main__":
    main()
