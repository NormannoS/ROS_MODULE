#!/usr/bin/env python

import rospy
from xml.etree import ElementTree as ET
from geometry_msgs.msg import Twist
from base_class import Base
from base_class import topics
from sgr_project.msg import Personality


class ParametersPublisher(Base):

    options = {
        "1": "Update personality parameters",
        "2": "Display actual personality",
        "3": "Update linear velocity",
        "4": "Display linear velocity",
        "5": "Update angular velocity",
        "6": "Display angular velocity",
        "h": "Display all options",
        "e": "exit"
    }

    def __init__(self, base_topics):
        super(ParametersPublisher, self).__init__()
        self.personality_publisher = rospy.Publisher(base_topics["publishers"]["personality_ctrl"], Personality)
        self.velocity_publisher = rospy.Publisher(base_topics["publishers"]["velocity_ctrl"], Twist)
        self.options_functions = {
                "1": self.update_personality,
                "2": self.display_actual_personlity,
                "3": self.update_linear_velocity,
                "4": self.display_actual_linear_velocity,
                "5": self.update_angular_velocity,
                "6": self.display_actual_angular_velocity,
                "h": self.display_options
            }
        self.velocity = Twist()
        self.personality = Personality()
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.extraversion = 0.0
        self.agreebleness = 0.0
        self.concientiouness = 0.0
        self.neuroticism = 0.0
        self.openness = 0.0
        #TODO READ FROM FILE
        self.init_parameters()

    def init_parameters(self):
        velocity_tree = ET.parse('init_files/velocity.xml')
        personality_tree = ET.parse('init_files/personality.xml')
        velocity_root = velocity_tree.getroot()
        personality_root = personality_tree.getroot()

        if velocity_root.find('linear') is not None:
            self.velocity.linear.x = float(velocity_root.find('linear').value)
        if velocity_root.find('angular') is not None:
            self.velocity.angular.z = float(velocity_root.find('angular').value)

        if personality_root.find('extraversion') is not None:
            self.personality.extraversion = float(personality_root.find('extraversion').value)

        if personality_root.find('agreebleness') is not None:
            self.personality.agreebleness = float(personality_root.find('agreebleness').value)

        if personality_root.find('concientiouness') is not None:
            self.personality.concientiouness = float(personality_root.find('concientiouness').value)

        if personality_root.find('neuroticism') is not None:
            self.personality.neuroticism = float(personality_root.find('neuroticism').value)

        if personality_root.find('openness') is not None:
            self.personality.openness = float(personality_root.find('openness').value)

    def keyboard_input_loop(self):
        exit_loop = False
        choice = None
        while not exit_loop:
            self.display_options()
            choice = input("Option: ")
            if choice in ParametersPublisher.options.keys() and choice != "e":
                self.options_functions[choice]()
            elif choice == "e":
                exit_loop = True
            else:
                print "Wrong input"

    def publish_velocity(self):
        self.velocity_publisher.publish(self.velocity)

    def update_linear_velocity(self):
        new_linear_velocity = input("Linear velocity (actual"+str(self.velocity.linear.x)+") :")
        try:
            new_linear_velocity_value = float(new_linear_velocity)
            self.velocity.angular.x = new_linear_velocity_value
        except ValueError:
            print "ERROR:" + str(new_linear_velocity) + " is not a number!"
            return
        self.publish_velocity()

    def display_actual_linear_velocity(self):
        print "Actual linear velocity : " + str(self.velocity.linear.x)

    def update_angular_velocity(self):
        new_angular_velocity = input("Angular velocity (actual"+str(self.velocity.angular.z)+") :")
        try:
            new_angular_velocity_value = float(new_angular_velocity)
            self.velocity.angular.z = new_angular_velocity_value
        except ValueError:
            print "ERROR:" + str(new_angular_velocity) + " is not a number!"
            return
        self.publish_velocity()

    def display_actual_angular_velocity(self):
        print "Actual angular velocity : " + str(self.velocity.angular.z)

    def display_options(self):
        print "Available options: "
        for k in ParametersPublisher.options.keys():
            print "\t-" + k + " : " + ParametersPublisher.options.get(k)

    def update_personality(self):
        print "***Updating personality parameters***"
        try:
            extraversion_value = float(input("Extraversion (actual " + str(self.extraversion) + " : "))
            agreebleness_value = float(input("Agreebleness (actual " + str(self.agreebleness) + " : "))
            concientiouness_value = float(input("Concientioness (actual " + str(self.concientiouness) + " : "))
            neuroticism_value = float(input("Neuroticism (actual " + str(self.neuroticism) + " : "))
            openness_value = float(input("Openness (actual " + str(self.openness) + " : "))
        except ValueError:
            print "ERROR: not a number!"
            return
        self.personality.extraversion = extraversion_value
        self.personality.agreebleness = agreebleness_value
        self.personality.concientiouness = concientiouness_value
        self.personality.neuroticism = neuroticism_value
        self.personality.openness = openness_value
        self.personality_publisher.publish(self.personality)
        print "***Parameters successfully updated***"

        #TODO update self values and publish on control topic

    def display_actual_personlity(self):
        print "***Actual personality parameters***"
        print "\t-Extraversion : " + str(self.personality.extraversion)
        print "\t-Agreebleness : " + str(self.personality.agreebleness)
        print "\t-Concientioness : " + str(self.personality.concientiouness)
        print "\t-Neuroticism : " + str(self.personality.neuroticism)
        print "\t-Openness : " + str(self.personality.openness)
        print "***********************************"


if __name__ == '__main__':
    print "Wellcome"
    personality_publisher = ParametersPublisher(topics)
    personality_publisher.keyboard_input_loop()
    print "Good Bye!"