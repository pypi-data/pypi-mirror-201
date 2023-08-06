#%%
import pyrealsense2 as rs
import threading
import time 
import numpy as np

# from PIL import Image
# from IPython.display import display

#%%
class rs2_AsyncCam : 
    def __init__(self,vid_src=0,grab_delay=0.1,width=640,height=480) :
        self.frame_status = False
        self.running = False
        self.depth_frame = None
        self.color_frame = None
        self.grab_delay = grab_delay
        self.width = width
        self.height = height
        self.pipeline = None
        self._critical_Section = None 
            
    def startCamera(self) :
        
        # RealSense context 생성
        context = rs.context()

        # 연결된 모든 RealSense 장치의 정보 얻기
        devices = context.query_devices()

        # 모든 장치의 이름 출력
        for dev in devices:
            print(dev.get_info(rs.camera_info.name))

        self.camera_model = devices[0].get_info(rs.camera_info.name)
        
        if self.pipeline is None :
            pipeline = rs.pipeline()
            config = rs.config()

            # Get device product line for setting a supporting resolution
            pipeline_wrapper = rs.pipeline_wrapper(pipeline)
            pipeline_profile = config.resolve(pipeline_wrapper)
            device = pipeline_profile.get_device()
            device_product_line = str(device.get_info(rs.camera_info.product_line))

            found_rgb = False
            for s in device.sensors:
                if s.get_info(rs.camera_info.name) == 'RGB Camera':
                    found_rgb = True
                    break
            if not found_rgb:
                print("The demo requires Depth camera with Color sensor")
                exit(0)

            config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, 30)

            if device_product_line == 'L500':
                config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
            else:
                config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

            print("device_product_line: ", device_product_line)
            print("found_rgb: ", found_rgb)
            print("init ok")
            profile = pipeline.start(config)
            self.pipeline = pipeline
            
            depth_sensor = profile.get_device().first_depth_sensor()
            depth_scale = depth_sensor.get_depth_scale()

            depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
            depth_intrinsics = depth_profile.get_intrinsics()
            self.depth_intrinsics = depth_intrinsics
            
            color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))            

            # Get the extrinsics (디바이스에서 얻은 extrinsics 사용)
            depth_to_color_extrinsics = depth_profile.get_extrinsics_to(color_profile)

            if "i" in self.camera_model:
                # imu가 포함된 모델
                print("IMU is included in this model.")
                self.extrinsics = profile.get_device().first_pose_sensor().get_extrinsics_to(profile.get_stream(rs.stream.depth))
            else:
                # imu가 없는 모델
                print("IMU is not included in this model.")
                self.extrinsics = profile.get_stream(rs.stream.depth).get_extrinsics_to(profile.get_stream(rs.stream.color))


            print("Depth Intrinsics: ", depth_intrinsics)
            print("Depth to Color Extrinsics: ", depth_to_color_extrinsics)
            print("Extrinsics: ", self.extrinsics)
            
            # Aligning Depth to Color
            self.align = rs.align(rs.stream.color)
            print("align data ok")
            
            # first frame
            frames = self.pipeline.wait_for_frames()            
            aligned_frames = self.align.process(frames)
            self.depth_frame = aligned_frames.get_depth_frame()
            self.color_frame = aligned_frames.get_color_frame()
            self.frame_status = True # frame is ready
            
        else :
            print("camera already started")
    
    def doLastFrame(self) :
        self._critical_Section = threading.Lock()
        t = threading.Thread(target=self._loop, args=())
        #주쓰레드와 생명을 같이한다, FALSE이면 주쓰레드와 관계없이 계속 동작한다.
        t.daemon = True
        t.start()
        self.threadObj = t
        
                  
    def stopCamera(self) :
        self.running = False
        self.frame_status = False
        
    def isOpened(self):
        
        if self._critical_Section is not None :
            if self.frame_status == False or self.running == False:
                return False
            else :
                return True
        else :
            return self.frame_status
        
    def _loop(self) :
        self.running = True
        
        while self.running :
            frames = self.pipeline.wait_for_frames()
            # frames = pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            self.depth_frame = aligned_frames.get_depth_frame()
            self.color_frame = aligned_frames.get_color_frame()
            self.frame_status = True # frame is ready
            time.sleep(self.grab_delay)
            
        print("camera stopped")
        self.pipeline.stop()
        self.pipeline = None
        self.frame_status = False
    def getFrame(self) :
        
        if self._critical_Section is not None :
            with self._critical_Section : 
                if self.frame_status :
                    return True, self.depth_frame, self.color_frame
                else :
                    return False, None, None
        else :
            # frames = pipeline.wait_for_frames()
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            self.depth_frame = aligned_frames.get_depth_frame()
            self.color_frame = aligned_frames.get_color_frame()
            self.frame_status = True # frame is ready
            
            return True, np.asanyarray(self.color_frame.get_data())
    def getDepthFrame(self) :
        return True,self.depth_frame    
    
    def _getPoint3d(self, x, y) :
        if self.frame_status :
            depth = self.depth_frame.get_distance(x, y)
            # 2D 이미지 좌표를 3D 좌표계로 변환
            point = rs.rs2_deproject_pixel_to_point(self.depth_intrinsics, [x, y], depth)
            
            # 픽셀에 해당하는 컬러 이미지의 RGB 값을 가져옴
            # color = self.color_frame.get_data()[y, x]
            color = np.asarray(self.color_frame.get_data())[y, x]
            return (point,(color[0],color[1],color[2]))
            # return point,color
        else :
            return None
    
    def getPoint3d(self, x, y) :
        if self._critical_Section is not None :
            with self._critical_Section : 
                return self._getPoint3d(x, y)
        else :
            return self._getPoint3d(x, y)
    
    def _getPointCloud(self, x1, y1, x2, y2, diff_x, diff_y):
        if self.frame_status :
            # Get the depth and color frames
            depth_frame = self.depth_frame
            color_frame = self.color_frame

            # Get the intrinsics of the camera
            intrinsics = self.depth_intrinsics

            points_list = []
            colors_list = []

            # Loop through the pixels and convert to point cloud coordinates
            for y in range(y1, y2):
                for x in range(x1, x2):
                    _x = x - diff_x;
                    _y = y - diff_y;
                    
                    if _x < 0 or _y < 0 or _x >= self.width or _y >= self.height :
                        depth = 0
                    else :
                        depth = depth_frame.get_distance(_x, _y)
                        
                    point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
                    color = np.asarray(color_frame.get_data())[y, x]

                    # Append point and color data to lists
                    points_list.append(point)
                    colors_list.append(color)

            # Convert lists to numpy arrays
            points = np.array(points_list)
            colors = np.array(colors_list)
            
            return (points, colors)
        else :
            return None
      
    def getPointCloud(self, x1, y1, x2, y2,diff_x=0,diff_y=0):
        if self._critical_Section is not None :
            with self._critical_Section :
                return self._getPointCloud(x1, y1, x2, y2,diff_x,diff_y)
        else :
            return self._getPointCloud(x1, y1, x2, y2,diff_x,diff_y)

#%%
if __name__ == '__main__' :
    import numpy as np
    import cv2

    import PIL.Image as Image
    import PIL.ImageColor as ImageColor
    import PIL.ImageDraw as ImageDraw
    import PIL.ImageFont as ImageFont

    from IPython.display import display
    
    cam = rs2_AsyncCam()
    cam.startCamera()
    
    time.sleep(3)
    
    _, color_frame = cam.getFrame()
    
    display(Image.fromarray( cv2.cvtColor(np.asanyarray(color_frame), cv2.COLOR_BGR2RGB )))
    
    #conver depth to color
    _,depth_frame = cam.getDepthFrame()
    depth_color = cv2.applyColorMap(cv2.convertScaleAbs(np.asanyarray(depth_frame.get_data()), alpha=0.03), cv2.COLORMAP_JET)
    
    display(Image.fromarray(cv2.cvtColor(depth_color, cv2.COLOR_BGR2RGB)))
    
    cam.stopCamera()

# %%
