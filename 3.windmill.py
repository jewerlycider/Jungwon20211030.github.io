import numpy as np
import cv2


class Windmill(object):
    def __init__(self , canvas_width = 1500 , canvas_height=1000 , rect_w = 100 ,rect_h = 100): #가로 세로
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.rect_width = rect_w
        self.rect_height = rect_h
        self.canvas = np.zeros((self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.delta_theta = 15
    def getline(self,x0,y0,x1,y1):
        points = []
        if (x0==x1):
            x = x0
            if y0>y1:
                for y in range(y0,y1+1,-1):
                    points.append((x,y,1))
            else:
                for y in range(y0,y1+1):
                    points.append((x,y,1))
            # print(points)
        elif abs((y1-y0)/(x1-x0)) < 1:    
            for x in range(x0,x1+1,1 if x0<x1 else -1):
                if x0 == x1:
                    y = y0
                else:
                    y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x,yint,1))   
        else: 
            for y in range(y0,y1+1,1 if y0<y1 else -1):
                if y0 == y1:
                    x = x0
                else:
                    x = (y   - y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)    
                points.append((xint,y,1))   
        return points 
    def drawLine(self,canvas, x0, y0, x1, y1, color=(255, 255, 255)):
        new_canvas = canvas.copy()
        xys = self.getline(x0, y0, x1, y1)
        for xy in xys:
            x, y, a= xy
            new_canvas[y, x, :] = color
        return new_canvas
    def deg2rad(self,deg):
        rad = deg * np.pi / 180.
        return rad 
    def drawPolygon(self,canvas, pts, color, fill_if_triangle=True):
        n = pts.shape[0]
        new_canvas = canvas.copy()
        points = []
        for k in range(n): #점 28인이유 getline함수때 모든 점의 값을 return 28개는 
            new_canvas = self.drawLine(new_canvas, pts[int(k%n),0], pts[int(k%n),1], 
                            pts[int((k+1)%n),0], pts[int((k+1)%n),1], color)
            points += self.getline(pts[int(k%n),0], pts[int(k%n),1], pts[int((k+1)%n),0], pts[int((k+1)%n),1])
        points = np.array(points)
        if fill_if_triangle:
            ys = points[:,1] #y좌표 뽐은 이유 높이
            ymin = ys.min()
            ymax = ys.max()
            for y in range(ymin,ymax+1,1): #y좌표 최대최소 뽑아서
                same_ys = [] #y좌표가 같은 녀석들
                for p in points: #x최소 최대 뽑기 y좌표는 2개가 나오는 게 맞다 x좌표 전부 칠하기 x최대최소 뽑으면 끝과 끝을 정하고 그 사이 것들을 채운다 가끔
                    if p[1]==y:
                        same_ys.append(p[0])
                xmin = min(same_ys)
                xmax = max(same_ys)
                for x in range(xmin,xmax+1,1):
                    new_canvas[y,x,:]=(255,255,255)
        return new_canvas


    def makeTmat(self,a,b):
        T = np.eye(3,3)
        T[0,2] = a
        T[1,2] = b
        return T
    def makeRmat(self,deg):
        rad = self.deg2rad(deg)
        c = np.cos(rad)
        s = np.sin(rad)
        R =  np.eye(3,3)
        R[0,0] = c
        R[0,1] = -s
        R[1,0] = s
        R[1,1] = c
        return R
    def getrectangle(self,width,height):
        points = []
        points.append((0,0,1))
        points.append((width,0,1))
        points.append((width,height,1))
        points.append((0,height,1))
        points = np.array(points)
        return points
    def gettriangle(self,):
        points=[]
        points.append((0,0,1))
        points.append((200,-50,1))
        points.append((200,50,1))
        return np.array(points)
    def main(self):
        w,h = 100,300
        triangle1 = self.gettriangle()
        triangle2 = self.gettriangle()
        triangle3 = self.gettriangle()
        triangle4 = self.gettriangle()
        triangle5 = self.gettriangle()
        rect = self.getrectangle(w,h)
        theta1 = 72
        theta2 = 72*2
        theta3 = 72*3
        theta4 = 72*4
        theta5 = 0

        x0 = 500
        y0 = 300

        T = self.makeTmat(x0,y0)
        T_w_half = self.makeTmat(-w//2,0)
        while True:
            new_canvas = self.canvas.copy()

            R1 = self.makeRmat(theta1)
            R2 = self.makeRmat(theta2)
            R3 = self.makeRmat(theta3)
            R4 = self.makeRmat(theta4)
            R5 = self.makeRmat(theta5)
            
            new_rect = ((T_w_half@T@rect.T).T).astype("int")
            new_triangle1 = ((T@R1@triangle1.T).T).astype("int")
            new_triangle2 = ((T@R2@triangle2.T).T).astype("int")
            new_triangle3 = ((T@R3@triangle3.T).T).astype("int")
            new_triangle4 = ((T@R4@triangle4.T).T).astype("int")
            new_triangle5 = ((T@R5@triangle5.T).T).astype("int")

            new_canvas = self.drawPolygon(new_canvas,new_rect,(255,255,255),fill_if_triangle=False)
            new_canvas = self.drawPolygon(new_canvas,new_triangle1,(255,255,255))
            new_canvas = self.drawPolygon(new_canvas,new_triangle2,(255,255,255))
            new_canvas = self.drawPolygon(new_canvas,new_triangle3,(255,255,255))
            new_canvas = self.drawPolygon(new_canvas,new_triangle4,(255,255,255))
            new_canvas = self.drawPolygon(new_canvas,new_triangle5,(255,255,255))
            

            cv2.imshow("canvas",new_canvas)
            cv2.waitKeyEx(5)

            theta1+=5
            theta2+=5
            theta3+=5
            theta4+=5
            theta5+=5
            theta1%=360
            theta2%=360
            theta3%=360
            theta4%=360
            theta5%=360




                
            
                
            
    
if __name__=="__main__":
    robot_arm = Windmill(1000,1000,150,80) #가로길이 
    robot_arm.main()