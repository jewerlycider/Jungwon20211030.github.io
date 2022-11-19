import numpy as np
import cv2


class RobotArm(object):
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

    def drawPolygon(self,canvas, pts, color, axis=False):
        n = pts.shape[0]
        new_canvas = canvas.copy()
        for k in range(n):
            new_canvas = self.drawLine(new_canvas, pts[int(k%n),0], pts[int(k%n),1], 
                            pts[int((k+1)%n),0], pts[int((k+1)%n),1], color)
        
        if axis == True: # center - pts[0]
            center = np.array([0., 0,0])
            for p in pts:
                center += p 
            center = center / pts.shape[0]
            center = center.astype(np.uint8) 
            # print(center)
            new_canvas = self.drawLine(new_canvas, center[0],center[1], pts[0][0],pts[0][1], color=(255, 128, 128))
        #
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
    
    
    def main(self):
        theta1 = -90
        theta2 = (theta1+self.delta_theta)%360
        theta3 = (theta2+self.delta_theta)%360
        theta4 = (theta3+self.delta_theta)%360
        theta5 = (theta4+self.delta_theta)%360
        
    
        while True:
            new_canvas = self.canvas.copy()
            rect1 = self.getrectangle(self.rect_width,self.rect_height)
            rect2 = self.getrectangle(self.rect_width,self.rect_height)
            rect3 = self.getrectangle(self.rect_width,self.rect_height)
            rect4 = self.getrectangle(self.rect_width,self.rect_height)
            rect5 = self.getrectangle(self.rect_width,self.rect_height)
            
            H1 = self.makeTmat(self.canvas_width//3,self.canvas_height*2//3) @ self.makeRmat(theta1) @ self.makeTmat(0,-self.rect_height//2)
            H2 = self.makeTmat(self.rect_width,0) @ self.makeTmat(0,self.rect_height//2) @ self.makeRmat(theta2) @ self.makeTmat(0,-self.rect_height//2)
            H3 = self.makeTmat(self.rect_width,0) @ self.makeTmat(0,self.rect_height//2) @ self.makeRmat(theta3) @ self.makeTmat(0,-self.rect_height//2)
            H4 = self.makeTmat(self.rect_width,0) @ self.makeTmat(0,self.rect_height//2) @ self.makeRmat(theta4) @ self.makeTmat(0,-self.rect_height//2)
            H5 = self.makeTmat(self.rect_width,0) @ self.makeTmat(0,self.rect_height//2) @ self.makeRmat(theta5) @ self.makeTmat(0,-self.rect_height//2)
            
            rect1 = H1 @ rect1.T
            rect1 = rect1.T
            rect1 = rect1.astype("int")
            new_canvas = self.drawPolygon(new_canvas,rect1,(255,255,255),axis = False)
        
            
            rect2 = H1 @ H2 @ rect2.T
            rect2 = rect2.T
            rect2 = rect2.astype("int")
            new_canvas = self.drawPolygon(new_canvas,rect2,(255,255,255),axis = False)
            
            
            rect3 = H1 @ H2 @ H3 @ rect3.T
            rect3 = rect3.T
            rect3 = rect3.astype("int")
            new_canvas = self.drawPolygon(new_canvas,rect3,(255,255,255),axis = False)

            
            rect4 = H1 @ H2 @ H3 @ H4 @ rect4.T
            rect4 = rect4.T
            rect4 = rect4.astype("int")
            new_canvas = self.drawPolygon(new_canvas,rect4,(255,255,255),axis = False)

            
            rect5 = H1 @ H2 @ H3 @ H4 @ H5 @ rect5.T
            rect5 = rect5.T
            rect5 = rect5.astype("int")
            new_canvas = self.drawPolygon(new_canvas,rect5,(255,255,255),axis = False)
                
                
                
                
            theta2 += 1
            theta3 += 1
            theta4 += 1
            cv2.imshow("canvas",new_canvas)
            cv2.waitKeyEx(30)
                
            
                
            
    
if __name__=="__main__":
    robot_arm = RobotArm(1000,1000,150,80) #가로길이 
    robot_arm.main()