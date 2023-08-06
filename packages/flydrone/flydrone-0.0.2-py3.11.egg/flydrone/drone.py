from pymavlink import mavutil
from dataclasses import dataclass

@dataclass
class Drone:
    the_connection: mavutil
    connection_url: str
    waypoints = []

    def __init__(self, url: str = 'udpin:localhost:14550'):
        self.the_connection = mavutil.mavlink_connection(url)
        self.connection_url = url
        self.heartbeat = self.the_connection.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.the_connection.target_system, self.the_connection.target_component))

    def return_to_launch(self, parameters: list[int] = [0, 0, 0, 0, 0, 0, 0, 0], change_mode: bool = True) -> None:
        RETURN_TO_LAUNCH_CMD = 20

        # return to launch
        self.the_connection.mav.command_long_send(
            self.the_connection.target_system, 
            self.the_connection.target_component,
            RETURN_TO_LAUNCH_CMD, 
            *parameters
        )
        return self.check()      
        

    def arm (self, parameters: list[int] = [0,0,0,0,0,0]) -> None :
        ARM_OR_DISARM_CMD = 400 
        ARM: int = 1

        self.the_connection.mav.command_long_send(
            self.the_connection.target_system, 
            self.the_connection.target_component, 
            ARM_OR_DISARM_CMD, 
            0, 
            ARM, 
            *parameters
        )
        return self.check()      
        

    def disarm (self, parameters: list[int] = [0,0,0,0,0,0]) -> None :
        ARM_OR_DISARM_CMD = 400 
        DISARM: int = 0

        self.the_connection.mav.command_long_send(
            self.the_connection.target_system, 
            self.the_connection.target_component, 
            ARM_OR_DISARM_CMD, 
            0, 
            DISARM, 
            *parameters
        )
        return self.check()      
        
        

    def takeoff(self , parameters: list[int] = [0, 0, 0, 0, 0, 0, 0] , arm: bool = False, altitude: int = 10) -> None :

        TAKEOFF_CMD = 22 

        if(arm == True): self.arm()

        self.the_connection.mav.command_long_send(
            self.the_connection.target_system, 
            self.the_connection.target_component,  
            TAKEOFF_CMD, 
            *parameters, 
            altitude
        )
        return self.check()      
        
        

    def local_movement(self, 
        depth_position: int, 
        horizontal_position: int, 
        vertical_position: int,
        depth_velocity: int = 0, 
        horizontal_velocity: int = 0, 
        vertical_velocity: int = 0,
        depth_acceleration: int = 0, 
        horizontal_acceleration: int = 0, 
        vertical_acceleration: int = 0,
        rotation: int = 0,
        rotation_degree: int = 0)  -> None :

        BOOT_TIME_MILLISECONDS: int = 10

        FORWARD_BACKWARD_POSITION_AXIS: int = depth_position
        RIGHT_LEFT_POSITION_AXIS: int = horizontal_position
        UP_DOWN_POSITION_AXIS: int = -1 * vertical_position

        FORWARD_BACKWARD_VELOCITY_AXIS: int = depth_velocity
        RIGHT_LEFT_VELOCITY_AXIS: int = horizontal_velocity
        UP_DOWN_VELOCITY_AXIS: int = -1 * vertical_velocity

        FORWARD_BACKWARD_ACCELERATION_AXIS: int = depth_acceleration
        RIGHT_LEFT_ACCELERATION_AXIS: int = horizontal_acceleration
        UP_DOWN_ACCELERATION_AXIS: int = -1 * vertical_acceleration

        YAW: int = rotation
        YAW_DEGREE: int = rotation_degree

        FRAME_TYPE = mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED
        
        IGNORE_X_POSITION: bool = False
        IGNORE_Y_POSITION: bool = False
        IGNORE_Z_POSITION: bool = False

        IGNORE_X_VELOCITY: bool = True if depth_velocity == 0 else False
        IGNORE_Y_VELOCITY: bool = True if horizontal_velocity == 0 else False
        IGNORE_Z_VELOCITY: bool = True if vertical_velocity == 0 else False

        IGNORE_X_ACCELERATION: bool = True if depth_acceleration == 0 else False
        IGNORE_Y_ACCELERATION: bool = True if horizontal_acceleration == 0 else False
        IGNORE_Z_ACCELERATION: bool = True if vertical_acceleration == 0 else False

        USE_FORCE: bool = False
        
        IGNORE_YAW: bool = True if rotation == 0 else False
        IGNORE_YAW_RATE: bool = True if rotation_degree == 0 else False
        
        MASK_RULES: str = str(
            str(int(IGNORE_YAW_RATE))+
            str(int(IGNORE_YAW))+
            str(int(USE_FORCE))+
            str(int(IGNORE_Z_ACCELERATION))+
            str(int(IGNORE_Y_ACCELERATION))+
            str(int(IGNORE_X_ACCELERATION))+
            str(int(IGNORE_Z_VELOCITY))+
            str(int(IGNORE_Y_VELOCITY))+
            str(int(IGNORE_X_VELOCITY))+
            str(int(IGNORE_Z_POSITION))+
            str(int(IGNORE_Y_POSITION))+
            str(int(IGNORE_X_POSITION))
        )
        
        

        SET_LOCAL_POSITION_CMD = mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            BOOT_TIME_MILLISECONDS, 

            self.the_connection.target_system,
            self.the_connection.target_component, 

            FRAME_TYPE, 
            
            int("0b"+MASK_RULES, 2), #first, convert MASK_RULES to binary by adding 0b in the first of the string. Second, convert that string binary to an actual binary by int("string_binary_here", base_2) will result in an actual binary instead of a binary as a string

            FORWARD_BACKWARD_POSITION_AXIS, 
            RIGHT_LEFT_POSITION_AXIS,
            UP_DOWN_POSITION_AXIS, 

            FORWARD_BACKWARD_VELOCITY_AXIS,
            RIGHT_LEFT_VELOCITY_AXIS,
            UP_DOWN_VELOCITY_AXIS,

            FORWARD_BACKWARD_ACCELERATION_AXIS,
            RIGHT_LEFT_ACCELERATION_AXIS,
            UP_DOWN_ACCELERATION_AXIS,  
            
            YAW,
            YAW_DEGREE
        )
        self.the_connection.mav.send(SET_LOCAL_POSITION_CMD)
        return self.check()      
        
    
    def global_movement(self, 
        latitude_position: int, 
        longtitude_position: int, 
        altitude_position: int,
        latitude_velocity: int = 0, 
        longtitude_velocity: int = 0, 
        altitude_velocity: int = 0,
        latitude_acceleration: int = 0, 
        longtitude_acceleration: int = 0, 
        altitude_acceleration: int = 0,
        rotation: int = 0,
        rotation_degree: int = 0)  -> None :

        BOOT_TIME_MILLISECONDS: int = 10

        FORWARD_BACKWARD_POSITION_AXIS: int = latitude_position
        RIGHT_LEFT_POSITION_AXIS: int = longtitude_position
        UP_DOWN_POSITION_AXIS: int = -1 * altitude_position

        FORWARD_BACKWARD_VELOCITY_AXIS: int = latitude_velocity
        RIGHT_LEFT_VELOCITY_AXIS: int = longtitude_velocity
        UP_DOWN_VELOCITY_AXIS: int = -1 * altitude_velocity

        FORWARD_BACKWARD_ACCELERATION_AXIS: int = latitude_acceleration
        RIGHT_LEFT_ACCELERATION_AXIS: int = longtitude_acceleration
        UP_DOWN_ACCELERATION_AXIS: int = -1 * altitude_acceleration

        YAW: int = rotation
        YAW_DEGREE: int = rotation_degree

        FRAME_TYPE = mavutil.mavlink.MAV_FRAME_GLOBAL
        
        IGNORE_X_POSITION: bool = False
        IGNORE_Y_POSITION: bool = False
        IGNORE_Z_POSITION: bool = False

        IGNORE_X_VELOCITY: bool = True if depth_velocity == 0 else False
        IGNORE_Y_VELOCITY: bool = True if horizontal_velocity == 0 else False
        IGNORE_Z_VELOCITY: bool = True if vertical_velocity == 0 else False

        IGNORE_X_ACCELERATION: bool = True if depth_acceleration == 0 else False
        IGNORE_Y_ACCELERATION: bool = True if horizontal_acceleration == 0 else False
        IGNORE_Z_ACCELERATION: bool = True if vertical_acceleration == 0 else False

        USE_FORCE: bool = False
        
        IGNORE_YAW: bool = True if rotation == 0 else False
        IGNORE_YAW_RATE: bool = True if rotation_degree == 0 else False
        
        MASK_RULES: str = str(
            str(int(IGNORE_YAW_RATE))+
            str(int(IGNORE_YAW))+
            str(int(USE_FORCE))+
            str(int(IGNORE_Z_ACCELERATION))+
            str(int(IGNORE_Y_ACCELERATION))+
            str(int(IGNORE_X_ACCELERATION))+
            str(int(IGNORE_Z_VELOCITY))+
            str(int(IGNORE_Y_VELOCITY))+
            str(int(IGNORE_X_VELOCITY))+
            str(int(IGNORE_Z_POSITION))+
            str(int(IGNORE_Y_POSITION))+
            str(int(IGNORE_X_POSITION))
        )

        SET_GLOBAL_POSITION_CMD = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
            BOOT_TIME_MILLISECONDS, 

            self.the_connection.target_system,
            self.the_connection.target_component, 

            FRAME_TYPE, 
            
            int("0b"+MASK_RULES, 2), #first, convert MASK_RULES to binary by adding 0b in the first of the string. Second, convert that string binary to an actual binary by int("string_binary_here", base_2) will result in an actual binary instead of a binary as a string

            FORWARD_BACKWARD_POSITION_AXIS, 
            RIGHT_LEFT_POSITION_AXIS,
            UP_DOWN_POSITION_AXIS, 

            FORWARD_BACKWARD_VELOCITY_AXIS,
            RIGHT_LEFT_VELOCITY_AXIS,
            UP_DOWN_VELOCITY_AXIS,

            FORWARD_BACKWARD_ACCELERATION_AXIS,
            RIGHT_LEFT_ACCELERATION_AXIS,
            UP_DOWN_ACCELERATION_AXIS,  
            
            YAW,
            YAW_DEGREE
        )
        self.the_connection.mav.send(SET_GLOBAL_POSITION_CMD)
        return self.check()      
        

    def old_add_new_waypoint(self, longtitude: float, latitude: float, altitude: float):
        location: dict[str, float] = {
            "latitude": latitude,
            "longtitude": longtitude,
            "altitude": altitude
        }
        self.waypoints.append(location)

    def old_delete_all_waypoints(self):
        self.waypoints.clear()
        
    def old_move_to_waypoints(self, hold_time: int = 5, accept_radius: int = 10, pass_radius: int = 5, yaw: int = 0):
        NAV_WAYPOINT_CMD: int = 16

        HOLD_TIME: int = hold_time

        ACCEPT_RADIUS_METERS: int = accept_radius
        PASS_RADIUS_METERS: int = pass_radius

        YAW: int = yaw

        for waypoint in self.waypoints:
            self.the_connection.mav.command_long_send(
                self.the_connection.target_system,
                self.the_connection.target_component,
                NAV_WAYPOINT_CMD,
                0,
                HOLD_TIME,
                ACCEPT_RADIUS_METERS,
                PASS_RADIUS_METERS,
                YAW,
                waypoint["latitude"],
                waypoint["longtitude"],
                waypoint["altitude"]
            )

    def add_new_waypoint(self, latitude: float, longtitude: float, altitude: float):
        self.the_connection.mav.mission_count_send(
            self.the_connection.target_system, 
            self.the_connection.target_component, 
            0, 
            0
        )

        print(self.the_connection.recv_match(type="MISSION_REQUEST", blocking=True))

        NAV_WAYPOINT_CMD: int = 16

        self.the_connection.mav.mission_item_send(
            target_system=self.the_connection.target_system, 
            target_component=self.the_connection.target_component, 
            seq=self.mission_count, # sequence (means the mission count, 0 is the first mission)
            current=0, # just make it zero
            autocontinue=1, # when finish mission 0 go to mission 1 automaticaly .....
            mission_type=0, # just make it zero 
            command= NAV_WAYPOINT_CMD,
            frame= mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # global frame
            x=latitude, # latitude
            y=longtitude, # longitude
            z=altitude, # altitude
            param1=0,param2=10,param3=5,param4=0 #other parameters
        )

        self.mission_count += 1

        return self.the_connection.recv_match(type="MISSION_ACK", blocking=True)
    
    def move_to_waypoints(self):
        MISSION_START_CMD: int = 300
        self.the_connection.mav.command_long_send(
            self.the_connection.target_system, 
            self.the_connection.target_component, 
            MISSION_START_CMD, # to start the mission
            0,0,0,0,0,0,0,0
        )
        return self.check()
    
    def change_mode(self , mode: str = 'GUIDED'):
        MAV_CHANGE_MODE_COMMAND = mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED 

        mode_id = self.the_connection.mode_mapping()[mode]
        self.the_connection.mav.set_mode_send(
            self.the_connection.target_system,
            MAV_CHANGE_MODE_COMMAND,
            mode_id
        )
        return self.check()      
        

    def sync_with_drone(self):
        GPS_INFO = self.the_connection.recv_match(type="GPS_RAW_INT", blocking=True)
        LOCAL_POSITION_INFO = self.the_connection.recv_match(type="LOCAL_POSITION_NED", blocking=True)
        SYSTEM_STATUS_INFO = self.the_connection.recv_match(type="SYS_STATUS", blocking=True)
        HEARTBEAT_INFO = self.the_connection.recv_match(type="HEARTBEAT", blocking=True)
        
        self.latitude = GPS_INFO.lat / 10 ** 7
        self.longtitude= GPS_INFO.lon / 10 ** 7
        self.altitude= LOCAL_POSITION_INFO.z * -1
        self.battery_remaining = SYSTEM_STATUS_INFO.battery_remaining
        if(HEARTBEAT_INFO.custom_mode == 3):
            self.mode = "AUTO"
        if(HEARTBEAT_INFO.custom_mode == 4):
            self.mode = "GUIDED"
        if(HEARTBEAT_INFO.custom_mode == 6):
            self.mode = "RTL"
            

    def check(self) : 
        check = self.the_connection.recv_match(type="COMMAND_ACK", blocking=True )
        if (check.result == 0)  : return "Command is valid "  
        if (check.result == 1)  : return "Command is valid, but cannot be executed at this time"
        if (check.result == 2)  : return "Command is invalid"
        if (check.result == 3)  : return "Command is not supported"
        if (check.result == 4)  : return "Command is valid, but execution has failed. This is used to indicate any non-temporary or unexpected problem"
        if (check.result == 5)  : return "Command is valid and is being executed."   
        if (check.result == 6)  : return "Command has been cancelled"  
        