import cv2
import pyrealsense2 as rs
# from realsense_depth import *
import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import numpy as np

# # defth camera
# class DepthCamera:
#     def __init__(self):
#         self.pipeline = rs.pipeline()
#         config = rs.config()
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))
#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 6)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#         cfg = self.pipeline.start(config)
#         # self.pipeline.wait_for_frames(10000)

#     def get_frame(self):
#         frames = self.pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()

#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
#         if not depth_frame or not color_frame:
#             return False, None, None
#         return True, depth_image, color_image

#     # def release(self):
#     #     self.pipeline.stop()

#     def show_intrinsics(self):

#         depth_intrinsics = self.pipeline.get_active_profile().get_stream(
#             rs.stream.depth).as_video_stream_profile().get_intrinsics()
#         return depth_intrinsics

#     def camera_cordinates(self, u, v, ppx, ppy, fx, fy, depth):
#         x = ((u-ppx) * depth)/(fx)
#         y = ((v-ppy) * depth)/(fy)
#         z = depth
#         return x, y, z
    


# customtkinter.set_appearance_mode("System")  
# customtkinter.set_default_color_theme("blue") 
# dc = DepthCamera() 



# Tkinter API
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("TULIP: Tea Plucking System")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TULIP", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = "OpenCamera", command=self.OpenCamera_btn)
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text = "Capture_Image", command=self.CaptureImage_btn)
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=10)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Color_Frame", "Depth_Frame", "Pointing"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=3, column=0, padx=10, pady=(10, 10))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Origin", "Plucking"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=4, column=0, padx=10, pady=(10, 10))
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="EXIT", command=self.quit)
        self.sidebar_button_3.grid(row=5, column=0, padx=10, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mode:", anchor="w")
        self.appearance_mode_label.grid(row=15, column=0, padx=5, pady=(5, 5))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=16, column=0, padx=5, pady=(5, 5))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Screen Scaling:", anchor="w")
        self.scaling_label.grid(row=17, column=0, padx=5, pady=(5, 5))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=18, column=0, padx=5, pady=(5, 5))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text=" ")
        self.entry.grid(row=3, column=1, columnspan=2,rowspan =10, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text = "Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # create textbox
        self.textbox = customtkinter.CTkFrame(self)
        self.textbox.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")
        # self.heading = customtkinter.CTkLabel(self, text="TEA PLUCKING SYSTEM")
        # self.heading.grid(padx = 10,pady=10, sticky= "nswe")
        
        # # create tabview   
        

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="COORDINATE INPUT :")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="nsew")
        self.radio_button_1 = customtkinter.CTkButton(self.radiobutton_frame, text="Coordinate input", command= self.open_input_dialog_event)
        self.radio_button_1.grid(row=1, column=2, padx=20, pady= (10,10))
        self.radio_button_2 = customtkinter.CTkButton(self.radiobutton_frame, text="Refresh", command= self.Refresh_btn)
        self.radio_button_2.grid(row=2, column=2, padx=20, pady= (10,10))
        
        # # create slider and progressbar frame
        #########################################
        # # create scrollable frame
        #######################################
        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew") 
        self.entry1 = customtkinter.CTkEntry(self.checkbox_slider_frame, placeholder_text="X Point - ")
        self.entry1.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.entry2 = customtkinter.CTkEntry(self.checkbox_slider_frame, placeholder_text="Y Point - ")
        self.entry2.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.entry3 = customtkinter.CTkEntry(self.checkbox_slider_frame, placeholder_text="Z Point - ")
        self.entry3.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.submit_button_1 = customtkinter.CTkButton(master=self.checkbox_slider_frame, text = "Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.submit_button_1.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # set default values
        # self.checkbox_1.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Hii! How are you\n\n" * 20)
        # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # self.seg_button_1.set("Value 2")
        self.label = customtkinter.CTkLabel(master=self.textbox, text='Select an Image Format:')
    # Camera Access
    # For Color Image Function
    

    def color_frme(self):
        flag = 1
        print(flag)
        ret, depth_frame, color_frame = dc.get_frame()
        if ret:
            if(flag==1):
                image = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
            # if(flag==0):
            #     image = Image.fromarray(depth_frame)        
            photo = customtkinter.CTkImage(self.textbox,image)
            self.label.configure(image=photo)
            self.label.image = photo
            self.label.grid()
            # cv2.imshow("Color frame", color_frame)
            # key = cv2.waitKey(1)
            # if key == 27:
            #     print("YES")
              
                    
        self.label.after(100, self.color_frme)
    
    # Camera Is Running - show in a text box -- Open Camera Button Hit    
    def OpenCamera_btn(self):
        self.entry.delete(0, tk.END)
        a= self.entry.insert(0,"OpenCamera Button Hit......")
        self.color_frme()
        print(a)
        
    def button_click1(self):
        print('Button clicked 1')
        
    # Capture_Image Button Hit     
    def CaptureImage_btn(self):
        self.entry.delete(0, tk.END)
        a= self.entry.insert(0,"Capture_Image Button Hit......") 
        print(a)
        
    # Refresh Button Hit     
    def Refresh_btn(self):
        self.entry.delete(0, tk.END)
        a= self.entry.insert(0,"Refresh Button Hit......")
        print(a)    
    
        
    # Create a function that calls both functions
    def call_both_functions(self):
        self.button_click()
        self.button_click1()
        
    def open_input_dialog_event(self):
        dialog1 = customtkinter.CTkInputDialog(text="Type x, y, z coordinates:", title="CoordinateValue")
        print("X, Y, Z coordinates : ", dialog1.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):    
        customtkinter.set_appearance_mode(new_appearance_mode)
        if(new_appearance_mode=="Origin"):
            self.entry.delete(0, tk.END)
            a= self.entry.insert(0,"Origin Button Hit......")
            
        elif(new_appearance_mode=="Plucking"):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Plucking Button Hit......")
        elif(new_appearance_mode=="Color_Frame"):
            self.entry.delete(0,tk.END)
            self.entry.insert(0,"Color Frame Button Hit....")
        elif(new_appearance_mode=="Depth_Frame"):
            self.entry.delete(0,tk.END)
            self.entry.insert(0,"Depth Frame Button Hit...")
        elif(new_appearance_mode=="Pointing"):
            self.entry.delete(0,tk.END)
            self.entry.insert(0, "Pointing Button Hit.....")

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    # app.color_frme()
    app.mainloop()