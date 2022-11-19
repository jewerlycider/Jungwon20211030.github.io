# Jungwon20211030.github.io
import numpy as np
import cv2


class Night_Star(object):
    def __init__(self , canvas_width = 1500 , canvas_height=1000 , rect_w = 100 ,rect_h = 100): #가로 세로
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.rect_width = rect_w
        self.rect_height = rect_h
        self.canvas = np.zeros((self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.pre_canvas1 = np.zeros((self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.pre_canvas2 = np.zeros((self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.pre_canvas = np.zeros((self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        
        
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
            try:
                new_canvas[y, x, :] = color
            except:
                pass
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
    
    def getRegularNgon(self,ngon,size=10):
        vertices = []
        delta = 360.0/ngon
        for i in range(ngon):
            degree = delta * i
            radian = self.deg2rad(degree)
            x = np.cos(radian)
            y = np.sin(radian)
            vertices.append((x,y,1/size))        
        vertices = np.array(vertices)
        return vertices*size
    def draw_diag(self,canvas,polygon,on_off = 1.0,color=(50,200,200)):
        if on_off>=0.4: #on off 40이상일때만 그려라
            num = polygon.shape[0] #몇각형인지 //5각형이면 5
            for i in range(num): #0-4
                for count in range(num):
                    if(2<=abs(i-count)<num-1):
                        canvas = self.drawLine(canvas,polygon[count,0],polygon[count,1],polygon[i,0],polygon[i,1],color=color)
            return canvas
        else:
            return canvas
        
    
    def main(self):
        self.stars = []
        self.moving_star = self.getRegularNgon(5,30)
        self.moving_star_T_mat = self.makeTmat(0,-self.canvas_height)
        for i in range(300):
            a,b = np.random.randint(30,self.canvas_width-30),np.random.randint(30,self.canvas_height-30)
            Tmat = self.makeTmat(a,b)
            star = self.getRegularNgon(5)
            star = ((Tmat@star.T).T).astype('int')
            self.stars.append(star)
        theta1 = 270
        while True:
            new_canvas = self.canvas.copy()
            new_canvas = cv2.addWeighted(new_canvas,0.7,self.pre_canvas,0.3,0)

            
            for star in self.stars:
                new_canvas = self.draw_diag(new_canvas,star,np.random.random())
            
            Rmat = self.makeRmat(theta1)
            new_star = ((Rmat@self.moving_star_T_mat@self.moving_star.T).T).astype('int')
            new_canvas = self.draw_diag(new_canvas,new_star,color=(255,255,255))
            
            cv2.imshow("canvas",new_canvas)
            cv2.waitKeyEx(5)

            theta1+=5
            theta1%=360
            
            self.pre_canvas2 = self.pre_canvas1.copy() #잔상 보여준 캔버스 기준으로 한 칸 뒤로 민것 pre1에 잇던거 2로 원래 캔버스 위에서 copy 되면 서 만들어짐 imshow가 최종
            self.pre_canvas1 = new_canvas.copy()
            self.pre_canvas = cv2.addWeighted(self.pre_canvas1,0.7,self.pre_canvas2,0.3,0) #전거 전전거 비율




                
            
                
            
    
if __name__=="__main__":
    robot_arm = Night_Star(1000,1000,150,80) #가로길이 
    robot_arm.main()
